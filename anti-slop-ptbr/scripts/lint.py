#!/usr/bin/env python3
"""Lint anti-slop para texto em portugues do Brasil.

Cobre a parte deterministica do guia: pontuacao proibida, deny-lists exatas,
atribuicao vaga, contraste telegrafado, e os thresholds contaveis (densidade de
conectores, fragmentos punchy, uniformidade de ritmo). O que exige julgamento
(adjetivo sem prova, gerundio que so interpreta, densidade informacional) fica
nas regras em prosa do SKILL.md; este script nao substitui a leitura.

Uso:
    python3 lint.py <<'TXT'
    o rascunho aqui
    TXT

    python3 lint.py caminho/do/arquivo.md
    python3 lint.py --only-fail arquivo.md      # so os bloqueios
    python3 lint.py --json arquivo.md           # saida estruturada

Le stdin por padrao, para nao gerar arquivo quando o texto vive numa resposta.
Sai com codigo 1 se houver qualquer FAIL, 0 caso contrario. Requer apenas a
stdlib do Python 3.8+.

Ignora bloco de codigo cercado, blockquote e code span: sem isso o proprio guia
e qualquer texto citado disparariam centenas de falsos positivos.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata

# ---------------------------------------------------------------------------
# Regras. Cada uma: (id, tier, categoria, regex, mensagem, peso)
# tier FAIL barra; WARNING sinaliza. peso alimenta o score da secao 16 do guia.
# ---------------------------------------------------------------------------

def _alt(*words: str) -> str:
    """Alternativa regex com fronteira de palavra tolerante a acento."""
    return r"(?<![\w])(?:" + "|".join(words) + r")(?![\w])"


PUNCT_RULES = [
    ("punct-travessao", "FAIL", "pontuacao", r"[—–]", "travessao (em/en dash)", 3),
    ("punct-ponto-medio", "FAIL", "pontuacao", r"·", "ponto medio", 3),
    ("punct-aspas-curvas", "FAIL", "pontuacao", r"[“”‘’]", "aspas curvas", 3),
    ("punct-reticencias", "FAIL", "pontuacao", r"…", "reticencias unicode", 3),
    ("punct-setas-uni", "FAIL", "pontuacao", r"[←-⇿⟵-⟿]", "seta unicode", 3),
    # `<=` e `>=` ficam de fora: sao comparacao, nao seta.
    ("punct-setas-ascii", "FAIL", "pontuacao", r"(?<![\w<>=-])(?:->|<-|=>)(?![\w=-])", "seta ASCII", 3),
]

CHATBOT_RULES = [
    ("chatbot-residuo", "FAIL", "residuo de chatbot", _alt(
        r"claro!", r"com certeza!", r"[oó]tima pergunta", r"excelente ponto",
        r"faz total sentido", r"aqui est[aá](?: o| a)?\b", r"vamos l[aá]!?",
        r"espero que ajude", r"se quiser,? posso", r"como modelo de i\.?a",
        r"com base nas informa[cç][oõ]es dispon[ií]veis",
    ), "residuo de chatbot", 3),
]

OPENER_RULES = [
    ("abertura-muleta", "FAIL", "abertura generica", _alt(
        r"no mundo de hoje", r"na era da i\.?a", r"na era digital",
        r"no cen[aá]rio atual", r"no contexto atual", r"nos dias de hoje",
        r"em um mundo cada vez mais", r"em um mercado cada vez mais competitivo",
        r"com o avan[cç]o da i\.?a", r"com a r[aá]pida evolu[cç][aã]o de",
        r"com a crescente ado[cç][aã]o de", r"diante desse cen[aá]rio",
        r"e se eu te dissesse", r"quando se trata de",
    ), "abertura da deny-list", 2),
]

CLOSER_RULES = [
    ("fecho-muleta", "FAIL", "fecho generico", _alt(
        r"em suma", r"em resumo", r"em conclus[aã]o", r"para concluir",
        r"em s[ií]ntese", r"ao final do dia", r"diante do exposto",
        r"em [uú]ltima an[aá]lise", r"no fim das contas", r"uma coisa [eé] certa",
        r"o futuro [eé] promissor", r"as possibilidades s[aã]o infinitas",
        r"veio para ficar", r"agora [eé] a sua vez",
    ), "fecho da deny-list", 2),
    ("fecho-engajamento", "WARNING", "fecho generico", _alt(
        r"e voc[eê]\?", r"me conta nos coment[aá]rios", r"bora conversar\?",
        r"curioso pra saber sua opini[aã]o",
    ), "fecho de engajamento formulaico", 2),
]

META_RULES = [
    ("meta-comentario", "FAIL", "meta-comentario", _alt(
        r"vale ressaltar", r"vale destacar", r"vale lembrar", r"vale observar",
        r"vale mencionar", r"cabe destacar", r"conv[eé]m lembrar",
        r"[eé] importante notar", r"[eé] importante destacar",
        r"[eé] fundamental entender", r"merece destaque",
    ), "meta-comentario sem informacao", 2),
]

ATTRIB_RULES = [
    ("atribuicao-vaga", "FAIL", "atribuicao vaga", _alt(
        r"estudos mostram", r"pesquisas indicam", r"especialistas apontam",
        r"especialistas acreditam", r"segundo especialistas",
        r"o mercado reconhece", r"observadores destacam", r"cr[ií]ticos argumentam",
        r"evid[eê]ncias sugerem", r"[eé] amplamente reconhecido", r"h[aá] consenso",
        r"l[ií]deres do setor", r"analistas afirmam",
    ), "atribuicao sem fonte identificavel", 3),
]

# Contraste telegrafado: forma explicita (ja no guia) e as variantes de enfase
# implicita levantadas na pesquisa de deny-list.
CONTRAST_RULES = [
    ("contraste-explicito", "FAIL", "contraste telegrafado",
     r"n[aã]o (?:[eé]|se trata de|se trata apenas de|[eé] s[oó]|[eé] apenas)[^.!?;]{2,60}?,\s*(?:[eé]|mas)\s",
     "construcao 'nao e X, e Y'", 3),
    ("contraste-locativo", "WARNING", "contraste telegrafado",
     r"n[aã]o est[aá] (?:em|no|na)[^.!?;]{2,60}?,\s*est[aá] (?:em|no|na)",
     "contraste locativo 'nao esta em X, esta em Y'", 3),
    ("contraste-aditivo", "WARNING", "contraste telegrafado",
     r"n[aã]o (?:com|por|de|para)\s[^.!?;]{2,50}?,\s*mas\s(?:com|por|de|para)\s",
     "contraste aditivo 'nao com X, mas com Y'", 2),
    ("mais-do-que", "WARNING", "contraste telegrafado",
     r"(?<![\w])mais do que (?:um|uma|apenas|s[oó])\b", "'mais do que X'", 2),
    ("vai-alem", "WARNING", "contraste telegrafado",
     r"(?<![\w])vai (?:muito )?al[eé]m d[aeo]", "'vai alem de'", 2),
]

# Reenquadramento sem negacao: o "nao e X, e Y" colapsado numa oracao.
REFRAME_RULES = [
    ("reenquadramento", "WARNING", "enfase implicita", _alt(
        r"o verdadeiro problema", r"o problema real", r"o verdadeiro desafio",
        r"o desafio real", r"o verdadeiro diferencial", r"o verdadeiro valor",
        r"a verdadeira quest[aã]o", r"a real quest[aã]o",
        r"a pergunta que importa", r"o verdadeiro custo", r"o custo real",
    ), "reenquadramento com oposto apenas pressuposto", 2),
]

# Anuncio de tese: setup que promete o payoff em vez de dar o ponto.
THESIS_RULES = [
    ("tese-verdade", "FAIL", "anuncio de tese",
     _alt(r"a verdade [eé] que", r"a real verdade [eé] que"),
     "'a verdade e que' e sempre removivel sem perda", 2),
    ("tese-exclusividade", "FAIL", "anuncio de tese",
     _alt(r"o que ningu[eé]m te conta", r"o que ningu[eé]m fala", r"o que ningu[eé]m conta"),
     "falsa exclusividade: o que vem depois normalmente e publico", 2),
    ("tese-revelacao", "FAIL", "anuncio de tese", _alt(
        r"[eé] a[ií] que mora o problema", r"e [eé] justamente a[ií] que",
        r"[eé] a[ií] que a coisa muda", r"[eé] a[ií] que entra",
        r"aqui est[aá] o ponto", r"a grande quest[aã]o [eé]",
    ), "setup de revelacao: comece pelo ponto", 2),
    ("tese-ponto", "WARNING", "anuncio de tese", _alt(
        r"o ponto [eé](?: que)?", r"o ponto central [eé]", r"o ponto-chave [eé]",
        r"o que importa [eé]", r"o que realmente importa [eé]",
        r"o que de fato importa [eé]", r"na pr[aá]tica,? o que importa [eé]",
        r"na pr[aá]tica,? o que acontece [eé]", r"o que est[aá] em jogo [eé]",
        r"o segredo est[aá] em", r"o segredo [eé]",
    ), "anuncio de tese: afirme direto", 2),
]

# Enfase por adjetivo de reforco. Tier WARNING sempre: 'real' e 'verdadeiro'
# sao legitimos quando o texto nomeia o termo oposto.
REINFORCE_RULES = [
    ("reforco-real", "WARNING", "reforco vazio",
     r"(?<![\w])(?:impacto|ganho|valor|problema|risco|custo|resultado|benef[ií]cio|efeito)s?\s+rea(?:l|is)(?![\w])",
     "'real' como reforco: corte se o oposto nao esta nomeado no texto", 1),
    ("reforco-verdadeiro", "WARNING", "reforco vazio",
     r"(?<![\w])verdadeir[oa]s?\s+\w+", "'verdadeiro' como reforco", 1),
    ("reforco-de-verdade", "WARNING", "reforco vazio",
     r"(?<![\w])\w+\s+de verdade(?![\w])", "'de verdade' como reforco", 1),
    ("reforco-tangivel", "WARNING", "reforco vazio",
     _alt(r"tang[ií]ve(?:l|is)"), "'tangivel': raro em PT-BR natural, frequente em copy de LLM", 1),
    ("reforco-genuino", "WARNING", "reforco vazio",
     _alt(r"genu[ií]n[oa]s?", r"genuinamente"), "'genuino' como reforco", 1),
    ("reforco-concreto", "WARNING", "reforco vazio",
     r"(?<![\w])(?:resultado|benef[ií]cio|ganho|dado|exemplo)s?\s+concret[oa]s?(?![\w])",
     "'concreto' promete a especificidade em vez de entrega-la", 1),
]

MISC_RULES = [
    ("e-sobre-abstrato", "WARNING", "enfase implicita",
     r"(?<![\w])[eé] sobre\s+(?!(?:[oa]s?|um|uma|uns|umas|seu|sua|este|esta|esse|essa|aquele|aquela|meu|minha|nosso|nossa)\s)[a-zà-ü]+(?=[\s.,;!?]|$)",
     "'e sobre' + abstrato sem artigo: metade orfa do 'nao e sobre X, e sobre Y'", 2),
    ("spoiler", "FAIL", "marcador importado",
     r"(?<![\w])(?:spoiler|plot twist)\s*:", "marcador de blog sem funcao informacional", 2),
    ("muda-o-jogo", "WARNING", "metafora gasta",
     _alt(r"muda o jogo", r"vira o jogo", r"muda tudo", r"outro n[ií]vel",
          r"game-?changer", r"divisor de [aá]guas", r"virada de chave"),
     "retorica do jogo: exija mecanismo ou metrica", 2),
    ("reformulacao", "WARNING", "redundancia",
     _alt(r"ou seja", r"em outras palavras"),
     "reformulacao: so vale se traduzir jargao, nao se repetir a abstracao", 1),
    ("pergunta-falsa", "WARNING", "pergunta falsa",
     r"(?:^|[.!?]\s)(?:o resultado|a diferen[cç]a|o segredo|o motivo|a raz[aã]o|e o melhor)\?\s",
     "pergunta falsa seguida de resposta", 2),
]

INFLATED_VERBS = [
    "mergulhe", "desvende", "eleve", "revolucione", "potencialize", "destrave",
    "alavanque", "empodere", "catalise", "ressignifique", "impulsione",
]
BROCHURE_ADJ = [
    "poderos[oa]s?", "robust[oa]s?", "incr[ií]ve(?:l|is)", "inovador(?:a|es|as)?",
    "de ponta", "transformador(?:a|es|as)?", "revolucion[aá]ri[oa]s?",
    "abrangentes?", "hol[ií]stic[oa]s?", "multifacetad[oa]s?", "disruptiv[oa]s?",
    "crucia(?:l|is)", "essencia(?:l|is)", "excepciona(?:l|is)",
]
EMPTY_ADVERBS = [
    "significativamente", "profundamente", "amplamente", "perfeitamente",
    "verdadeiramente", "realmente", "extremamente",
]
CONNECTORS = [
    "al[eé]m disso", "ademais", "adicionalmente", "nesse sentido", "dessa forma",
    "desse modo", "portanto", "contudo", "no entanto", "ainda assim",
    "consequentemente", "por conseguinte", "em contrapartida", "por outro lado",
    "assim", "por fim",
]
GERUND_TAILS = [
    "garantindo", "permitindo", "promovendo", "fortalecendo", "contribuindo",
    "refor[cç]ando", "evidenciando", "consolidando", "impulsionando",
    "proporcionando", "viabilizando",
]

LEXICAL_RULES = [
    ("verbo-inflado", "WARNING", "vocabulario inflado", _alt(*INFLATED_VERBS), "verbo inflado", 1),
    ("adjetivo-brochura", "WARNING", "vocabulario inflado", _alt(*BROCHURE_ADJ), "adjetivo de brochura", 1),
    ("adverbio-vazio", "WARNING", "vocabulario inflado", _alt(*EMPTY_ADVERBS), "adverbio vazio", 1),
    ("cauda-gerundio", "WARNING", "cauda de gerundio",
     r",\s*(?:" + "|".join(GERUND_TAILS) + r")(?![\w])",
     "cauda de gerundio: exija mecanismo, numero ou consequencia", 2),
]

ALL_RULES = (
    PUNCT_RULES + CHATBOT_RULES + OPENER_RULES + CLOSER_RULES + META_RULES
    + ATTRIB_RULES + CONTRAST_RULES + REFRAME_RULES + THESIS_RULES
    + REINFORCE_RULES + MISC_RULES + LEXICAL_RULES
)

COMPILED = [
    (rid, tier, cat, re.compile(pat, re.IGNORECASE), msg, weight)
    for rid, tier, cat, pat, msg, weight in ALL_RULES
]

# ---------------------------------------------------------------------------
# Mascaramento: bloco de codigo, blockquote e code span nao sao copy.
# Substituidos por espacos, para os numeros de linha e coluna nao mudarem.
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
CODESPAN_RE = re.compile(r"`[^`\n]*`")
OFF_RE = re.compile(r"<!--\s*lint:off\s*-->", re.IGNORECASE)
ON_RE = re.compile(r"<!--\s*lint:on\s*-->", re.IGNORECASE)


def mask(text: str) -> tuple[str, list[str]]:
    """Devolve (texto mascarado, linhas originais).

    Mascara o que nao e copy: bloco de codigo cercado, blockquote, code span, e
    regiao entre <!-- lint:off --> e <!-- lint:on -->. Os marcadores existem
    porque uma deny-list, um exemplo de "antes" e um texto de terceiro citado
    contem de proposito o que o lint barra. Sem eles, o proprio guia acusa
    centenas de falsos positivos e o time desliga a ferramenta.
    """
    original = text.splitlines()
    out = []
    in_fence = False
    lint_off = False
    for line in original:
        if OFF_RE.search(line):
            lint_off = True
            out.append(" " * len(line))
            continue
        if ON_RE.search(line):
            lint_off = False
            out.append(" " * len(line))
            continue
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(" " * len(line))
            continue
        if lint_off or in_fence or line.lstrip().startswith(">"):
            out.append(" " * len(line))
            continue
        out.append(CODESPAN_RE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out), original


def has_emoji(ch: str) -> bool:
    if unicodedata.category(ch) == "So":
        return True
    return 0x1F300 <= ord(ch) <= 0x1FAFF


# ---------------------------------------------------------------------------
# Analise
# ---------------------------------------------------------------------------

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def find_matches(masked: str, original: list[str]) -> list[dict]:
    findings = []
    offsets = []
    pos = 0
    for line in masked.splitlines():
        offsets.append(pos)
        pos += len(line) + 1

    def locate(idx: int) -> tuple[int, int]:
        lo = 0
        for i, start in enumerate(offsets):
            if start > idx:
                break
            lo = i
        return lo + 1, idx - offsets[lo] + 1

    for rid, tier, cat, rx, msg, weight in COMPILED:
        for m in rx.finditer(masked):
            line_no, col = locate(m.start())
            findings.append({
                "id": rid, "tier": tier, "categoria": cat, "mensagem": msg,
                "peso": weight, "linha": line_no, "coluna": col,
                "trecho": m.group(0).strip()[:70],
                "contexto": original[line_no - 1].strip()[:110] if line_no <= len(original) else "",
            })

    for line_no, line in enumerate(masked.splitlines(), 1):
        for col, ch in enumerate(line, 1):
            if has_emoji(ch):
                findings.append({
                    "id": "punct-emoji", "tier": "FAIL", "categoria": "pontuacao",
                    "mensagem": "emoji na copy", "peso": 3, "linha": line_no,
                    "coluna": col, "trecho": ch,
                    "contexto": original[line_no - 1].strip()[:110],
                })
    return findings


def structural_checks(masked: str) -> list[dict]:
    """Thresholds contaveis da secao 15 do guia."""
    out = []
    paragraphs = [p for p in re.split(r"\n\s*\n", masked) if p.strip()]

    conn_rx = re.compile(r"^\s*(?:" + "|".join(CONNECTORS) + r")\b", re.IGNORECASE)
    conn_starts = sum(1 for p in paragraphs if conn_rx.match(p))
    if conn_starts >= 3:
        out.append({
            "id": "estrutura-conectores", "tier": "WARNING", "categoria": "ritmo",
            "mensagem": f"{conn_starts} paragrafos comecam com conector", "peso": 1,
            "linha": 0, "coluna": 0, "trecho": "", "contexto": "",
        })

    sentences = [s.strip() for s in SENT_SPLIT.split(masked) if s.strip()]

    frag_run = 0
    for s in sentences:
        words = len(s.split())
        if words <= 5 and not re.search(r"\d", s):
            frag_run += 1
            if frag_run == 3:
                out.append({
                    "id": "estrutura-fragmentos", "tier": "WARNING", "categoria": "ritmo",
                    "mensagem": "3 ou mais fragmentos punchy consecutivos sem informacao",
                    "peso": 1, "linha": 0, "coluna": 0, "trecho": s[:60], "contexto": "",
                })
        else:
            frag_run = 0

    lengths = [len(s.split()) for s in sentences]
    for i in range(len(lengths) - 2):
        window = lengths[i:i + 3]
        if min(window) >= 8 and max(window) - min(window) <= 2:
            out.append({
                "id": "estrutura-ritmo", "tier": "WARNING", "categoria": "ritmo",
                "mensagem": f"3 frases consecutivas de tamanho muito parecido ({window})",
                "peso": 1, "linha": 0, "coluna": 0, "trecho": "", "contexto": "",
            })
            break

    questions = masked.count("?")
    if questions >= 2 and len(masked.split()) < 300:
        out.append({
            "id": "estrutura-perguntas", "tier": "WARNING", "categoria": "ritmo",
            "mensagem": f"{questions} perguntas em texto curto", "peso": 1,
            "linha": 0, "coluna": 0, "trecho": "", "contexto": "",
        })
    return out


MIN_WORDS_TO_NORMALIZE = 120


def score(findings: list[dict], words: int) -> dict:
    raw = sum(f["peso"] for f in findings)
    # A secao 16 do guia fixa faixas (0-2 ok ... 10+ reescrever) sem normalizar
    # por tamanho. Sem normalizar, qualquer texto longo estoura; normalizando
    # sempre, um paragrafo de 30 palavras com um achado vira "reescrever".
    # Abaixo de MIN_WORDS_TO_NORMALIZE usa o score bruto, acima usa por 300.
    per300 = raw * 300 / max(words, 1)
    basis = raw if words < MIN_WORDS_TO_NORMALIZE else per300
    if basis <= 2:
        verdict = "ok"
    elif basis <= 5:
        verdict = "revisar"
    elif basis <= 9:
        verdict = "provavel slop"
    else:
        verdict = "reescrever"
    return {"bruto": raw, "por_300_palavras": round(per300, 1),
            "palavras": words, "base": "bruto" if words < MIN_WORDS_TO_NORMALIZE else "por_300",
            "veredicto": verdict}


# ---------------------------------------------------------------------------
# Saida
# ---------------------------------------------------------------------------

def report(findings: list[dict], sc: dict, only_fail: bool) -> str:
    fails = [f for f in findings if f["tier"] == "FAIL"]
    warns = [f for f in findings if f["tier"] == "WARNING"]
    lines = []

    def block(title: str, items: list[dict]) -> None:
        if not items:
            return
        lines.append(f"\n{title} ({len(items)})")
        for f in sorted(items, key=lambda x: (x["linha"], x["coluna"])):
            loc = f"L{f['linha']}:{f['coluna']}" if f["linha"] else "texto"
            trecho = f' "{f["trecho"]}"' if f["trecho"] else ""
            lines.append(f"  {loc:>10}  [{f['id']}]{trecho}")
            lines.append(f"              {f['mensagem']}")

    block("FAIL", fails)
    if not only_fail:
        block("WARNING", warns)

    base = "score bruto" if sc["base"] == "bruto" else "score por 300 palavras"
    lines.append(
        f"\nscore {sc['bruto']} bruto, {sc['por_300_palavras']} por 300 palavras "
        f"({sc['palavras']} palavras): {sc['veredicto']}, por {base}"
    )
    if not fails and not warns:
        lines.append("nenhuma marca deterministica encontrada")
    lines.append(
        "\nO lint cobre so a parte deterministica. Densidade informacional, "
        "adjetivo sem prova e simetria estrutural continuam exigindo leitura."
    )
    return "\n".join(lines).lstrip("\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint anti-slop para PT-BR.")
    ap.add_argument("path", nargs="?", default="-", help="arquivo (default: stdin)")
    ap.add_argument("--only-fail", action="store_true", help="mostra apenas os bloqueios")
    ap.add_argument("--json", action="store_true", help="saida estruturada")
    args = ap.parse_args()

    if args.path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"erro: {exc}", file=sys.stderr)
            return 2

    if not text.strip():
        print("erro: nenhum texto recebido (passe um arquivo ou escreva no stdin)", file=sys.stderr)
        return 2

    masked, original = mask(text)
    findings = find_matches(masked, original) + structural_checks(masked)
    sc = score(findings, len(masked.split()))

    if args.json:
        print(json.dumps({"score": sc, "achados": findings}, ensure_ascii=False, indent=2))
    else:
        print(report(findings, sc, args.only_fail))

    return 1 if any(f["tier"] == "FAIL" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
