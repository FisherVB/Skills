# Tells estruturais e semânticos

> Catálogo de padrões de estrutura e de sentido, com exemplos de reescrita.

Entre marcadores `lint:off`: os exemplos de "antes" contêm de propósito as construções barradas.

<!-- lint:off -->

# 5. Tells estruturais

## 5.1. Regra de três

Exemplo ruim:

"rápido, confiável e eficiente"

Problema:

Três quase-sinônimos carregando a informação de um.

Regra:

> Se os três itens não forem semanticamente distintos, reduzir.

---

## 5.2. Contraste binário telegrafado

Evitar:

- não é X, é Y;
- não porque X, mas Y;
- não se trata apenas de X, mas de Y;
- não é só X, é Y.

Exemplo:

"Não é só software, é uma nova forma de trabalhar."

Preferir:

"Centraliza o processo de aprovação e reduz retrabalho entre marketing e jurídico."

---

## 5.3. "Mais do que X"

Evitar:

"Mais do que uma ferramenta, é um parceiro estratégico."

Regra:

> Cortar a primeira metade e dizer diretamente o que o produto faz.

---

## 5.4. "Vai além de"

Evitar:

"A solução vai além da automação."

Pergunta obrigatória:

> O que ela faz além da automação?

---

## 5.5. Negação dramática em série

Evitar:

"Não é uma agência. Não é um SaaS. É uma nova categoria."

Regra:

> Nomear a categoria e provar por que ela existe.

---

## 5.6. Pergunta falsa seguida de resposta

Evitar:

- O resultado? Mais eficiência.
- A diferença? Dados.
- O segredo? Consistência.

Regra:

> Cortar suspense artificial.

---

## 5.7. Pergunta que responde a si mesma

Evitar:

"Por que isso importa? Porque..."

Regra:

> Na maioria dos casos, transformar em afirmação direta.

---

## 5.8. Setup de revelação

Evitar:

- E é aí que entra a IA.
- Aqui está o ponto.
- A grande questão é:
- A verdade é que:

Regra:

> Começar pelo ponto.

---

## 5.9. Fragmentos punchy empilhados

Evitar:

"Mais foco. Mais clareza. Mais resultado."

Regra:

> Flag 3 ou mais fragmentos consecutivos sem informação concreta.

---

## 5.10. Slogan binário

Evitar:

- Menos trabalho. Mais resultado.
- Menos complexidade, mais crescimento.
- Mais velocidade, menos esforço.

Regra:

> Exigir mecanismo, métrica ou consequência concreta.

---

## 5.11. Simetria suspeita

Sinais:

- sempre 3 benefícios;
- sempre 3 desafios;
- sempre 3 próximos passos;
- blocos com tamanho muito parecido;
- títulos espelhados;
- todos os bullets com a mesma construção.

Regra:

> Permitir estrutura irregular quando o conteúdo pedir.

---

## 5.12. Parágrafo-molde

Padrão típico:

1. tese;
2. explicação;
3. exemplo genérico;
4. conclusão.

Problema:

Quando todos os parágrafos seguem a mesma arquitetura, o texto fica previsível.

Regra:

> Variar a função e o tamanho dos parágrafos.

---

## 5.13. Lista-molde

Exemplo:

- Permite...
- Garante...
- Oferece...
- Facilita...

Regra:

> Variar ou transformar em prosa quando a lista não acrescentar clareza.

---

## 5.14. Lista por compulsão

Sinal:

Tudo vira lista de 3 ou 5 itens.

Regra:

> Só listar quando a enumeração ajudar o leitor.

---

## 5.15. Redundância tripla

Padrão:

1. afirma;
2. reformula;
3. resume.

Regra:

> Manter apenas a formulação mais informativa.

---

## 5.16. Conclusão-resumo automática

Sinal:

O último parágrafo apenas repete o que já foi dito.

Regra:

> Fechar com informação nova ou terminar antes.

---

## 5.17. Seção "desafios e oportunidades"

Evitar construções genéricas como:

"Apesar dos avanços, ainda existem desafios."

Regra:

> Nomear o problema concreto.

---

## 5.18. Futuro genérico

Evitar:

"À medida que a tecnologia evolui, espera-se que..."

Regra:

> Só manter se houver previsão, marco, hipótese ou evento concreto.

---

## 5.19. Faixa falsa

Evitar:

- de startups a grandes corporações;
- do iniciante ao especialista;
- de pequenas empresas a líderes globais.

