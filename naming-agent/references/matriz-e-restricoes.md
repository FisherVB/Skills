# Matriz de Decisão, restrições e disponibilidade

Leia pros Passos 6 (pontuar) e 8 (checar restrições). Dá o significado de cada
nota na matriz e as regras práticas de até onde confiar nas checagens.

## As restrições (Passo 1)

Todo nome tem que passar nestas — são o filtro antes de pontuar:

- **Curto** — idealmente 1–3 sílabas.
- **Registrável (domínio)** — dá pra ter o domínio de interesse.
- **Fácil de falar e entender** — teste do telefone.
- **Se escreve como se fala** — teste do rádio.
- **Funciona em inglês** — se for global.
- **Buscável no Google** — não afunda em homônimos.

Nome que falha numa restrição dura (impronunciável, sentido ruim num idioma-alvo,
clone de gigante) sai antes da matriz, por melhor que soe.

## A Matriz de Decisão (Passo 6) — o que é 0, 1, 2, 3

Pontue cada nome de 0 a 3 por critério. O objetivo é forçar comparação honesta e
expor fraqueza que o "soa legal" esconde. Guia de nota:

| Critério | 0 | 3 |
|---|---|---|
| **Funciona internacionalmente** | sentido/pronúncia ruim fora do país | limpo em todos os mercados-alvo |
| **Soa bem / agradável** | áspero, travado | gostoso de ouvir e dizer |
| **Fácil de pronunciar** | gente hesita/erra | sai sozinho na boca |
| **Se escreve como se fala** | precisa soletrar | escrito certo de primeira |
| **Fácil de buscar no Google** | sumido num mar de homônimos | acha de primeira, pouco disputado |
| **Registrável (domínio e nome)** | domínio/marca claramente tomados | plausivelmente registrável |
| **Transmite benefício / mensagem** | não diz nada | carrega a promessa da marca |
| **Memorável** | esquecido em um minuto | gruda depois de uma exposição |
| **Causa impacto** | morno, esquecível | chama atenção, tem presença |
| **É único** | se confunde na categoria | inconfundivelmente dele |

Some as notas e ranqueie — o script faz isso. Mas use julgamento: um nome que
crava a personalidade da marca pode valer mais que o de maior soma. Pondere por
brief (app de consumo pesa memorável/dizível; escritório de advocacia pesa
impacto/credibilidade).

**Portas de corte** (falhou = sai, não importa a soma): sentido negativo real num
idioma-alvo; colisão quase idêntica com um gigante da mesma área; impronunciável
pro público.

## Rastreio linguístico / cultural

A checagem mais barata que evita o erro mais caro. Pra cada finalista, pense no
sentido e na conotação em **cada idioma de mercado-alvo**, mais os idiomas
globais se a marca viajar.

- Cheque: palavrão/tabu, homônimo infeliz, associação esquisita, cluster difícil
  pra não-nativo.
- Quando não tiver certeza de um sentido num idioma, **diga que não tem** e
  recomende checar com nativo — não afirme que está ok no chute.
- Rastreie também o **domínio lido como uma palavra só** (o problema do
  "pen island" → penisland): diga o domínio em voz alta sem espaços.

## Disponibilidade de domínio — como ler

O script usa **RDAP** (sucessor oficial do WHOIS), resolvendo o servidor
autoritativo de cada TLD pelo bootstrap do IANA.

- **"available"** = o registro não existe → sinal forte de registrável. Mas: o
  registrador pode precificar como *premium* ou ter reservado. Confirme num
  registrador antes de contar com ele.
- **"registered"** = tomado. (O dono pode vender, mas trate como tomado.)
- **"unknown"** = o TLD não tem endpoint RDAP (vários ccTLDs: `.io`, `.co`, `.me`,
  `.us`...) ou a consulta falhou. **Não** reporte como livre. Cheque na mão.
- DNS "sem site" ≠ livre. Muito domínio registrado não tem site — por isso RDAP,
  não ping.

## Handles de rede — como ler

A sondagem `--handles` busca a URL de perfil e infere do status HTTP. É
**indicativa**: handle parado/suspenso volta como tomado; plataforma com
anti-bot volta non-200 pra perfil real. Primeira passada — confira os finalistas
abrindo o perfil.

## Marca (trademark) — a versão honesta

Você **não** faz clearance jurídico. O que dá pra fazer:
- Busca de nocaute: busque o nome exato + categoria, e o nome na busca pública do
  órgão (INPI no Brasil, USPTO, EUIPO — se tiver navegador) pra pegar colisão óbvia.
- Sinalize quando o nome é palavra comum já muito registrada, ou numa classe lotada.

O que **dizer ao usuário**: clearance de marca de verdade (marcas iguais ou
semelhantes nas classes/jurisdições) é passo profissional/jurídico. Domínio livre
não significa marca livre. Diga isso em bom português, uma vez, sem alarmismo. No
Brasil, o registro é no **INPI**.

## Checklist de pré-commit (entregue pro usuário nos finalistas)

Antes de cravar um nome, confirme:
1. Domínio confirmado num registrador (não só RDAP), a preço aceitável.
2. Handles principais de fato livres (checados na mão).
3. Sentido rastreado por nativo em cada mercado grande.
4. Clearance de marca profissional nas classes/jurisdições (INPI no Brasil).
5. Dito em voz alta pra algumas pessoas do público — elas falam, escrevem e
   lembram no dia seguinte.
