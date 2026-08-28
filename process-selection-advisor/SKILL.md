---
name: process-selection-advisor
description: >-
  Escolhe qual processo (na verdade: qual etapa) vale automatizar ou orquestrar com
  agentes, e qual não vale — antes de qualquer construção. Conduz um diagnóstico
  guiado que separa a etapa da narrativa do processo, aplica três portas de
  elegibilidade (dado acessível, resposta verificável, erro absorvível), classifica a
  forma do trabalho, calcula o ponto de equilíbrio contra o custo humano e de
  manutenção, e devolve um veredicto entre automatizar, assistir, redesenhar antes ou
  não mexer. Entrega um Scorecard de candidatos, o recorte da etapa escolhida e a
  passagem de bastão para o desenho de contexto e de eval. Use quando houver mais
  ideias de automação do que capacidade de execução, quando alguém pedir "vamos
  automatizar tal área", quando um piloto de IA não gerou ganho perceptível, quando
  for montar a fila de casos de uso de um squad de IA, ou quando as palavras qual
  processo, priorizar automação, caso de uso, mapear oportunidade, vale a pena
  automatizar, ROI de agente ou fila de automação aparecerem.
---

# Process Selection — automatizar o processo errado com competência é o desperdício mais caro

## Modos de uso

Pergunte primeiro como o usuário quer trabalhar:

1. **Guiado** — uma pergunta por vez, ~20 minutos por candidato.
2. **Despejo de contexto** — o usuário cola a lista de ideias, o fluxograma, a ata da
   reunião; você organiza e pula o que já está respondido.
3. **Melhor palpite** — você assume o razoável, marca cada suposição com `[suposto]`
   e segue.

Se o usuário trouxer **mais de um candidato**, rode as três portas (Q2) em todos antes
de aprofundar qualquer um. Elimina metade da lista em dez minutos e evita gastar a
sessão no candidato mais simpático em vez do mais viável.

## Input

Em linguagem natural:

- A lista de processos ou ideias em disputa, mesmo bagunçada.
- Quem faz o trabalho hoje, quantas pessoas, quanto tempo.
- Onde o dado vive (sistema, planilha, e-mail, cabeça de alguém).
- O que já foi tentado e não pegou.
- Qual pressão está por trás do pedido (custo, prazo, qualidade, cliente, chefe).

Falta de informação vira pergunta, não bloqueio.

## Quando usar

✅ **Use quando:**

- Existem mais ideias de automação do que gente para construir.
- A conversa começou com "vamos usar IA em [área]" — área não é processo.
- Um piloto rodou, funcionou tecnicamente e ninguém sentiu diferença.
- O squad de IA precisa de uma fila defensável, não de uma lista de desejos.
- A automação anterior morreu por manutenção, não por qualidade.

❌ **Não use quando:**

- A etapa e o veredicto já estão claros e acordados — vá para o desenho.
- O pedido é de melhoria de prompt num fluxo que já roda bem.
- O problema é de sistema/integração e ninguém está propondo IA.
- O processo está em mudança estrutural nos próximos 90 dias (troca de ERP, fusão de
  áreas); espere o desenho novo, ou você vai automatizar um processo que vai deixar
  de existir.

## Três premissas que mudam a conversa

**1. Não se automatiza um processo. Automatiza-se uma etapa.**
Processo é unidade de gestão; etapa é unidade de automação. "Automatizar o
faturamento" não é escopo — é ambição. "Extrair os dados do pedido do e-mail e
preencher o registro" é escopo. Quem insiste no processo inteiro entrega tarde,
depende de sete integrações e não consegue medir nada.

**2. Automatizar desperdício produz desperdício mais rápido.**
Se a etapa só existe porque alguém, em 2019, pediu um relatório que ninguém mais lê,
o ganho é eliminar, não acelerar. Sempre pergunte se a etapa deveria existir antes de
perguntar se pode ser automatizada.

**3. O maior ganho geralmente está no que hoje *não* é feito.**
Economia de horas é o cálculo fácil e o de menor teto — e frequentemente não vira
caixa, porque a pessoa continua na folha. O ganho grande está no trabalho que ninguém
faz por falta de tempo: analisar todos os clientes em vez dos dez maiores, revisar
todos os contratos em vez de uma amostra, responder em uma hora em vez de dois dias.
Chame isso pelo nome: **custo do não-feito**. É invisível na planilha de economia e é
onde vive a diferenciação.

