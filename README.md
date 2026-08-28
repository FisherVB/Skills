# Skills

Skillset colaborativo da Fisher.

#FORK, use, melhore! Esse repositório é nosso para desenvolvimento conjunto.

**Dê feedback!** Sem ele não evoluímos. Proponha novos skills ou plugins que
considere relevantes para o uso na nossa comunidade.

> Este repositório é espelhado a partir de
> [`fisher-brain/30-skills-e-prompts`](https://github.com/FisherVB/fisher-brain/tree/main/30-skills-e-prompts),
> que é a fonte de verdade. Mudanças devem ser feitas lá — veja
> [Sincronização](#sincronização) abaixo.

## Trilha de automação e orquestração com agentes

Skills próprios da Fisher para conduzir clientes e times internos da ideia de automação
até a operação. A ordem respeita as dependências: sem seleção não há escopo, sem eval
não há rollout defensável.

| # | Skill | Papel na trilha |
|---|---|---|
| 1 | [`process-selection-advisor`](process-selection-advisor/) | Qual etapa vale automatizar — e qual não vale. Veredicto: automatizar / assistir / redesenhar antes / não mexer |
| 2 | [`eval-design`](eval-design/) | Como saber se o agente está certo antes que o cliente descubra. Golden Dataset, linha de corte, gate |

Gaps mapeados para desenvolvimento futuro, na sequência em que fazem sentido:

- `context-design` — manifesto de contexto: o que persiste, o que é recuperado, quem é o dono da fronteira
- `tool-and-data-access` — acesso a sistema, API/MCP, permissão e dado sensível
- `human-in-the-loop-design` — onde o humano aprova, onde só audita, onde o agente age só (entra direto no veredicto "assistir")
- `failure-and-rollback` — o que o agente faz quando não sabe, e como reverter ação já executada
- `agent-cost-model` — custo por execução × custo do trabalho substituído, com manutenção

## Escrita e revisão

| Skill | Papel |
|---|---|
| [`anti-slop-ptbr`](anti-slop-ptbr/) | Tira as marcas de escrita gerada por IA de texto em PT-BR. Deny-lists de vocabulário e pontuação, tells estruturais, teste de densidade informacional, score editorial |

## Instalação local

Os skills ficam versionados aqui e são instalados por symlink, para que `git pull`
atualize a versão em uso:

```bash
ln -s <caminho-local-deste-repo>/<skill> ~/.claude/skills/<skill>
```

### Empacotar como plugin do app do Claude

O symlink cobre o Claude Code na sua máquina. Para instalar um skill no app do Claude,
e em sessões na nuvem, que não enxergam o seu `~/.claude/`, gere um pacote `.plugin`
a partir da mesma pasta:

```bash
python3 build-plugin.py anti-slop-ptbr    # ou --all
```

O arquivo sai em `dist/<skill>.plugin`, que o git ignora, e se instala abrindo-o no app.
O script monta o manifesto a partir do próprio `SKILL.md`, então o repositório continua
sendo a fonte única: não existe uma segunda cópia do conteúdo para divergir.

Um detalhe que muda como você mantém isso: o plugin instalado é um snapshot, não um
link. Quem instalou não recebe as suas mudanças com `git pull`. Suba a `version` no
`plugin.json` da pasta do skill a cada mudança publicada e redistribua o pacote, para
que dê para saber qual versão cada pessoa está rodando.

## Convenção

Cada skill é uma pasta com `SKILL.md` (frontmatter `name` + `description` detalhada,
que é o que dispara o skill), `README.md` (o que faz, quando usar, exemplo de
invocação) e `references/` com os templates de saída.

Opcionalmente, um `plugin.json` com os metadados de release (`version`, `keywords`)
lidos pelo `build-plugin.py`. Esse arquivo não entra no pacote gerado e não interfere
no symlink.

Padrão de escrita adotado: modos de uso (guiado / despejo de contexto / melhor
palpite), escada de decisão com uma pergunta por turno, right-sizing Light / Standard /
Heavy, e armadilhas conhecidas sempre com **consequência e correção**.

## Contribuindo

Este repositório é a porta de entrada para contribuições externas — quem não é
colaborador da Fisher não tem acesso ao `fisher-brain`, que é privado. Abra um PR
aqui normalmente.

**Todo PR só pode ser mesclado com aprovação de `@cgamboa-fisher` ou `@vinicatto`**
(regra de proteção de branch + `CODEOWNERS`).

## Sincronização com fisher-brain

A sincronização com `fisher-brain/30-skills-e-prompts` (o second brain privado da
Fisher) é bidirecional, e cada lado sempre passa por PR + aprovação de
`@cgamboa-fisher` ou `@vinicatto` no repositório de destino — nunca há merge direto:

- **fisher-brain → Skills:** todo push em `main` do fisher-brain que altere a pasta
  abre um PR aqui, mantendo este repositório espelhado.
- **Skills → fisher-brain:** todo PR mesclado aqui (incluindo contribuições externas)
  abre um PR de inclusão no fisher-brain. Ser aceito aqui **não** aplica a mudança lá
  automaticamente — é uma proposta, ainda sujeita a aprovação no second brain privado.

Um arquivo `.github/fisher-brain-sync-manifest.txt` rastreia quais pastas de topo são
geridas por essa sincronização, para que uma contribuição nova aqui nunca seja apagada
antes de ser replicada para o fisher-brain.
