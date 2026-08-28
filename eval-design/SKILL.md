---
name: eval-design
description: >-
  Desenha o sistema de avaliação (eval) de um fluxo com IA ou agentes antes de
  colocá-lo em produção. Conduz um diagnóstico guiado para definir qual decisão o
  eval sustenta, o que conta como resposta certa, o custo assimétrico do erro, o
  Golden Dataset, o método de julgamento mais barato que ainda decide, e a linha de
  corte que libera ou segura o rollout. Entrega um Eval Card, o dataset inicial e o
  plano de regressão. Use quando alguém disser que o piloto "está funcionando bem"
  sem número que sustente, quando for decidir se um agente sai do piloto para
  produção, quando trocar de modelo ou de prompt e precisar saber se piorou, quando
  um fluxo com IA já em produção começar a errar sem que ninguém saiba dizer quanto,
  ou quando as palavras eval, avaliação, golden dataset, LLM-as-judge, regressão,
  acurácia, alucinação, teste de agente ou "como eu meço isso" aparecerem.
---

# Eval Design — como saber se o agente está certo antes que o cliente descubra

## Modos de uso

Comece perguntando ao usuário como quer trabalhar:

1. **Guiado** — uma pergunta por vez, ~15 minutos.
2. **Despejo de contexto** — o usuário cola o que já tem (prompt, exemplos, print de
   erro) e você pula o que já estiver respondido.
3. **Melhor palpite** — você assume o razoável, marca cada suposição com `[suposto]`
   e segue; o usuário corrige no fim.

Não avance sem essa escolha. Em qualquer modo, sinalize progresso ("Eval 3/6").

## Input

Em linguagem natural, o que ajuda:

- Qual é o fluxo (o que entra, o que o agente faz, o que sai, quem consome).
- Em que estágio está: ideia, piloto, produção.
- O que já deu errado, com exemplo concreto.
- Quem hoje diria se uma saída está certa ou errada.
- Volume: quantas execuções por dia/semana.

Nada disso é obrigatório para começar. Falta de informação vira pergunta.

## Quando usar

✅ **Use quando:**

- O fluxo vai sair do piloto e alguém precisa assinar embaixo.
- A qualidade é avaliada por impressão ("achei que ficou bom") e não por medida.
- Há troca prevista de modelo, prompt, base de dados ou fornecedor.
- O erro tem custo real: dinheiro, cliente, contrato, segurança, reputação.
- Um agente orquestrado tem várias etapas e ninguém sabe qual delas erra.

❌ **Não use quando:**

- É uso pessoal, uma vez, sem consequência de erro (escrever um e-mail).
- O fluxo ainda nem existe — desenhe o fluxo primeiro, o eval vem junto do desenho.
- O problema é acesso a dado ou permissão, não qualidade da resposta.
- O que se quer é benchmark de modelo do mercado; isso é escolha de fornecedor, não
  eval do seu caso.

## A tese

**O eval é a especificação do produto escrita de trás para frente.** Enquanto
ninguém consegue dizer o que é uma resposta certa, não existe requisito — existe
expectativa. E expectativa não passa em auditoria, não sobrevive a troca de modelo e
não resolve discussão entre duas áreas.

Três consequências práticas:

- **Escrever o eval quase sempre melhora o prompt.** A dificuldade de definir "certo"
  revela que o pedido estava ambíguo desde o começo.
- **Sem eval, toda mudança é aposta.** Trocar o modelo por um mais novo é um upgrade
  que você não consegue provar — e uma regressão que você não consegue detectar.
- **Eval não é teste de software.** Software determinístico tem certo e errado; saída
  de modelo tem faixa aceitável. Você não busca 100%, busca **linha de corte
  defensável e estável ao longo do tempo**.

## A escada de decisão (6 perguntas)

Uma pergunta por turno. Cada resposta muda as seguintes — não dispare o questionário
inteiro de uma vez.

### Q1 — Qual decisão este eval sustenta?

Complete a frase: *"Vou medir isto para decidir **[subir / segurar / reverter /
escolher entre A e B]**, e sem esse número eu decidiria por **[impressão de quem]**."*

Se não fechar a frase, o eval vira relatório bonito que ninguém lê. Elimine a métrica.

Recusa comum: "quero medir a qualidade geral". Não existe. Existe *qualidade para
liberar o rollout*, *qualidade para justificar o custo*, *qualidade para não violar
uma norma*. Cada uma pede um corte diferente.

### Q2 — O que conta como certo, e quem julga?

Três coisas, nesta ordem:

1. **A unidade avaliada.** Uma resposta inteira? Um campo extraído? Uma ação tomada?
   Um agente numa cadeia de cinco? Avaliar "a saída final" de um fluxo orquestrado
   esconde qual etapa quebrou.
2. **O árbitro humano.** Nome, não área. Se duas pessoas discordam sobre a mesma
   saída, o eval mede a discordância delas, não o modelo.