## A escada de decisão (7 perguntas)

Uma por turno. Sinalize progresso ("Seleção 3/7").

### Q1 — Qual é a etapa, em uma frase com verbo?

Force o recorte: *"Alguém pega **[entrada]**, faz **[verbo]**, e produz **[saída]**,
que é usada por **[quem]** para **[decidir o quê]**."*

Se a frase precisar de "e" três vezes, são três etapas. Separe e escolha uma.

Peça o volume junto: **quantas vezes por semana × quanto tempo cada vez × quantas
pessoas**. Sem esses três números não existe caso, existe história.

Atenção ao viés do tempo: **o que consome mais horas não é necessariamente o gargalo**.
Pergunte onde o trabalho *espera*. Muitas vezes a etapa longa não trava nada e a
etapa de dois minutos trava o dia inteiro porque depende de uma pessoa só.

### Q2 — As três portas de elegibilidade

Portas duras, avaliadas em sequência. Falhou em uma, **pare** — não negocie com ela,
registre o candidato como bloqueado e diga o que o desbloquearia.

**Porta 1 — O dado de entrada é acessível a um agente?**
Não "existe": *acessível*. Está em sistema com API, em arquivo, em e-mail? Ou está em
PDF escaneado, em conversa de WhatsApp, ou na cabeça de quem faz? Há permissão para
usar? Tem dado pessoal ou sensível envolvido, e sob qual base?
*Falha comum:* "o dado está no ERP" — está, mas ninguém tem acesso de leitura e
liberar leva quatro meses. Isso é parte do projeto, não detalhe.

**Porta 2 — Existe como saber se a saída está certa?**
Alguém consegue olhar e dizer certo/errado em tempo razoável? Existe fonte de
verdade para conferir? Se ninguém sabe julgar, não há eval — e sem eval a automação é
fé. (Aqui a passagem de bastão é para `eval-design`.)

**Porta 3 — O erro é absorvível?**
Quanto custa um erro e ele é reversível? Rascunho que passa por gente, sim. Emissão
fiscal, movimentação de estoque, comunicação ao cliente sem revisão: só com desenho
específico de aprovação. Erro irreversível não elimina o candidato, mas **rebaixa o
veredicto de "automatizar" para "assistir"**.

### Q3 — Qual é a forma do trabalho?

Classifique a etapa. A forma prevê o resultado melhor que o setor:

| Forma do trabalho | Aptidão | Observação |
|---|---|---|
| Ler muito texto e extrair/resumir | Alta | O caso mais confiável que existe hoje |
| Classificar e rotear por critério escrito | Alta | Desde que o critério exista escrito |
| Redigir rascunho a partir de dado estruturado | Alta | Humano revisa e assina |
| Buscar e reconciliar informação em várias fontes | Média-alta | Depende da Porta 1 |
| Aplicar regra determinística e calcular | Baixa (para IA) | Isto é sistema, não agente — e sai mais barato |
| Coordenar pessoas, negociar, cobrar | Baixa | Automatize o lembrete, não a negociação |
| Julgar exceção com contexto político | Muito baixa | Aqui a IA prepara o dossiê; a pessoa decide |
| Assumir responsabilidade por uma decisão | Nenhuma | Responsabilidade não delega para software |

Duas leituras importantes: se a resposta é "aplicar regra e calcular", **a
recomendação honesta é não usar IA** — é automação clássica, mais barata e
determinística. E se a resposta é "julgar exceção", o recorte certo não é a decisão, é
o **preparo** da decisão.

### Q4 — O processo atual merece ser preservado?

Antes de acelerar, teste:

- Se essa etapa parasse hoje, quem reclamaria e em quantos dias?
- A saída é consumida ou arquivada?
- Por que ela existe assim? (Se a resposta é "sempre foi", há espaço para eliminar.)
- Quantas vezes o trabalho é refeito por erro ou por retrabalho de outra área?

