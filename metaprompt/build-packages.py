#!/usr/bin/env python3
"""Gera de novo os pacotes do metaprompt a partir dos arquivos desta pasta.

Saidas (sobrescritas nesta mesma pasta):
    metaprompt.skill       -> metaprompt/SKILL.md            (Claude.ai / Cowork)
    metaprompt-plugin.zip  -> metaprompt-plugin/...          (plugin do Claude Code)

O layout do plugin e montado assim:
    .claude-plugin/plugin.json   <- plugin.json
    commands/metaprompt.md       <- commands/metaprompt.md
    skills/metaprompt/SKILL.md   <- SKILL.md
    README.md                    <- README.md

Rode depois de qualquer mudanca em SKILL.md, README.md, commands/ ou plugin.json,
e suba a `version` do plugin.json a cada mudanca publicada. As datas dentro dos
arquivos zip sao fixas para que o mesmo conteudo gere o mesmo pacote.

Uso:
    python3 metaprompt/build-packages.py
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "metaprompt"
FIXED_DATE = (2026, 1, 1, 0, 0, 0)


def write(zf: zipfile.ZipFile, arcname: str, data: bytes) -> None:
    info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def read(rel: str) -> bytes:
    return (HERE / rel).read_bytes()


def main() -> None:
    manifest = json.loads(read("plugin.json"))
    if manifest.get("name") != NAME:
        raise SystemExit(f"plugin.json precisa ter name = {NAME!r}")

    skill_path = HERE / f"{NAME}.skill"
    with zipfile.ZipFile(skill_path, "w") as zf:
        write(zf, f"{NAME}/SKILL.md", read("SKILL.md"))

    commands = sorted((HERE / "commands").glob("*.md"))
    plugin_path = HERE / f"{NAME}-plugin.zip"
    root = f"{NAME}-plugin"
    with zipfile.ZipFile(plugin_path, "w") as zf:
        write(zf, f"{root}/.claude-plugin/plugin.json", read("plugin.json"))
        for cmd in commands:
            write(zf, f"{root}/commands/{cmd.name}", cmd.read_bytes())
        write(zf, f"{root}/skills/{NAME}/SKILL.md", read("SKILL.md"))
        write(zf, f"{root}/README.md", read("README.md"))

    print(f"{skill_path.name}  (SKILL.md)")
    print(f"{plugin_path.name}  (v{manifest['version']}, {len(commands) + 3} arquivos)")


if __name__ == "__main__":
    main()
