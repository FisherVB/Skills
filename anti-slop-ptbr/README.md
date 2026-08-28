# anti-slop-ptbr

> Revisão editorial de texto em português do Brasil: tira as marcas recorrentes de escrita gerada por IA e exige especificidade no lugar delas.

## O que faz

Aciona quando você escreve ou pede revisão de texto em PT-BR e aplica um conjunto de
regras contra os sinais recorrentes de AI slop: vocabulário inflado, trios retóricos,
caudas de gerúndio abstratas, atribuição vaga, simetria excessiva, conclusões que só
resumem o texto e baixa densidade informacional.

O princípio que organiza o resto: cluster de sinais vale mais que palavra individual, e
toda frase precisa fazer pelo menos um trabalho verificável (fato, mecanismo, número,
nome, decisão, consequência ou interpretação não óbvia).

## Quando usar

- Antes de publicar copy, artigo, post, newsletter, landing page, release ou e-mail.
- Ao receber um texto que "parece escrito por IA" e você não sabe apontar onde.
- Como segunda passada em rascunho próprio, para cortar o que não carrega informação.

Não use como detector de autoria. O score é heurística editorial, não prova de que um
texto foi gerado por IA.

## Exemplo de invocação

```
revise esse texto com o anti-slop:

"Em um mercado cada vez mais competitivo, nossa plataforma robusta centraliza os dados,
garantindo maior eficiência e promovendo decisões mais estratégicas. Estudos mostram que
empresas de todos os portes se beneficiam. Pronto para transformar sua operação?"
```

Retorno esperado: o texto reescrito com mecanismo e número no lugar das abstrações, mais
a lista dos cortes com o motivo de cada um (abertura de muleta, adjetivo sem prova,
cauda de gerúndio, atribuição vaga, universalização, CTA slop).

## Estrutura

```
anti-slop-ptbr/
|-- SKILL.md                      princípio central, barreiras de FAIL, estruturas a desmontar
|-- plugin.json                   metadados de release lidos pelo build-plugin.py
|-- scripts/
|   `-- lint.py                   passada determinística: pontuação, deny-lists, thresholds
`-- references/
    |-- listas-proibidas.md       deny-lists de pontuação, vocabulário, ênfase implícita, reforço vazio
    |-- tells-estruturais.md      catálogo de tells com exemplos de reescrita
    `-- lint-e-revisao.md         testes de revisão, thresholds, score, pseudolint
```

O corpo do `SKILL.md` fica enxuto de propósito. As listas completas e o roteiro de lint
são carregados sob demanda, quando a revisão realmente precisa deles.

## Lint

O que é determinístico não deveria depender de atenção. `scripts/lint.py` cobre pontuação
proibida, deny-lists exatas, atribuição vaga, contraste telegrafado e os thresholds
contáveis. Lê stdin, então não gera arquivo quando o texto vive numa resposta:

```bash
python3 scripts/lint.py <<'TXT'
o rascunho aqui
TXT
```

FAIL sai com código 1; WARNING imprime e exige julgamento. Aceita caminho de arquivo,
`--only-fail` e `--json`. Regiões entre `<!-- lint:off -->` e `<!-- lint:on -->` são
ignoradas, para citar texto de terceiro ou escrever exemplo de "antes".

O lint não cobre tudo, e a divisão é o desenho: o determinístico vai para o script, o
contextual fica nas regras em prosa. `real` e `verdadeiro` só são vazios quando remover o
adjetivo não muda o sentido, e isso é julgamento, não string. Em chat sem shell o skill
funciona igual, só sem a verificação automática.

## Instalação

Duas rotas, mesma fonte:

- **Claude Code**, por symlink, que pega `git pull` na hora:

  ```bash
  ln -s ~/Developer/fisher-brain/30-skills-e-prompts/anti-slop-ptbr ~/.claude/skills/anti-slop-ptbr
  ```

- **App do Claude**, por pacote, para quem não tem o repositório clonado:

  ```bash
  cd 30-skills-e-prompts && python3 build-plugin.py anti-slop-ptbr
  ```

  Depois abra `dist/anti-slop-ptbr.plugin` no app. É um snapshot: ao mudar o skill, suba
  a `version` no `plugin.json` e redistribua.

## Licença

MIT
