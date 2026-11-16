# naming

Skill de **naming** da Fisher: nomeia marcas, produtos, empresas, startups,
features e campanhas rodando um **workshop estruturado em 11 passos** (o "Zoo
Method") — em vez de um brainstorm solto.

## O que faz

Conduz você **passo a passo, perguntando no chat** (é uma conversa, não um
relatório), pelo método:

1. **Restrições** — curto, registrável, teste do rádio/telefone, inglês se
   global, buscável.
2. **Wordbank** — banco de palavras de atributo e propósito.
3. **Tabela de Segmentação** — 12 territórios (aliteração, descritivo, inventado,
   evocativo, geografia, acrônimo, siglas, outras línguas, patronímico,
   abreviação, experiência, nome próprio).
4. **Brainstorming** — preenche a tabela usando o Wordbank.
5. **Escolher 5–7** candidatos.
6. **Matriz de Decisão** — pontua 0–3 em 10 critérios.
7. **Coffee-break** — releitura com olhos frescos.
8. **3 finalistas** — checa restrições de verdade (domínio via RDAP, Google).
9. **Votação** — formulário dos 3 (preferido / menos gosta / por quê).
10. **Escolha e regularização** — domínio + registro de marca.
11. **(Opcional) Branding.**

Roda em dois modos: **solo** (o agente propõe e confirma cada etapa) ou
**facilitador** (gera os artefatos pro time preencher no workshop).

## Quando usar

Sempre que precisar nomear algo: "como vou chamar isso?", nome de marca/produto/
empresa/app/startup, renomear um produto, achar domínio livre pra uma ideia.
Dispara mesmo sem a palavra "naming". Nomeia em português e inglês.

## Estrutura

```
naming/
├── SKILL.md                       # o workshop em 11 passos
├── plugin.json                    # metadados de release (version, keywords)
├── references/
│   ├── territorios.md             # os 12 territórios, com táticas e exemplos
│   └── matriz-e-restricoes.md     # matriz 0–3, restrições, disponibilidade, marca
└── scripts/
    ├── check_availability.py      # domínio (RDAP via IANA) + handles, stdlib
    └── decision_matrix.py         # ranqueia a Matriz de Decisão (0–3), stdlib
```

## Instalação local

Como as outras skills do repo — symlink pra `git pull` manter atualizado:

```bash
ln -s <caminho-deste-repo>/naming ~/.claude/skills/naming
```

Pra usar no app do Claude / sessões na nuvem, gere o pacote:

```bash
python3 build-plugin.py naming
```

## Os scripts, soltos

Funcionam sem dependências nem API key:

```bash
python3 scripts/check_availability.py --tld com,com.br,ai "acme" "Acme Labs"
python3 scripts/check_availability.py --tld com --handles "vero" "keel"
python3 scripts/decision_matrix.py matriz.json
```

`check_availability.py` lê disponibilidade dos servidores RDAP autoritativos (via
bootstrap do IANA), inclusive `.com.br`; ccTLDs sem RDAP (`.io`, `.co`, `.me`)
voltam **unknown** por design — confira na mão. Ressalvas no cabeçalho de cada
script e em `references/`.
