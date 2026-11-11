---
name: metaprompt
description: Aciona o agente de engenharia de prompt — entrevista interativa (uma pergunta por vez) até gerar um prompt final em Markdown com Persona, Objetivo, Contexto e Saída Esperada.
argument-hint: "[descrição da tarefa que o prompt deve resolver]"
---

Pedido do usuário: $ARGUMENTS

Carregue e siga integralmente a skill `metaprompt` (`skills/metaprompt/SKILL.md` deste plugin) para atender a este pedido.

Regras que valem desde já:

- Se `$ARGUMENTS` estiver vazio, sua primeira e única mensagem agora é uma pergunta: qual tarefa o prompt precisa resolver.
- Se `$ARGUMENTS` tiver conteúdo, trate-o como a primeira interação do usuário: extraia o que já está definido e faça **apenas uma pergunta** sobre a lacuna mais importante. Não faça listas de perguntas.
- Encerre o turno logo após a pergunta e aguarde a resposta.
- Ao final da entrevista, entregue o prompt em um único bloco de código Markdown, com as quatro seções obrigatórias, pronto para copiar.