Regra:

> Nomear o ICP real.

---

## 5.20. Universalização

Evitar:

- empresas de todos os portes;
- profissionais de diferentes setores;
- organizações de todos os tipos;
- qualquer pessoa que queira crescer.

Regra:

> Delimitar quem realmente se beneficia.

---

## 5.21. "Seja você X ou Y"

Evitar:

"Seja você empreendedor ou executivo..."

Regra:

> Cortar segmentação artificial quando não houver diferença de uso.

---

# 6. Cauda de gerúndio

Sinal forte em PT-BR.

Padrão:

> fato concreto + vírgula + gerúndio abstrato.

Exemplos:

"A plataforma centraliza os dados, garantindo maior eficiência e promovendo decisões mais estratégicas."

"A nova identidade reforça a marca, criando conexões mais profundas e fortalecendo sua presença no mercado."

"O sistema automatiza tarefas, permitindo que as equipes foquem no que realmente importa."

"A iniciativa amplia o acesso, contribuindo para um ecossistema mais inclusivo e sustentável."

Palavras a flagar quando aparecem nessa posição:

- garantindo
- permitindo
- promovendo
- fortalecendo
- contribuindo
- reforçando
- evidenciando
- consolidando
- impulsionando
- proporcionando
- viabilizando

Regra:

> Não banir gerúndio. Flag quando a oração final apenas interpreta o fato sem acrescentar mecanismo, número, etapa ou consequência verificável.

---

# 8. Slop semântico

## 8.1. Qualificação sem mecanismo

Exemplo:

"Uma solução estratégica e eficiente."

Pergunta:

> Estratégica por quê? Eficiente em qual métrica?

---

## 8.2. Importância autodeclarada

Evitar:

- representa um marco;
- marca uma mudança significativa;
- tem papel fundamental;
- é peça-chave;
- é essencial para;
- reflete uma tendência mais ampla;
- se consolida como referência;
- ganha cada vez mais relevância.

Regra:

> Substituir a declaração de importância pela evidência que prova a importância.

---

## 8.3. Impacto imaginado

Evitar:

- transforma a forma como empresas operam;
- redefine o futuro de X;
- muda a maneira como nos relacionamos com Y;
- está moldando uma nova era;
- promete revolucionar o setor.

Regra:

> Explicar o processo concreto que mudou.

---

## 8.4. Análise anexada

Evitar fatos seguidos de:

- reforçando a importância de;
- evidenciando o compromisso com;
- consolidando sua posição como;
- demonstrando o potencial de;
- destacando seu papel como;
- sinalizando uma mudança mais ampla.

Regra:

> Se a interpretação é óbvia ou não comprovada, cortar.

---

## 8.5. Abstração de relação

Flag:

- está alinhado com;
- se conecta a;
- está associado a;
- dialoga com;
- converge com;
- reflete;
- remete a.

Pergunta obrigatória:

> Qual é a relação concreta?

---

# 9. Densidade informacional

Este é um dos sinais mais importantes.

Evitar frases que afirmam muito e especificam nada.

Exemplo ruim:

"A IA está transformando profundamente a forma como empresas trabalham."

Exemplo melhor:

"A equipe reduziu de 4 horas para 40 minutos o tempo gasto para produzir o relatório semanal."

Regra principal:

> Toda frase precisa fazer pelo menos um trabalho verificável: acrescentar fato, mecanismo, exemplo, decisão, contraste real, consequência ou interpretação não óbvia.

Se uma frase pode ser removida sem perda de informação, cortar.

---

# 10. Ritmo

Slop tende a ter:

- frases de tamanho parecido;
- parágrafos de tamanho parecido;
- mesma cadência;
- mesma estrutura sintática;
- listas excessivamente organizadas;
- alternância previsível entre tese, explicação e conclusão.

Regra:

> Variar frases curtas e longas de forma natural.

Flag sugerido:

> 3 ou mais frases consecutivas com tamanho e construção muito semelhantes.

---

# 13. Markdown e formatação

Flagar quando o texto final não pede Markdown e aparecem:

- headings excessivos;
- negrito em quase toda frase-chave;
- separadores `---`;
- tabelas desnecessárias;
- blockquotes decorativos;
- listas para ideias que caberiam em uma frase;
- títulos com capitalização artificial;
- seção de "Conclusão" em texto curto.

Regra:

> Formatação deve servir ao conteúdo, não simular organização.

---


<!-- lint:on -->