Três desfechos: **preservar** (a etapa é boa, acelere), **redesenhar antes**
(automatizar cimentaria o ruim) ou **eliminar** (o melhor retorno de todos, e não
precisa de IA).

### Q5 — A conta fecha?

Três números, honestos:

- **Ganho anual** = (volume/ano × tempo por execução × custo/hora) + custo do
  não-feito, este último declarado em separado e sem inventar precisão.
- **Custo de construção** = pessoa × semanas, mais integração e acesso a dado. Some
  o tempo de liberar permissão; é onde os prazos morrem.
- **Custo de operação anual** = execução (modelo/infra) + **manutenção**, que é a
  linha que todo mundo esquece: prompt quebra quando o processo muda, modelo é
  descontinuado, layout de sistema muda. Orce entre 15% e 30% da construção por ano,
  todo ano.

Ponto de equilíbrio em meses = construção ÷ (ganho mensal − operação mensal). Régua
prática: **acima de 18 meses, o candidato só passa se o ganho for estratégico e
declarado como tal** — não maquie a economia para justificar o que é aposta.

Faça também o teste do contrafactual: **existe uma solução chata que resolve 80%?**
Um campo obrigatório no formulário, um relatório agendado, um filtro. Se existe, ela
vence — e você guarda a capacidade do time para o que só IA faz.

### Q6 — Quem é o dono, e quem perde?

Automação não falha por técnica; falha por adoção.

- **Dono da etapa** — nome, não área. Sem dono, não comece.
- **Quem recebe a saída** — o que muda no trabalho dessa pessoa? Ela vai confiar? O
  que ela vai querer conferir nos primeiros 30 dias?
- **Quem perde** — controle, relevância, headcount, poder de barganha. Nomeie sem
  eufemismo, ainda que só nesta sessão. A resistência que você não nomeia é a que
  mata o piloto em silêncio.
- **O que vai deixar de ser feito** para liberar quem constrói. Se a resposta é
  "nada, é por cima do trabalho atual", o projeto já está atrasado.

### Q7 — Veredicto

Um dos quatro, explícito, com a razão em uma linha:

| Veredicto | Quando | Próximo passo |
|---|---|---|
| **Automatizar** | Passou as três portas, forma de alta aptidão, conta fecha, tem dono | Desenho de contexto → `eval-design` → piloto |
| **Assistir** | Passou as portas mas o erro é caro ou irreversível | Agente prepara, humano aprova; medir a taxa de aprovação sem alteração |
| **Redesenhar antes** | A etapa é ruim ou o dado não existe de forma usável | Corrigir processo/dado; reavaliar em 90 dias |
| **Não mexer** | Volume baixo, regra determinística, ou é negociação/responsabilidade | Dizer não com o motivo escrito. Vale tanto quanto um sim |

Um "não mexer" bem argumentado é entregável. É o que devolve credibilidade ao squad
quando ele diz "sim" na vez seguinte.

## Priorizando entre candidatos

Quando houver vários aprovados, pontue de 1 a 5 e some com peso:

| Critério | Peso |
|---|---|
| Ganho (horas + custo do não-feito) | 3 |
| Aptidão da forma do trabalho (Q3) | 3 |
| Facilidade de acesso ao dado (Porta 1) | 2 |
| Verificabilidade (Porta 2) | 2 |
| Absorção do erro (Porta 3) | 2 |
| Dono presente e engajado (Q6) | 2 |
| Baixo custo de manutenção previsto | 1 |

Regra de sequência que vale mais que a pontuação: **o primeiro caso do time não é o
de maior ganho, é o que termina.** Escolha um que caiba em 4–6 semanas, tenha dono
presente e produza um número que alguém fora do time entenda. O segundo caso é o
ambicioso — e ele só existe se o primeiro entregou.

## Right-sizing

- **Light (1h)** — 1 a 3 candidatos, só as três portas e o Q1. Para uma reunião em que
  alguém precisa decidir hoje onde colocar o time.
- **Standard (meio dia)** — até 8 candidatos: portas em todos, escada completa nos 3
  sobreviventes, Scorecard e sequência. **Padrão para montar a fila de um squad.**
