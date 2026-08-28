#!/usr/bin/env python3
"""Empacota um skill desta pasta como arquivo .plugin instalavel no app do Claude.

O repositorio e a fonte unica: o skill vive em 30-skills-e-prompts/<skill>/ no
layout de symlink (SKILL.md na raiz da pasta) e este script deriva dele o layout
de plugin (.claude-plugin/plugin.json + skills/<skill>/), sem duplicar conteudo.

Uso:
    ./build-plugin.py anti-slop-ptbr
    ./build-plugin.py --all
    ./build-plugin.py anti-slop-ptbr --out /tmp

Cada skill pode trazer um plugin.json opcional na propria pasta para sobrescrever
os metadados derivados (principalmente version, que precisa subir a cada release,
senao quem instalou o plugin nao tem como saber que a versao mudou):

    { "version": "0.2.0", "keywords": ["copy", "revisao"] }

Esse plugin.json fica na pasta do skill e nao entra no pacote: o script gera o
manifesto final a partir dele. Requer apenas a stdlib do Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = SKILLS_DIR / "dist"
DEFAULT_AUTHOR = "Fisher"
DEFAULT_LICENSE = "MIT"
DEFAULT_VERSION = "0.1.0"

# Arquivos e pastas que nunca entram no pacote.
EXCLUDE_NAMES = {"plugin.json", ".DS_Store"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class BuildError(Exception):
    pass


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    """Le o frontmatter YAML do SKILL.md.

    Parser deliberadamente restrito: aceita apenas `chave: valor` de uma linha,
    que e o formato que todo SKILL.md deste repositorio usa. Nao ha dependencia
    de PyYAML.
    """
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise BuildError(f"{skill_md} nao comeca com frontmatter (---)")
    end = text.find("\n---", 4)
    if end == -1:
        raise BuildError(f"{skill_md} tem frontmatter sem fechamento (---)")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or line.startswith((" ", "\t")):
            continue
        fields[key.strip()] = value.strip().strip("'\"")
    return fields


def first_sentence(text: str) -> str:
    """Primeira frase da description, para o campo curto do manifesto.

    A description do frontmatter e longa de proposito (e ela que dispara o
    skill). O manifesto do plugin quer uma linha.
    """
    match = re.search(r"^(.+?[.!?])(\s|$)", text.strip())
    return (match.group(1) if match else text.strip()).strip()


def build_manifest(skill_dir: Path, frontmatter: dict[str, str]) -> dict:
    name = skill_dir.name
    description = frontmatter.get("description", "")
    if not description:
        raise BuildError(f"{skill_dir/'SKILL.md'} nao tem `description` no frontmatter")

    manifest = {
        "name": name,
        "version": DEFAULT_VERSION,
        "description": first_sentence(description),
        "author": {"name": DEFAULT_AUTHOR},
        "license": DEFAULT_LICENSE,
        "repository": "https://github.com/FisherVB/fisher-brain",
    }

    override_path = skill_dir / "plugin.json"
    if override_path.exists():
        try:
            override = json.loads(override_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise BuildError(f"{override_path} nao e JSON valido: {exc}") from exc
        if not isinstance(override, dict):
            raise BuildError(f"{override_path} precisa conter um objeto JSON")
        override.pop("name", None)  # o nome vem sempre da pasta
        manifest.update(override)

    if not NAME_RE.match(manifest["name"]):
        raise BuildError(
            f"'{manifest['name']}' nao e kebab-case; renomeie a pasta do skill"
        )
    return manifest


def collect_files(skill_dir: Path) -> list[Path]:
    files = [
        path
        for path in sorted(skill_dir.rglob("*"))
        if path.is_file()
        and path.name not in EXCLUDE_NAMES
        and not any(part.startswith(".") or part == "dist" for part in path.relative_to(skill_dir).parts)
    ]
    if not files:
        raise BuildError(f"{skill_dir} nao tem arquivos para empacotar")
    return files


def build(skill_dir: Path, out_dir: Path) -> Path:
    if not skill_dir.is_dir():
        raise BuildError(f"{skill_dir} nao existe ou nao e uma pasta")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise BuildError(f"{skill_dir} nao tem SKILL.md")

    manifest = build_manifest(skill_dir, parse_frontmatter(skill_md))
    name = manifest["name"]
    files = collect_files(skill_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.plugin"

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            ".claude-plugin/plugin.json",
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        )
        for path in files:
            rel = path.relative_to(skill_dir)
            # README.md fica na raiz do plugin; o resto vira o corpo do skill.
            arcname = (
                "README.md" if rel.as_posix() == "README.md" else f"skills/{name}/{rel.as_posix()}"
            )
            zf.write(path, arcname)

    print(f"{out_path}  (v{manifest['version']}, {len(files) + 1} arquivos)")
    if not (skill_dir / "plugin.json").exists():
        print(
            f"  aviso: {name} nao tem plugin.json, versao fixada em {DEFAULT_VERSION}. "
            "Crie o arquivo e suba a version a cada mudanca publicada.",
            file=sys.stderr,
        )
    return out_path


def discover_skills() -> list[Path]:
    return sorted(p.parent for p in SKILLS_DIR.glob("*/SKILL.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Empacota skills de 30-skills-e-prompts como arquivos .plugin."
    )
    parser.add_argument("skills", nargs="*", help="pastas de skill (ex: anti-slop-ptbr)")
    parser.add_argument("--all", action="store_true", help="empacota todo skill com SKILL.md")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="pasta de saida (default: ./dist)")
    args = parser.parse_args()

    if args.all:
        targets = discover_skills()
        if not targets:
            print("nenhum skill com SKILL.md encontrado", file=sys.stderr)
            return 1
    elif args.skills:
        targets = [SKILLS_DIR / s if not Path(s).is_absolute() else Path(s) for s in args.skills]
    else:
        parser.print_help()
        return 2

    failures = 0
    for skill_dir in targets:
        try:
            build(Path(skill_dir).resolve(), args.out.resolve())
        except BuildError as exc:
            print(f"erro: {exc}", file=sys.stderr)
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
