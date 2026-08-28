# process-selection-advisor

> Escolhe qual etapa vale automatizar com agentes — e qual não vale — antes de qualquer construção. Devolve um veredicto entre automatizar, assistir, redesenhar antes ou não mexer.

## O que faz

Conduz um diagnóstico guiado de 7 perguntas que:

1. Força o recorte da **etapa** (não do processo) em uma frase com verbo, com volume real.
2. Aplica **três portas eliminatórias**: dado acessível, saída verificável, erro absorvível.
3. Classifica a **forma do trabalho** (ler e extrair, classificar, redigir, calcular, negociar, julgar) — a forma prevê o resultado melhor que o setor.
4. Testa se o processo atual **merece ser preservado** (automatizar desperdício produz desperdício mais rápido).
5. Fecha a **conta** — ganho em horas, custo do não-feito, construção, manutenção anual, ponto de equilíbrio.
6. Nomeia **dono, consumidor da saída e quem perde algo**.
7. Emite o **veredicto** e a sequência: o primeiro caso do time é o que *termina*, não o de maior ganho.

Saída: Scorecard de candidatos (`references/candidate-scorecard.md`), recorte da etapa, conta em três linhas, sequência recomendada e a lista de "não" com motivo escrito.

## Quando usar

- Há mais ideias de automação do que capacidade de execução.
- A conversa começou com "vamos usar IA em [área]" — área não é processo.
- Um piloto rodou, funcionou tecnicamente e ninguém sentiu diferença.
- O squad de IA precisa de uma fila defensável.

**Não use** quando a etapa e o veredicto já estão acordados, quando o problema é de integração sem ninguém propondo IA, ou quando o processo vai mudar estruturalmente nos próximos 90 dias.

## Exemplo de invocação

```
/process-selection-advisor
```

Ou em linguagem natural:

> Temos seis ideias de automação na logística e capacidade para uma. Me ajuda a escolher.

> A diretoria pediu "IA no comercial". Preciso transformar isso em escopo antes da próxima reunião.

## Encadeamento

Veredicto "automatizar" ou "assistir" → desenho de contexto → [`eval-design`](../eval-design/). O bloco 9 do scorecard já entrega o árbitro humano e a fonte de verdade que o `eval-design` pede.
