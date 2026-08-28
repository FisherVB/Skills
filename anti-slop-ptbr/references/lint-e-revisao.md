# Revisão, lint e score

> Testes de revisão, thresholds, heurística de score e pseudolint. Complementa `scripts/lint.py`, que automatiza só a parte determinística.

<!-- lint:off -->

# 14. Regras de revisão

## 14.1. Teste de especificidade

Para cada frase, perguntar:

1. Há um fato?
2. Há um mecanismo?
3. Há um exemplo?
4. Há um número?
5. Há um nome?
6. Há uma decisão?
7. Há uma consequência verificável?
8. Há uma interpretação realmente nova?

Se a resposta for não para tudo, considerar cortar ou reescrever.

---

## 14.2. Teste de compressão

Pergunta:

> Posso remover 30% desta frase sem perder significado?

Se sim, provavelmente há filler.

---

## 14.3. Teste de prova

Para adjetivos como:

- estratégico;
- eficiente;
- relevante;
- inovador;
- robusto;
- escalável;
- poderoso;

perguntar:

> Qual evidência permite usar esta palavra?

Sem evidência, remover.

---

## 14.4. Teste de estrutura

Perguntar:

- há trios demais?
- há simetria demais?
- todos os parágrafos têm o mesmo formato?
- quase todo parágrafo começa com conector?
- existem perguntas retóricas artificiais?
- o texto termina resumindo o próprio texto?
- todos os bullets começam da mesma forma?

Se sim, reestruturar.

---

# 15. Thresholds sugeridos para lint

## FAIL imediato

- pontuação proibida;
- emoji na copy;
- resíduo explícito de chatbot;
- opener ou closer exato da deny-list;
- atribuição vaga sem fonte;
- construção proibida "não é X, é Y";
- setas;
- aspas curvas;
- travessão.

## WARNING forte

- 2 ou mais palavras infladas na mesma frase;
- 4 ou mais termos da lista de slop em 150 palavras;
- 3 ou mais parágrafos começando com conectores;
- 2 ou mais caudas abstratas de gerúndio;
- 2 ou mais perguntas retóricas em texto curto;
- 2 ou mais construções "mais do que X";
- 3 ou mais fragmentos punchy consecutivos.

## REVISÃO estrutural

- 3 frases consecutivas com tamanho muito parecido;
- 3 seções consecutivas com arquitetura idêntica;
- 2 ou mais trios retóricos em texto curto;
- conclusão sem informação nova;
- bullets semanticamente redundantes;
- repetição frequente de tese + explicação + wrap-up;
- excesso de frases com abstrações sem mecanismo.

---

# 16. Heurística de score

Sugestão simples:

```text
+3 hard ban
+3 atribuição vaga
+3 estrutura "não é X, é Y"
+2 cauda de gerúndio abstrata
+2 abertura ou fecho genérico
+2 pergunta falsa + resposta
+2 metáfora gasta
+1 verbo inflado
+1 adjetivo de brochura
+1 conector serializado
+1 advérbio vazio
+1 trio retórico
```

Interpretação sugerida:

```text
0-2: ok
3-5: revisar
6-9: provável slop
10+: reescrever
```

Não usar esse score como detector de autoria por IA. Ele serve apenas como heurística editorial.

---

# 17. Pseudolint

```text
for each sentence:
    check hard_bans
    check banned_openers_and_closers
    check inflated_vocabulary
    check vague_attribution
    check binary_contrast
    check fake_question_answer
    check abstract_gerund_tail
    check semantic_density

for each paragraph:
    check connector_opening
    check repeated_structure
    check low_information_density

for full_text:
    check rhythm_uniformity
    check symmetry
    check rule_of_three_density
    check conclusion_redundancy
    check formatting_excess
```

---

# 18. Prompt de revisão anti-slop

Use como segunda passada:

```text
Revise o texto abaixo em PT-BR.

Objetivo:
remover sinais recorrentes de AI slop sem deixar o texto artificialmente seco.

Regras:

1. Corte frases que não acrescentam fato, mecanismo, exemplo, decisão, consequência ou interpretação não óbvia.
2. Remova abstrações sem evidência.
3. Troque adjetivos promocionais por informação concreta.
4. Corte conectores desnecessários.
5. Evite estruturas "não é X, é Y", "mais do que X", "vai além de X" e perguntas falsas seguidas de resposta.
6. Corte caudas de gerúndio que apenas interpretam a frase anterior.
7. Elimine atribuições vagas como "estudos mostram" sem fonte identificável.
8. Reduza trios retóricos e simetria excessiva.
9. Varie o ritmo das frases.
10. Não crie uma conclusão apenas para resumir o que já foi dito.
11. Preserve termos técnicos necessários.
12. Não troque uma palavra proibida por um sinônimo igualmente vago.
13. Priorize números, nomes, passos, mecanismos, exemplos e consequências concretas.
14. Preserve o sentido original.
```

---

# 19. Regra editorial final

Antes de aprovar um texto, perguntar:

> Este texto parece escrito para dizer algo ou para soar como texto?

Se estiver mais preocupado em soar bem do que em carregar informação, reescrever.

A meta não é "parecer humano".

A meta é:

- ser específico;
- ser útil;
- ser direto;
- ser informativo;
- variar naturalmente;
- evitar abstração sem prova;
- parar quando não há mais nada a dizer.

---

# 20. Referências úteis

Materiais que ajudam a expandir ou revisar este guia:

- Wikipedia, Signs of AI writing
- WikiProject AI Cleanup
- Pew Research, How Much of the Internet Is Written With AI?
- Stop Slop, SKILL.md
- No AI Slop, SKILL.md
- NousResearch, Anti-Slop Reference
- Structured Signs of AI Writing
- estudos acadêmicos sobre mudanças de vocabulário após a adoção de LLMs

Observação:

Essas referências servem para catalogar padrões editoriais. Nenhum desses sinais, isoladamente ou em conjunto, prova que um texto foi escrito por IA.

<!-- lint:on -->
