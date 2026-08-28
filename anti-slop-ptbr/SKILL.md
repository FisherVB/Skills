---
name: anti-slop-ptbr
description: Revisa, reescreve e audita textos em português do Brasil para remover marcas recorrentes de escrita gerada por IA (AI slop). Use quando o usuário pedir para revisar, editar, "despiorar", tirar cara de IA, limpar slop, avaliar ou pontuar um texto em PT-BR, e também antes de entregar qualquer copy, artigo, post, newsletter, landing page, e-mail, roteiro, release ou documento redigido em português do Brasil. Acione com frases como "revise esse texto", "tira o tom de IA", "isso parece escrito por IA", "deixa mais natural", "anti-slop", "escreva um post em PT-BR".
---

# Anti-Slop PT-BR

Guia operacional para produzir e revisar texto em português do Brasil com alta densidade informacional, sem as marcas previsíveis de escrita gerada por IA.

## Quando aplicar

Aplique em dois momentos:

1. Ao escrever qualquer texto em PT-BR destinado a leitores (copy, artigo, post, e-mail, documento). Escreva já dentro das regras, não depois.
2. Ao revisar texto existente. Rode a passada de auditoria e reporte o que foi cortado e por quê.

## Princípio central

Nenhuma palavra isolada prova slop. O sinal é a combinação de vocabulário inflado, estrutura previsível, simetria excessiva, entusiasmo genérico, atribuição vaga e baixa densidade informacional.

Regra: cluster de sinais vale mais que palavra individual. Não troque um termo proibido por um sinônimo igualmente vago.

## Regra de densidade

Toda frase precisa fazer pelo menos um trabalho verificável: acrescentar fato, mecanismo, exemplo, número, nome, decisão, consequência ou interpretação não óbvia.

Se a frase pode sair sem perda de informação, corte.

## Passada determinística: o lint

`scripts/lint.py` cobre a parte que não deveria depender de atenção: pontuação proibida, deny-lists exatas, atribuição vaga, contraste telegrafado e os thresholds contáveis. Ele lê stdin, então **não gera arquivo** quando o texto vive numa resposta:

```bash
python3 scripts/lint.py <<'TXT'
o rascunho aqui
TXT
```

Se o texto já é um arquivo, passe o caminho: `python3 scripts/lint.py rascunho.md`.

Quando rodar, e a regra escala com o tamanho da entrega:

- **Sem shell disponível**: não rode. Use as regras em prosa deste arquivo. Nada se perde além da verificação automática.
- **Com shell, resposta curta de conversa**: não rode. Uma chamada de ferramenta não se paga para três frases.
- **Entrega para leitor** (copy, artigo, documento, release, landing page): rode antes de entregar. É onde o erro custa.

Saída: FAIL sai com código 1 e barra a entrega; WARNING imprime e exige julgamento. O score reporta bruto e normalizado por 300 palavras, e usa o bruto abaixo de 120 palavras.

Regiões entre `<!-- lint:off -->` e `<!-- lint:on -->` são ignoradas. Use ao citar texto de terceiro ou ao escrever um exemplo de "antes".

O lint não substitui a leitura. Densidade informacional, adjetivo sem prova, gerúndio que apenas interpreta e simetria estrutural continuam exigindo julgamento.

## Barreiras diretas (FAIL)

Barre sempre, sem discussão:

<!-- lint:off -->

- travessão (em dash e en dash), ponto médio, aspas curvas, reticências unicode, setas (unicode ou ASCII), emoji na copy. Use vírgula, dois-pontos, parênteses, ponto, hífen.
- resíduo de chatbot: "Claro!", "Ótima pergunta", "Aqui está", "Espero que ajude", "Como modelo de IA".
- aberturas de muleta: "No mundo de hoje", "Cada vez mais", "Na era da IA", "Nesse contexto", "Diante desse cenário".
- fechos de muleta: "Em suma", "Em conclusão", "No fim das contas", "As possibilidades são infinitas", "veio para ficar".
- meta-comentário vazio: "Vale ressaltar", "É importante notar", "Cabe destacar".
- atribuição vaga sem fonte: "estudos mostram", "especialistas apontam", "o mercado reconhece".
- contraste telegrafado: "não é X, é Y", "mais do que X", "vai além de", pergunta falsa seguida de resposta ("O resultado? Mais eficiência.").
- anúncio de tese: "a verdade é que", "o que ninguém te conta é", "é aí que mora o problema".
- marcador importado de blog: "Spoiler:", "Plot twist:".

