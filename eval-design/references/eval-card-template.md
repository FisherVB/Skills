# Eval Card — [nome do fluxo]

Uma página. Se não couber, o escopo do eval está grande demais.

| Campo | Conteúdo |
|---|---|
| **Fluxo avaliado** | O que entra, o que o agente faz, o que sai |
| **Estágio** | Protótipo / Piloto / Produção |
| **Decisão que este eval sustenta** | "Medimos para decidir ___; sem isso decidiríamos por ___" |
| **Unidade avaliada** | Resposta inteira / campo / ação / etapa N da cadeia |
| **Árbitro humano** | Nome e papel |
| **Erro que dói mais** | Falso positivo ou falso negativo, e por quê |
| **Reversibilidade** | O erro é desfeito como? |
| **Right-sizing** | Light / Standard / Heavy |
| **Dono do eval** | Nome |
| **Última revisão** | Data + o que mudou |

## Rubrica

| # | Critério (observável) | Aprovado se | Reprovado se |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Abstenção conta como acerto quando: ___

## Golden Dataset

| Fatia | Nº de casos | Origem | Linha de corte |
|---|---|---|---|
| Típico | | | ≥ __% |
| Borda | | | ≥ __% |
| Adversarial | | | ≥ __% |
| Regressão vivida | | histórico de erros reais | 100% |

Conjunto cego congelado: __ casos, aberto apenas em ___.

## Método de julgamento

| Critério | Nível (1 determinístico / 2 rubrica auto / 3 LLM-judge / 4 humano) | Justificativa |
|---|---|---|
| | | |

Se usa LLM-as-judge — concordância com o árbitro humano: __% em __ casos, medida em
__/__/____. Recalibrar a cada troca de modelo do juiz.

## Gate e operação

- **Roda quando:** todo deploy / semanalmente / troca de modelo, dado ou fornecedor
- **Quem segura o rollout:** ___
- **Reprovou → rota de falha:** ___
- **Amostragem em produção:** __% das execuções, revisadas por ___
- **Canal de contestação do usuário:** ___

## O que NÃO está medido

- 
- 
- 

Escrever isto por extenso é o item que mais protege quem assina o rollout.
