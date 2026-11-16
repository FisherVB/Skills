#!/usr/bin/env python3
"""Check name availability: domains (via RDAP) and optional social handles.

Why RDAP and not WHOIS/DNS:
  - DNS says nothing about registration — a registered domain can have no site.
  - WHOIS is unstructured, rate-limited, and inconsistent per TLD.
  - RDAP (RFC 7482/9082) is the registries' official, JSON, keyless successor.
    A 404 from the *authoritative* registry means "no such registration" →
    the domain is available. A 200 means it's registered.

Why we resolve the server via IANA's bootstrap (not a proxy like rdap.org):
  - A proxy returns its own 404 for TLDs it doesn't know (e.g. .io), which is
    indistinguishable from a real "not registered" 404 — a dangerous false
    "available". We instead load IANA's bootstrap (data.iana.org/rdap/dns.json),
    find the authoritative RDAP server for the TLD, and query it directly.
  - TLDs absent from the bootstrap (many ccTLDs: .io, .co, .me, .us, .sh, ...)
    have no usable RDAP endpoint here → we report "unknown", never "available".

Everything here is stdlib-only (urllib) so the script runs anywhere Python 3
runs, with no pip install and no API keys.

IMPORTANT — read the caveats:
  * "available" = not currently registered. A registrar may still sell it as a
    premium/reserved name. Confirm at a registrar before relying on it.
  * "unknown" = no RDAP endpoint for that TLD, or the lookup failed. NOT the
    same as available. Some ccTLDs aren't in RDAP and need a manual check.
  * Handle probes are indicative only: parked/suspended handles look taken,
    and some platforms soft-404 or rate-limit real profiles. Verify by hand.

Usage:
  python3 check_availability.py --tld com,io,ai "acme" "Acme Labs" "acmeio"
  python3 check_availability.py --tld com --handles "acme" "vero"
  python3 check_availability.py --json --tld com,io "acme"

Notes:
  * Name args are slugified for the domain label (lowercased, spaces/underscores
    dropped, only [a-z0-9-] kept) so you can pass human-readable names directly.
  * Be polite: this hits public endpoints. Keep lists reasonable.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

# IANA's official RDAP bootstrap: maps every TLD to its authoritative RDAP
# server. Fetched once per run and cached in _BOOTSTRAP.
IANA_RDAP_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"

USER_AGENT = "naming-agent-availability-check/1.0 (+stdlib urllib)"
TIMEOUT = 12

_BOOTSTRAP = None  # dict: tld -> authoritative RDAP base URL (trailing slash)


def load_bootstrap() -> dict:
    """Load and cache the IANA TLD -> RDAP-server map. Empty dict on failure."""
    global _BOOTSTRAP
    if _BOOTSTRAP is not None:
        return _BOOTSTRAP
    mapping = {}
    try:
        data = json.loads(_get(IANA_RDAP_BOOTSTRAP).read().decode("utf-8"))
        for service in data.get("services", []):
            tlds, urls = service[0], service[1]
            base = next((u for u in urls if u.startswith("https://")), urls[0] if urls else None)
            if not base:
                continue
            if not base.endswith("/"):
                base += "/"
            for tld in tlds:
                mapping[tld.lower()] = base
    except Exception:  # noqa: BLE001 - treat any failure as "no bootstrap"
        mapping = {}
    _BOOTSTRAP = mapping
    return mapping

# Profile-URL templates for a first-pass handle probe. Not an API — just the
# public profile page. 404 → likely free; 200 → likely taken (with false
# positives for parked/suspended accounts).
HANDLE_PLATFORMS = {
    "instagram": "https://www.instagram.com/{h}/",
    "x": "https://x.com/{h}",
    "tiktok": "https://www.tiktok.com/@{h}",
    "github": "https://github.com/{h}",
    "youtube": "https://www.youtube.com/@{h}",
}

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def slug(name: str) -> str:
    """Human name -> domain label. 'Acme Labs' -> 'acmelabs'."""
    s = name.strip().lower()
    s = s.replace(" ", "").replace("_", "")
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = s.strip("-")
    return s


def handle_slug(name: str) -> str:
    """Human name -> handle. 'Acme Labs' -> 'acmelabs' (no dashes)."""
    return slug(name).replace("-", "")


def _get(url: str, method: str = "GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=TIMEOUT)


def resolve_rdap_base(tld: str):
    """Find the authoritative RDAP base for a (possibly multi-label) TLD.

    Multi-label public suffixes like 'com.br' aren't keys in the bootstrap — the
    registry is keyed by 'br'. So try the full suffix, then strip leftmost labels
    until a bootstrap entry matches ('com.br' -> 'br' -> registro.br). The full
    domain is still queried against whichever server we find.
    """
    mapping = load_bootstrap()
    parts = tld.split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in mapping:
            return mapping[candidate]
    return None


def check_domain(label: str, tld: str) -> dict:
    """Return {'domain','status','detail'}; status in available/registered/unknown.

    A 404 counts as "available" only because it came from the TLD's *authoritative*
    RDAP server (resolved via IANA bootstrap), so it genuinely means "no such
    registration" — not "I don't know this TLD".
    """
    domain = f"{label}.{tld}"
    base = resolve_rdap_base(tld)
    if base is None:
        return {
            "domain": domain,
            "status": "unknown",
            "detail": "no RDAP for this TLD (check manually)",
        }
    url = f"{base}domain/{domain}"
    try:
        _get(url)
        return {"domain": domain, "status": "registered", "detail": "RDAP 200"}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"domain": domain, "status": "available", "detail": "RDAP 404 (authoritative)"}
        if e.code == 400:
            return {"domain": domain, "status": "unknown", "detail": "RDAP 400 (bad/invalid)"}
        if e.code in (429, 503):
            return {"domain": domain, "status": "unknown", "detail": f"RDAP {e.code} (rate/again)"}
        return {"domain": domain, "status": "unknown", "detail": f"RDAP {e.code}"}
    except urllib.error.URLError as e:
        return {"domain": domain, "status": "unknown", "detail": f"lookup failed ({e.reason})"}
    except Exception as e:  # noqa: BLE001 - surface anything odd as unknown
        return {"domain": domain, "status": "unknown", "detail": str(e)}


def check_handle(platform: str, handle: str) -> dict:
    url = HANDLE_PLATFORMS[platform].format(h=handle)
    try:
        resp = _get(url, method="GET")
        code = resp.getcode()
        if code == 200:
            return {"platform": platform, "handle": handle, "status": "taken", "detail": "200"}
        if code == 404:
            return {"platform": platform, "handle": handle, "status": "available", "detail": "404"}
        return {"platform": platform, "handle": handle, "status": "unknown", "detail": str(code)}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"platform": platform, "handle": handle, "status": "available", "detail": "404"}
        if e.code in (403, 429):
            return {"platform": platform, "handle": handle, "status": "unknown", "detail": f"{e.code} (blocked/rate)"}
        return {"platform": platform, "handle": handle, "status": "unknown", "detail": str(e.code)}
    except urllib.error.URLError as e:
        return {"platform": platform, "handle": handle, "status": "unknown", "detail": str(e.reason)}
    except Exception as e:  # noqa: BLE001
        return {"platform": platform, "handle": handle, "status": "unknown", "detail": str(e)}


def _mark(status: str) -> str:
    return {
        "available": f"{GREEN}available{RESET}",
        "registered": f"{RED}taken{RESET}",
        "taken": f"{RED}taken{RESET}",
        "unknown": f"{YELLOW}unknown{RESET}",
    }.get(status, status)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check domain (RDAP) and optional social-handle availability for name ideas.",
    )
    ap.add_argument("names", nargs="+", help="One or more name ideas (human-readable is fine).")
    ap.add_argument("--tld", default="com", help="Comma-separated TLDs to check (default: com).")
    ap.add_argument("--handles", action="store_true", help="Also probe social handles.")
    ap.add_argument(
        "--platforms",
        default=",".join(HANDLE_PLATFORMS),
        help="Comma-separated platforms for --handles (default: all known).",
    )
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")
    args = ap.parse_args()

    tlds = [t.strip().lstrip(".").lower() for t in args.tld.split(",") if t.strip()]
    platforms = [p.strip().lower() for p in args.platforms.split(",") if p.strip()]
    bad = [p for p in platforms if p not in HANDLE_PLATFORMS]
    if args.handles and bad:
        print(f"Unknown platform(s): {', '.join(bad)}. Known: {', '.join(HANDLE_PLATFORMS)}", file=sys.stderr)
        return 2

    results = []
    for name in args.names:
        label = slug(name)
        entry = {"input": name, "label": label, "domains": [], "handles": []}
        if not label:
            entry["error"] = "name produced an empty domain label"
            results.append(entry)
            continue
        for tld in tlds:
            entry["domains"].append(check_domain(label, tld))
        if args.handles:
            h = handle_slug(name)
            for p in platforms:
                entry["handles"].append(check_handle(p, h))
        results.append(entry)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    for entry in results:
        header = f"{entry['input']}"
        if entry["label"] and entry["label"] != entry["input"].lower():
            header += f"  {DIM}({entry['label']}){RESET}"
        print(f"\n{header}")
        if entry.get("error"):
            print(f"  {YELLOW}! {entry['error']}{RESET}")
            continue
        for d in entry["domains"]:
            print(f"  {d['domain']:<28} {_mark(d['status']):<22} {DIM}{d['detail']}{RESET}")
        for h in entry["handles"]:
            who = f"@{h['handle']} on {h['platform']}"
            print(f"  {who:<28} {_mark(h['status']):<22} {DIM}{h['detail']}{RESET}")

    print(
        f"\n{DIM}RDAP 'available' = not registered now; confirm at a registrar "
        f"(premium/reserved names exist). 'unknown' != available. "
        f"Handle probes are indicative — verify finalists by hand.{RESET}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
