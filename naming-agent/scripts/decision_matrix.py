#!/usr/bin/env python3
"""Monta e ranqueia a Matriz de Decisão do método de naming (notas 0 a 3).

Pontuar é subjetivo — quem dá as notas é a pessoa (ou o agente, junto com ela).
Este script só faz a parte determinística: valida a escala 0–3, soma, ordena e
marca o top 3. Assim a matriz fica reproduzível e fácil de revisitar no Passo 8.

Entrada: um JSON. A forma mínima é um dicionário nome -> lista de notas, uma por
critério, na ordem dos critérios do método (10 por padrão):

    {
      "Keel":   [3, 3, 3, 2, 2, 3, 2, 3, 2, 3],
      "Lumen":  [3, 2, 3, 3, 1, 2, 3, 2, 2, 2],
      "Vero":   [2, 3, 3, 3, 2, 3, 1, 3, 2, 2]
    }

Ou a forma completa, pra trocar/encurtar os critérios:

    {
      "criteria": ["Internacional", "Soa bem", "Pronúncia", ...],
      "scores": { "Keel": [3,3,3,...], ... }
    }

Uso:
    python3 decision_matrix.py matriz.json
    python3 decision_matrix.py matriz.json --json
    cat matriz.json | python3 decision_matrix.py -

Stdlib puro. Sem dependências.
"""

import argparse
import json
import sys

CRITERIOS_PADRAO = [
    "Funciona internacionalmente",
    "Soa bem / agradável",
    "Fácil de pronunciar",
    "Se escreve como se fala",
    "Fácil de buscar no Google",
    "Registrável (domínio e nome)",
    "Transmite benefício / mensagem",
    "Memorável",
    "Causa impacto",
    "É único",
]

MAX_NOTA = 3

GREEN = "\033[32m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def parse_input(raw: str):
    """Return (criteria, scores_dict). Accepts minimal or full shape."""
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("o JSON precisa ser um objeto")
    if "scores" in data:
        criteria = data.get("criteria", CRITERIOS_PADRAO)
        scores = data["scores"]
    else:
        criteria = CRITERIOS_PADRAO
        scores = data
    if not isinstance(scores, dict) or not scores:
        raise ValueError("nenhum nome com notas encontrado")
    return criteria, scores


def validate(criteria, scores):
    errors = []
    n = len(criteria)
    for name, row in scores.items():
        if not isinstance(row, list):
            errors.append(f"{name}: notas precisam ser uma lista")
            continue
        if len(row) != n:
            errors.append(f"{name}: {len(row)} notas, mas há {n} critérios")
        for i, v in enumerate(row):
            if not isinstance(v, (int, float)) or v < 0 or v > MAX_NOTA:
                crit = criteria[i] if i < n else f"#{i+1}"
                errors.append(f"{name}: nota {v!r} em '{crit}' fora de 0..{MAX_NOTA}")
    return errors


def rank(criteria, scores):
    rows = []
    for name, row in scores.items():
        total = sum(row)
        rows.append({"name": name, "scores": row, "total": total})
    rows.sort(key=lambda r: r["total"], reverse=True)
    for i, r in enumerate(rows):
        r["rank"] = i + 1
        r["top3"] = i < 3
    return rows


def render_table(criteria, rows) -> str:
    n = len(criteria)
    max_total = n * MAX_NOTA
    header = "| # | Nome | " + " | ".join(f"C{i+1}" for i in range(n)) + " | Total |"
    sep = "|" + "---|" * (n + 3)
    lines = [header, sep]
    for r in rows:
        cells = " | ".join(str(s) for s in r["scores"])
        mark = " 🏆" if r["top3"] else ""
        lines.append(f"| {r['rank']} | **{r['name']}**{mark} | {cells} | {r['total']}/{max_total} |")
    legend = "\n".join(f"- **C{i+1}** — {c}" for i, c in enumerate(criteria))
    return "\n".join(lines) + "\n\n" + legend


def render_pretty(criteria, rows) -> str:
    max_total = len(criteria) * MAX_NOTA
    out = [f"\n{BOLD}Matriz de Decisão — ranqueada (0..{MAX_NOTA} por critério){RESET}\n"]
    for r in rows:
        bar = "█" * r["total"] + "·" * (max_total - r["total"])
        mark = f"{GREEN}🏆{RESET}" if r["top3"] else "  "
        out.append(f"{mark} {r['rank']:>2}. {r['name']:<16} {r['total']:>3}/{max_total}  {DIM}{bar}{RESET}")
    top = [r["name"] for r in rows if r["top3"]]
    out.append(f"\n{BOLD}Top 3 pra votação:{RESET} " + ", ".join(top))
    out.append(f"{DIM}Critérios: " + "; ".join(f"C{i+1}={c}" for i, c in enumerate(criteria)) + RESET)
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Ranqueia a Matriz de Decisão de naming (notas 0 a 3).")
    ap.add_argument("file", help="arquivo JSON com as notas, ou '-' pra stdin")
    ap.add_argument("--json", action="store_true", help="saída JSON (ranqueada) em vez de tabela")
    ap.add_argument("--markdown", action="store_true", help="tabela em Markdown (boa pra colar em doc)")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    try:
        criteria, scores = parse_input(raw)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Erro lendo a entrada: {e}", file=sys.stderr)
        return 2

    errors = validate(criteria, scores)
    if errors:
        print("Matriz inválida:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2

    rows = rank(criteria, scores)

    if args.json:
        print(json.dumps({"criteria": criteria, "ranking": rows, "max_total": len(criteria) * MAX_NOTA}, ensure_ascii=False, indent=2))
    elif args.markdown:
        print(render_table(criteria, rows))
    else:
        print(render_pretty(criteria, rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