3. **A rubrica.** Critérios observáveis, com exemplo de aprovado e de reprovado lado
   a lado. "Tom adequado" não é critério; "não promete prazo que não está na tabela"
   é.

Teste da rubrica: entregue-a a alguém que não participou da conversa. Se essa pessoa
classificar 10 saídas igual ao árbitro, a rubrica existe. Se não, o que você tem é
gosto pessoal.

### Q3 — Qual erro dói mais?

Quase nunca os dois erros custam igual. Separe:

- **Falso positivo** — o agente age/afirma quando não deveria. Nota errada emitida,
  crédito liberado, promessa feita ao cliente.
- **Falso negativo** — o agente deixa de agir/afirmar quando deveria. Caso escapa,
  fraude passa, oportunidade morre.

A assimetria define **onde fica a linha de corte e onde entra o humano**. Fluxo em
que o falso positivo custa caro pede agente conservador, com abstenção explícita
("não sei" é uma resposta válida e deve ser medida como acerto quando cabível).

Pergunte também: **o erro é reversível?** Rascunho revisado por gente e transferência
bancária executada não pertencem ao mesmo regime de eval.

### Q4 — De onde vêm os casos?

O **Golden Dataset** é o conjunto de casos com resposta de referência. Sem ele não
existe eval, existe anedota.

Composição — proporções que funcionam na prática:

| Fatia | Peso | O que é |
|---|---|---|
| Caso típico | ~40% | O dia a dia. Se falhar aqui, nem discuta o resto |
| Borda | ~30% | Formato estranho, dado faltando, ambiguidade legítima |
| Adversarial | ~15% | Pedido fora de escopo, tentativa de burlar, dado envenenado |
| Regressão vivida | ~15% | Todo erro real já visto entra aqui **e nunca sai** |

Tamanho: **20 casos** para decidir sobre um protótipo, **40–60** para liberar
produção, **100+** quando o erro tem custo regulatório ou financeiro direto. Poucos
casos bem escolhidos batem mil casos coletados no automático.

Regra de higiene: os casos vêm de **histórico real amostrado**, não da memória de
quem construiu o fluxo. Quem escreve o prompt não escolhe sozinho os casos — é
cherry-pick involuntário, e o eval passa a medir o quanto o autor conhece a própria
solução.

Congele uma fatia como **conjunto cego**, que ninguém olha ao ajustar o prompt. É a
única defesa contra otimizar para a prova.

### Q5 — Qual o método mais barato que ainda decide?

Suba a escada só até onde a decisão exige. Cada degrau custa mais e demora mais:

| Nível | Método | Bom para | Custo |
|---|---|---|---|
| 1 | **Verificação determinística** — formato, schema, faixa, presença de campo, número bate com a fonte | Extração, cálculo, classificação, chamada de ferramenta | Centavos |
| 2 | **Rubrica automática** — regras sobre o conteúdo (citou fonte? ficou no escopo? recusou quando devia?) | Resposta estruturada | Baixo |
| 3 | **LLM-as-judge** — modelo avalia contra rubrica escrita | Texto aberto, tom, aderência a política | Médio |
| 4 | **Revisão humana** — o árbitro do Q2 | Calibração, casos limítrofes, auditoria | Alto |

Erro clássico é começar no nível 3. Metade dos evals que as pessoas acham que
precisam de LLM-as-judge é resolvida no nível 1: **se existe uma fonte da verdade,
compare com ela em vez de pedir opinião a um modelo.**

**Calibrar o LLM-as-judge, quando usar:** pegue ~20 casos, faça o humano e o juiz
avaliarem os mesmos itens em cego, meça a concordância. Abaixo de ~80%, o juiz não
está pronto — conserte a rubrica, não o modelo. Repita a calibração a cada troca de
modelo do juiz. Um juiz não calibrado é pior que nenhum: dá número, e número
convence.

Cuidados conhecidos do juiz-modelo: tende a preferir resposta longa, a favorecer
texto do mesmo modelo que a gerou e a ser sensível à ordem quando compara duas
opções — alterne a ordem e mantenha as respostas com tamanho comparável.

### Q6 — Qual a linha de corte, e o que acontece quando não passa?

Um eval sem consequência é dashboard. Defina:

- **Linha de corte por fatia**, não só a média. Típico ≥ 95% e adversarial ≥ 90% é
  uma exigência; "média 93%" esconde que o fluxo falha justamente onde dói.
- **Gate** — quem/o quê segura o rollout. Idealmente automático no deploy; se for
  humano, com nome e prazo.
- **Rota de falha** — reprovou, e agora? Volta pro prompt, entra revisão humana no
  meio, ou o caso é redirecionado para atendimento?
- **Cadência** — todo deploy, semanal, e obrigatoriamente a cada troca de modelo,
  base de dados ou fornecedor.

