# eval-design

> Desenha o sistema de avaliação de um fluxo com IA antes de ele ir para produção. O eval é a especificação do produto escrita de trás para frente.

## O que faz

Conduz um diagnóstico guiado de 6 perguntas que:

1. Amarra o eval a uma **decisão** ("medimos para decidir subir/segurar; sem isso decidiríamos por impressão de quem").
2. Define **o que conta como certo**: unidade avaliada, árbitro humano com nome, rubrica com critérios observáveis.
3. Separa a **assimetria do erro** (falso positivo × falso negativo) e a reversibilidade.
4. Monta o **Golden Dataset** — 40% típico, 30% borda, 15% adversarial, 15% regressão vivida — com conjunto cego congelado.
5. Escolhe o **método mais barato que ainda decide**: verificação determinística → rubrica automática → LLM-as-judge (com calibração medida) → revisão humana.
6. Fixa a **linha de corte por fatia** e o gate: quem segura o rollout, e o que acontece quando reprova.

Saída: Eval Card de uma página (`references/eval-card-template.md`), Golden Dataset v1, plano de regressão e a lista explícita do que **não** está medido.

## Quando usar

- O fluxo vai sair do piloto e alguém precisa assinar embaixo.
- A qualidade é avaliada por impressão ("achei que ficou bom").
- Vai haver troca de modelo, prompt, base de dados ou fornecedor.
- Um agente orquestrado tem várias etapas e ninguém sabe qual delas erra.

**Não use** para uso pessoal sem consequência de erro, para fluxo que ainda não existe, ou quando o problema é acesso a dado e não qualidade de resposta.

## Exemplo de invocação

```
/eval-design
```

Ou em linguagem natural:

> O agente que classifica os e-mails do SAC está pronto. Como eu sei que ele está certo antes de desligar a conferência humana?

> Quero trocar o modelo do fluxo de extração. Como sei se piorou?

## Encadeamento

Vem depois de [`process-selection-advisor`](../process-selection-advisor/) (que já identifica o árbitro humano e a fonte de verdade) e antes de qualquer decisão de rollout.
