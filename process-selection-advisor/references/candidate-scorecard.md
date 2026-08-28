# Scorecard de Candidatos — [área / rodada / data]

## 1. Recorte de cada candidato

Uma linha por candidato. Se a frase não fechar, o candidato não está pronto.

| # | Etapa (entrada → verbo → saída → quem usa → para decidir o quê) | Vezes/semana | Min/vez | Pessoas |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## 2. Portas de elegibilidade (eliminatórias)

| # | Porta 1 — dado acessível | Porta 2 — saída verificável | Porta 3 — erro absorvível | Situação |
|---|---|---|---|---|
| 1 | | | | passa / bloqueado |
| 2 | | | | |
| 3 | | | | |

Para cada bloqueado, escreva **o que o desbloquearia** — em geral é um projeto de dado
ou de permissão, e frequentemente vale mais que a automação em si:

- Candidato __: desbloqueio = ___

## 3. Forma do trabalho e aptidão

| # | Forma predominante | Aptidão (alta / média / baixa / nenhuma) | Recorte ajustado |
|---|---|---|---|
| 1 | | | |

Se a forma for "aplicar regra e calcular", a recomendação é automação clássica, não IA.
Se for "julgar exceção", o recorte muda para o **preparo** da decisão.

## 4. Pontuação (1–5 × peso)

| Critério | Peso | Cand. 1 | Cand. 2 | Cand. 3 |
|---|---|---|---|---|
| Ganho (horas + não-feito) | 3 | | | |
| Aptidão da forma | 3 | | | |
| Acesso ao dado | 2 | | | |
| Verificabilidade | 2 | | | |
| Absorção do erro | 2 | | | |
| Dono presente | 2 | | | |
| Baixa manutenção prevista | 1 | | | |
| **Total** | | | | |

## 5. A conta (do candidato escolhido)

| Linha | Valor | Como foi estimado |
|---|---|---|
| Ganho anual em horas | | volume × tempo × custo/hora |
| Custo do não-feito | | declarado em separado, sem falsa precisão |
| Custo de construção | | pessoa × semanas + integração + liberação de acesso |
| Custo de operação/ano | | execução + manutenção (15–30% da construção) |
| **Equilíbrio (meses)** | | construção ÷ (ganho mês − operação mês) |

Solução chata que resolveria 80%: ___ — se existe, ela vence.

## 6. Pessoas

| Papel | Nome | Observação |
|---|---|---|
| Dono da etapa | | |
| Consome a saída | | o que ela vai querer conferir nos primeiros 30 dias |
| Quem perde algo | | controle / relevância / headcount — e o que ganha em troca |
| Quem constrói | | e o que deixa de fazer para isso |

## 7. Veredicto e sequência

| # | Veredicto (automatizar / assistir / redesenhar antes / não mexer) | Razão em uma linha |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

- **Primeiro caso** (o que termina em 4–6 semanas): ___
- **Segundo caso** (o ambicioso): ___
- **Na fila**, com a condição de entrada: ___

## 8. Os "não", por escrito

- Candidato __: não, porque ___
- Candidato __: não, porque ___

Um "não" bem argumentado é entregável — é o que sustenta o "sim" da próxima rodada.

## 9. Passagem de bastão

- Desenho de contexto: ___
- `eval-design`: quem é o árbitro humano da saída, e qual a fonte de verdade → ___