## Right-sizing

Ofereça e registre a escolha:

- **Light (1–2h)** — 20 casos, níveis 1–2, uma linha de corte, planilha. Para
  protótipo e para convencer alguém a investir.
- **Standard (1–2 dias)** — 40–60 casos com conjunto cego, níveis 1–3 com juiz
  calibrado, cortes por fatia, roda no deploy. **Padrão para qualquer coisa que toque
  cliente ou dinheiro.**
- **Heavy (1–2 semanas)** — 100+ casos, eval por etapa da cadeia de agentes, amostragem
  contínua em produção, painel de deriva, revisão humana periódica agendada. Para
  fluxo regulado, irreversível ou de alto volume.

Na dúvida, comece Light e suba. Eval que não roda vale zero, por mais completo que
seja no papel.

## Saídas

Ao final, entregue nesta ordem:

1. **Eval Card** (uma página) — use `references/eval-card-template.md`.
2. **Golden Dataset v1** — tabela com id, entrada, saída de referência, fatia, origem
   do caso, quem validou.
3. **Plano de regressão** — quando roda, quem olha, quem tem o poder de segurar.
4. **O que ainda não está medido** — lista explícita. É o item mais honesto do
   entregável e o que mais protege quem assina.

## Depois de produção

O eval não termina no rollout:

- **Amostragem contínua** — sorteie de 1% a 5% das execuções reais para revisão. É o
  que alimenta a fatia de regressão.
- **Deriva** — mesmo eval, resultado caindo, prompt igual: mudou o modelo, mudou o
  dado de entrada, ou mudou o mundo. Investigue nessa ordem.
- **Canal de contestação** — quem usa precisa ter um botão de "isso está errado" que
  vira caso no dataset. Sem isso o erro só aparece quando vira reclamação.

## Armadilhas conhecidas

1. **Começar pelo LLM-as-judge.** → Custa mais, decide menos e adiciona um segundo
   modelo não confiável ao problema. *Correção:* passe pelos níveis 1 e 2 primeiro e
   só suba o que sobrar.

2. **Golden Dataset escrito por quem escreveu o prompt.** → O eval mede o autor,
   não o fluxo; passa em tudo e quebra no primeiro caso real. *Correção:* amostre do
   histórico e deixe outra pessoa selecionar.

3. **Ajustar o prompt olhando o conjunto de teste.** → Você otimiza para a prova; o
   número sobe e a qualidade real não. *Correção:* conjunto cego congelado, aberto só
   na decisão de rollout.

4. **Métrica única, média geral.** → Esconde falha concentrada na fatia que mais
   importa. *Correção:* corte por fatia, com adversarial separado.

5. **Nunca medir a abstenção.** → O modelo aprende a sempre responder e a alucinar em
   vez de dizer "não sei". *Correção:* trate a recusa correta como acerto e coloque
   casos sem resposta possível no dataset.

6. **Avaliar só a saída final de uma cadeia de agentes.** → Você sabe que quebrou,
   nunca onde. *Correção:* eval por etapa nos pontos de handoff, mesmo que simples.

7. **Eval sem dono.** → Roda três semanas, morre com a primeira semana corrida.
   *Correção:* nome no Eval Card e cadência amarrada ao deploy, não ao calendário.

8. **Tratar 100% como meta.** → Persegue-se perfeição em vez de decidir; o rollout
   trava para sempre. *Correção:* linha de corte defensável, escrita antes de rodar o
   eval — nunca depois de ver o resultado.

## Exemplo aplicado

**Fluxo:** agente lê e-mails de pedido de cliente e cria o registro no sistema.

- **Q1** — decidir se pode rodar sem conferência humana campo a campo.
- **Q2** — unidade = cada campo extraído (cliente, produto, quantidade, prazo);
  árbitro = a analista sênior do time; rubrica = campo bate com o e-mail, ou fica em
  branco quando o e-mail é ambíguo.
- **Q3** — falso positivo (quantidade errada virando pedido) custa muito mais que
  falso negativo (campo em branco que alguém preenche). Agente conservador.
- **Q4** — 50 e-mails reais dos últimos 6 meses: 20 típicos, 15 bordas (anexo,
  encaminhamento, dois pedidos no mesmo e-mail), 8 adversariais (pedido de
  cancelamento disfarçado), 7 de erros já vistos.
- **Q5** — nível 1 resolve quase tudo: campo extraído × campo do e-mail, tipo e faixa.
  Nível 3 só para "o e-mail era ambíguo o bastante para justificar deixar em branco?".
- **Q6** — quantidade e prazo ≥ 99%, demais campos ≥ 95%, adversarial ≥ 95%. Reprovou:
  volta para fila de revisão humana total. Roda a cada deploy e toda troca de modelo.

Resultado: Light em uma tarde, e uma decisão de automação que sobrevive à pergunta
"como você sabe?".
