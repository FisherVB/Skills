# metaprompt

> Transforma um pedido vago ("preciso de um prompt para X") em um prompt pronto para uso, depois de uma entrevista curta com quem pediu. Uma pergunta por vez.

## O que faz

Atua como especialista em engenharia de prompt e de contexto. Em vez de devolver um prompt genérico logo de cara, conduz uma entrevista para apurar o que o modelo executor vai precisar saber:

1. Lê o pedido inicial e separa o que já está definido do que falta. Não pergunta o que o usuário já disse.
2. Faz **uma pergunta por mensagem**, sempre com uma linha explicando por que ela importa.
3. Segue a ordem das lacunas: tarefa e resultado → quem consome a saída → insumos que o modelo vai receber → formato e extensão → critérios de qualidade e restrições → exemplos, tom e casos de borda.
4. Ajusta a profundidade ao tamanho do problema: de 2 a 4 perguntas para tarefa simples, mais para tarefa complexa ou recorrente.
5. Pesquisa na web quando faz diferença (padrão de mercado, API, norma, formato) e traz o achado na pergunta seguinte para o usuário confirmar.
6. Encerra quando mais uma pergunta já não mudaria o prompt.

Saída: um único bloco de código Markdown, em segunda pessoa e no idioma do usuário, com as quatro seções obrigatórias:

| Seção | Conteúdo |
|---|---|
| **Persona** | Papel que o modelo executor deve assumir |
| **Objetivo** | Tarefa a cumprir |
| **Contexto** | Tudo o que foi apurado na entrevista, incluindo restrições e o que não fazer |
| **Saída Esperada** | Estrutura verificável: seções, campos, extensão, formato |

Depois do bloco vêm no máximo duas linhas: as premissas assumidas e o que vale ajustar.

Regras do prompt gerado: `[colchetes]` só para o que muda a cada execução, contexto concreto em vez de resumo vago, saída descrita por estrutura e não por adjetivos. Se o prompt for de uso repetido, a fronteira entre a parte fixa e a entrada variável fica explícita.

## Quando usar

- Você quer que outro modelo execute uma tarefa repetidamente e precisa de uma instrução estável.
- O prompt atual dá resultado inconsistente e você não sabe o que está faltando.
- A tarefa depende de contexto que só você tem (cliente, processo, formato interno) e precisa ser escrita de forma que o modelo entenda.

**Não use** para pergunta pontual que você mesmo faria direto ao modelo, nem quando o problema é falta de dado ou de acesso a sistema, e não a forma da instrução.

## Exemplo de invocação

```
/metaprompt preciso de um prompt para analisar contratos de M&A
```

Ou em linguagem natural:

> Me ajuda a criar um prompt para classificar os chamados do suporte por urgência.

> Melhora esse prompt aqui: [cole o prompt atual]

Sem argumento (`/metaprompt` sozinho), a primeira pergunta é qual tarefa o prompt precisa resolver.

### Atalhos

- **`gera direto`** ou **`sem perguntas`**: pula a entrevista, gera o prompt e lista embaixo as premissas assumidas.
- **`melhora esse prompt`** + o prompt atual: aponta as lacunas nas quatro seções e pergunta só sobre o que falta.

## Instalação

| Arquivo | Para quê |
|---|---|
| `SKILL.md` | A skill. Fonte de verdade do comportamento |
| `commands/metaprompt.md` | O comando `/metaprompt` do plugin |
| `plugin.json` | Manifesto do plugin (versão, autor, keywords) |
| `build-packages.py` | Gera os dois pacotes abaixo a partir dos arquivos acima |
| `metaprompt.skill` | Pacote só da skill, para Claude.ai / Cowork |
| `metaprompt-plugin.zip` | Plugin completo: skill + comando `/metaprompt` + manifesto |

**Claude Code, por symlink** (atualiza com `git pull`):

```bash
ln -s <caminho-local-deste-repo>/metaprompt ~/.claude/skills/metaprompt
```

**Claude Code, como plugin** (inclui o comando `/metaprompt`): descompacte `metaprompt-plugin.zip`, coloque a pasta em um marketplace de plugins e rode `/plugin marketplace add <repo-ou-caminho>` seguido de `/plugin install metaprompt`. Para testar sem marketplace, use `claude --plugin-dir <pasta-descompactada>`.

**Claude.ai / Cowork**: abra o `metaprompt.skill` e clique em **Save skill**. Não há comando de barra nesse modo; a skill dispara por linguagem natural ("cria um prompt para...", "melhora esse prompt").

### Atualizar os pacotes

Os pacotes `.skill` e `.zip` são snapshots: quem já instalou não recebe mudanças sozinho. Depois de mudar `SKILL.md`, `README.md`, `commands/` ou `plugin.json`, suba a `version` no `plugin.json` e gere os pacotes de novo:

```bash
python3 metaprompt/build-packages.py
```

Faça commit dos pacotes junto com a mudança, para que o que está no GitHub bata com o código-fonte.