<!-- lint:on -->

As listas completas estão em `references/listas-proibidas.md`.

## Ênfase implícita

O contraste telegrafado tem variantes sem negação explícita, que fazem o mesmo trabalho retórico e escapam da regra acima. Pressupõem um X falso que nunca é nomeado:

<!-- lint:off -->

- reenquadramento: "o verdadeiro problema é", "a real questão é", "o custo real de", "o risco não está em X, está em Y".
- anúncio de tese em tom mais fraco: "o ponto é", "o que realmente importa é", "o que está em jogo é", "o segredo está em".
- contraste por concessão: "não com X, mas com Y", "na teoria X, na prática Y".
- metade órfã do "é sobre": "liderança é sobre confiança". Sem artigo e sem qualificador, a frase não pode ser medida nem falsificada.

<!-- lint:on -->

## Reforço vazio

`real`, `verdadeiro`, `de verdade`, `tangível`, `genuíno` e `concreto` normalmente substituem informação por ênfase. A regra é contextual, não de string:

> Flag apenas quando remover o adjetivo não altera o significado da frase.

Se o texto nomeia o termo oposto, o adjetivo carrega informação e passa.

<!-- lint:off -->

"O orçamento previa R$ 1,2 milhão; o custo real ficou em R$ 1,7 milhão" usa `real` com função, porque o projetado está no texto. "Ganho real" sem oposto nomeado é ênfase, corte.

<!-- lint:on -->

Nunca trate este eixo como FAIL. `o verdadeiro diferencial` é clichê da imprensa de negócios brasileira anterior aos LLMs: a IA amplifica, não inventou.

## Estruturas a desmontar

- Trio retórico com quase-sinônimos ("rápido, confiável e eficiente"). Reduza quando os itens não forem semanticamente distintos.
- Cauda de gerúndio abstrata: fato concreto, vírgula, gerúndio que só interpreta o fato. Exija mecanismo, número, etapa ou consequência, ou corte a oração.
- Simetria suspeita: sempre três benefícios, blocos do mesmo tamanho, todos os bullets com a mesma construção. Deixe a estrutura ficar irregular quando o conteúdo pedir.
- Conclusão que apenas resume o texto. Feche com informação nova ou pare antes.
- Faixa falsa e universalização ("de startups a grandes corporações", "empresas de todos os portes"). Nomeie o ICP real.
- Fragmentos punchy empilhados e slogan binário. Exija métrica ou mecanismo.

Catálogo completo, com exemplos de reescrita, em `references/tells-estruturais.md`.

## Ritmo e formatação

Varie tamanho e construção das frases. Sinalize três ou mais frases consecutivas com tamanho e sintaxe muito parecidos.

Não simule organização com formatação. Se o destino do texto não pede Markdown, não use headings, negrito espalhado, separadores nem tabelas decorativas.

## Passada de auditoria

Para revisar um texto, siga o roteiro de `references/lint-e-revisao.md`, que traz os quatro testes de revisão (especificidade, compressão, prova, estrutura), os thresholds, a heurística de score, o pseudolint e o prompt de segunda passada.

Regra de agregação para os eixos de ênfase implícita e reforço vazio: três ou mais ocorrências no mesmo parágrafo elevam para revisão obrigatória. Uma ocorrência isolada é observação, não erro.

Ao reportar, entregue o texto revisado primeiro. Depois liste os cortes principais com o motivo em uma linha cada. Não trate o score como detector de autoria por IA: ele é heurística editorial.

## Limite

O objetivo não é parecer humano nem produzir texto artificialmente seco. É ser específico, útil, direto, informativo, variar naturalmente, evitar abstração sem prova e parar quando não houver mais nada a dizer.

Preserve termos técnicos necessários e o sentido original do autor.