- **Heavy (1–2 semanas)** — inclui observação do trabalho real (acompanhar quem faz,
  não só perguntar), medição de volume no sistema e validação da conta com finanças.
  Para quando a decisão envolve headcount, investimento ou compromisso com a
  diretoria.

## Saídas

1. **Scorecard de candidatos** — use `references/candidate-scorecard.md`.
2. **Recorte da etapa escolhida** — a frase do Q1, com entrada, saída e consumidor.
3. **Conta em três linhas** — ganho, construção, operação anual e ponto de equilíbrio.
4. **Sequência recomendada** — primeiro caso (o que termina), segundo (o ambicioso),
   e o que fica na fila com a condição para entrar.
5. **Lista de "não" com motivo** — por escrito.
6. **Passagem de bastão** — para o desenho de contexto e para `eval-design`, com as
   perguntas já respondidas aqui.

## Armadilhas conhecidas

1. **Escolher o processo mais visível.** → O caso vitrine tem dez interessados, cada
   um com um requisito, e não termina. *Correção:* o primeiro caso é escolhido por
   probabilidade de terminar, não por audiência.

2. **Aceitar "área" como escopo.** → "IA no comercial" não tem entrada, saída nem
   dono; vira seis meses de reunião. *Correção:* exija a frase com verbo do Q1.

3. **Ignorar o custo de manutenção.** → A automação funciona seis meses, o processo
   muda, ninguém mantém, o time volta ao manual e a conclusão organizacional passa a
   ser "IA não funciona aqui". *Correção:* 15–30% da construção por ano, orçado e com
   dono.

4. **Contar economia de horas que não vira caixa.** → A conta é aprovada, o custo não
   cai, o patrocinador perde confiança na próxima. *Correção:* declare separadamente
   horas reduzidas e custo do não-feito; não misture.

5. **Automatizar antes de resolver o acesso ao dado.** → Três semanas de prompt e
   quatro meses esperando permissão. *Correção:* Porta 1 é a primeira por um motivo.

6. **Usar IA onde regra resolve.** → Mais caro, não determinístico, mais difícil de
   auditar. *Correção:* se dá para escrever a regra, escreva a regra.

7. **Perguntar em vez de olhar.** → O processo descrito na reunião não é o processo
   executado; as exceções (que são a maior parte do trabalho) só aparecem quando você
   senta ao lado. *Correção:* no Standard, valide o volume no sistema; no Heavy,
   observe.

8. **Não nomear quem perde.** → O piloto é sabotado por indiferença educada.
   *Correção:* Q6 explícito, e um desenho em que o dono da etapa ganhe algo real.

## Exemplo aplicado

**Pedido inicial:** "queremos usar IA na logística."

**Candidatos após o Q1** — (a) conferir divergência entre nota fiscal e o que chegou;
(b) responder ao cliente onde está o pedido; (c) decidir realocação de carga quando
falta caminhão.

**Portas:**
- (a) dado em sistema ✔ / conferível contra a nota ✔ / erro apontado antes do
  pagamento, absorvível ✔ → **passa**
- (b) dado depende de status que chega por WhatsApp do motorista ✘ (Porta 1) →
  **bloqueado**: o desbloqueio é o registro de status na origem, não um agente
- (c) forma = julgar exceção com contexto político (custo, cliente, relação com
  transportadora) → **não automatizar a decisão**; recortar o *preparo*: montar em 2
  minutos o dossiê de opções com custo e impacto de prazo

**Conta em (a):** 300 conferências/mês × 12 min × custo/hora, mais o custo do
não-feito (hoje só 30% das notas são conferidas — o ganho real é conferir 100%).
Construção de 4 semanas, equilíbrio em 7 meses.

**Veredicto:** (a) **automatizar**, primeiro caso — cabe no prazo, tem dono no fiscal,
e produz um número que a diretoria entende: divergência recuperada em reais.
(c) **assistir**, segundo caso. (b) **redesenhar antes** — vira projeto de captura de
status, e resolve (b) e metade de (c) de uma vez.

Repare no padrão: o pedido era "IA na logística" e o entregável foi uma automação, um
copiloto e um projeto de dado que não é de IA. É o resultado normal de uma seleção
bem feita.
