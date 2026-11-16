# Experimento 1: primeira execução completa (12–13/nov/2026)

Primeira execução da comparação completa (`make comparacao`), no commit `1ee3691` (C1–C15).
Faz parte do trabalho: foi esta execução que revelou os defeitos registrados como **C16** em
[`docs/metodologia.md`](../docs/metodologia.md), corrigidos antes do experimento 2. Os números daqui
valem como **resultado preliminar**; os do experimento 2 substituem estes no artigo.

## Ambiente

| | |
|---|---|
| Máquina | VM VMware, 4 vCPUs Intel Xeon Gold 6348 @ 2,60 GHz, 15 GiB, Linux 6.4 (SLES), Docker 28.5.1, Compose 2.22 |
| Perfil de CPU | `compose.4cpu.yml` (C15): banco núcleo 0, API núcleo 1, gerador núcleos 2–3 com 2 processos |
| Desenho | 3 implementações × 5 repetições intercaladas × 10 cenários, degraus de 60 s, banco novo a cada implementação |
| Duração | 21h41 → 07h21 (cerca de 9h40) |
| Contrato (C14) | as três APIs passaram (`logs/contrato.log`) |
| Calibração do gerador | cumpre a agenda até 3000 req/s contra o servidor nulo (`logs/calibracao.txt`) |

## Conteúdo

```
resultados/<impl>/rep_<k>/<cenario>/   resumo.csv + config.json (sem envios_*.csv e erros_*.csv, ~2,3 GB)
                                       o resumo.csv tem a coluna atraso_p99_apos_largada_ms (C16)
figuras/original/                      figuras e comparacao.md como saíram da execução
figuras/comparacao_reanalise/          comparacao.md e figuras com a reanálise C16
logs/                                  execucao.log, contrato.log, calibracao.txt, ambiente.txt,
                                       alteracoes_locais_no_servidor.diff (2 ajustes feitos no servidor)
```

Reproduzir a reanálise a partir deste arquivo:

```bash
python -m ponto.analise.comparar --resultados experimento_1/resultados \
    --saida experimento_1/figuras/comparacao_reanalise --descontar-largada 2
```

## Erros encontrados nesta execução (C16)

Nenhum degrau teve a API reiniciando. Três defeitos do ambiente de medição invalidaram degraus que
estavam bons:

| | Defeito | Evidência | Efeito |
|---|---|---|---|
| a | **Surto de largada do gerador.** O instante zero era fixado 0,5 s à frente antes de a agenda chegar aos processos; a 1500 req/s ou mais, a agenda (60–120 mil registros) demorava mais que isso. | No lote a 1500–2000 req/s, o 1º registro saía 140–480 ms atrasado; atraso p99 de 17–176 ms no degrau, mas de 1,2–6 ms excluídos os 2 s iniciais. | Quase todos os degraus de lote a 1500–2000 req/s marcados `gerador_atrasou`, com a API respondendo em menos de 1 ms (p50). O limite do lote ficou preso em 1000–1500. |
| b | **Portas efêmeras esgotadas** no contêiner de carga depois do baseline saturado (timeouts fecham conexões; cerca de 28 mil portas em TIME_WAIT). | `Cannot assign requested address` em `lote_50` a 100 e 250 req/s (imperativo rep_1 e rep_2) e em `lote_200` a 100 (rep_2), logo depois de `baseline` a 2000. | A rampa parava, e a repetição contava como limite 0 na mediana. |
| c | **Contador `pendentes` vazando na versão Elixir.** Subia antes do `GenServer.call` à fila e só descia na recusa; com a chamada estourando o prazo e a fila recusando depois, nunca descia. | Depois de `lote_50` a 3000 req/s na rep_2, a API nunca mais ficou ociosa: 11 degraus seguidos `fila_nao_drenou`. Causa deduzida do código e dos sintomas; não há logs da API desta execução. | Os "[0–…]" do Elixir na tabela original. Os dados desses degraus parecem normais, mas ficam inválidos. |

O defeito (c) está na casca imperativa da versão Elixir, fora do núcleo funcional, como o B1.

**Reanálise.** (a) pode ser corrigido depois da coleta, porque os `envios_*.csv` têm o horário
agendado e o real de cada requisição: o atraso p99 é medido só depois dos 2 s iniciais. (b) e (c)
não: esses degraus continuam inválidos e as repetições sem limite mensurável ficam fora da mediana
(por isso há `n=3` e `n=4`). Na mesma reanálise, a latência p99 também é medida sem os 2 s iniciais
(coluna `lat_p99_apos_largada_ms`), e um degrau em que o gerador atrasou **porque a API já tinha
saturado** (≥ 1% de erros de carga) passa a contar como válido e reprovado (C17): eram 26 degraus de
baseline a 1500–2000 req/s e 4 de lote a 3000, todos do Elixir. No total, a reanálise revalidou 28
degraus no imperativo, 27 no funcional e 32 no Elixir.

## Resultados (reanálise C16)

Limite em req/s, critério `ok_carga`, mediana [mín–máx] das repetições:

| cenário | imperativo | funcional | Elixir | original (os três) |
|---|---|---|---|---|
| baseline | 1000 | 1000 | 1000 | 1000 |
| lote_50 / 200 / 1000 | 2000 | 2000 | 2000 | 1000–1500 |

Nas versões Python, os degraus de lote a 3000 req/s continuam inválidos (atraso p99 do gerador de
cerca de 200 ms mesmo depois da largada, sem erros de carga), então o limite do lote é **≥ 2000**;
acima disso o teto é do gerador nesta máquina. No Elixir, 4 desses degraus encheram a fila
(`recusado:fila_cheia`) e contam como reprovados: lá o limite de 2000 é real nessas repetições. Com
tão poucos degraus, a diferença fica para o experimento 2 confirmar.
Tabelas completas, pelos três critérios, em `figuras/comparacao_reanalise/comparacao.md`.

Latência p99 das respostas 2xx (ms), depois dos 2 s iniciais, mediana [mín–máx] das repetições, e
p do teste de Mann-Whitney exato (n = 5 contra 5; o menor p possível é 0,008). Tabela completa,
todos os degraus, em `figuras/comparacao_reanalise/comparacao.md`:

| degrau | imperativo | funcional | Elixir | p imp×fun | p fun×Elixir |
|---|---|---|---|---|---|
| baseline, 500 req/s | 8,1 [7,2–11,0] | 13,1 [9,2–15,1] | 6,6 [6,0–7,7] | 0,056 | **0,008** |
| baseline, 1000 req/s | 168 [115–222] | 202 [166–273] | 67 [41–97] | 0,421 | **0,008** |
| lote_200, 1500 req/s | 4,7 [3,0–5,3] | 5,5 [4,3–7,4] | 1,8 [1,5–2,3] | 0,175 | **0,016** |
| lote_200, 2000 req/s | 14,7 [12,1–17,3] | 36,9 [15,1–67,5] | 6,8 [5,3–8,4] | 0,095 | **0,016** |
| lote_1000, 1000 req/s | 1,3 [1,2–1,4] | 1,7 [1,5–2,2] | 0,9 [0,8–1,0] | **0,008** | **0,008** |
| lote_1000, 2000 req/s | 11,4 [9,9–37,0] | 40,7 [17,7–104] | 6,2 [5,0–7,1] | 0,056 | **0,016** |

Cenários de falha a 500 req/s (praticamente iguais nas três implementações e nas 5 repetições):

| cenário | resultado |
|---|---|
| lote, queda de 10 s, com retry | nenhum erro (6 retries) |
| lote, queda de 10 s, sem retry | disponibilidade 1,0 e integridade cerca de 0,50: ~5000 `perda_silenciosa` + ~2400 `cascata_de_perda` |
| lote, quedas de 20 s e 30 s, com retry | ~52 perdidos (um lote, quando as 8 tentativas se esgotam) + 1340 / 6390 `recusado:fila_cheia` |
| baseline, sem retry | ~5000 `recusado:banco_indisponivel` (503) e integridade 1,0 |
| baseline, com retry | ~3400 `processado_sem_confirmacao` (C11) **e 640–1150 erros de integridade, quase todos `saida_antes_da_entrada`** |

## Conclusões preliminares

- **H1 (estilo): confirmada na vazão e nos erros**, com uma ressalva. Limites iguais, mesmos tipos
  e contagens de erro. O funcional tem p99 maior na maioria dos degraus perto da saturação (de 20%
  a quase 4×), mas só um degrau tem diferença significativa (p < 0,05); nos outros, p de 0,06 a 0,4.
  É tendência, não diferença estabelecida.
- **H2 (runtime): confirmada.** O Elixir tem p99 2,5 a 6× menor perto da saturação, com diferença
  significativa contra o Python funcional em quase todos os degraus a partir de 1000 req/s, com os mesmos
  tipos de erro e o mesmo ponto de saturação (o gargalo é o banco, com 1 CPU). Extra: zero
  `ordem_invertida` no baseline a 1000 req/s nas 5 repetições (`sem_erros` 1000, contra 500 do Python).
- **H3 (arquitetura): confirmada.** O lote aguenta pelo menos 2× a vazão do baseline e, com o banco fora e
  sem retry, confirma 202 para cerca de metade de registros que se perdem; o baseline recusa
  explicitamente. Achado novo: **o retry no baseline também gera erros de integridade**, porque
  reordena as gravações (a saída é gravada enquanto a entrada ainda está em retry).

## O que muda para o experimento 2

Com C16 corrigido no código: largada sincronizada do gerador, `sysctls` de portas no contêiner de
carga, repetição automática de degrau que falha por erro de execução, contador de pendentes do Elixir
dentro da fila. A reanálise (`--descontar-largada`) não é mais necessária para resultados novos.

E, a partir da revisão deste experimento contra a proposta (C17): log da API salvo por repetição;
calibração com degraus de 60 s; degraus de 1250, 1750 e 2500 req/s; cenários de **queda real** do
banco; a mesma classificação de erros de conexão nas três APIs (antes, numa queda real, cada uma
reagiria de um jeito); tabela de latência com teste estatístico; métricas de código para H1
(`make metricas`); e o degrau "API saturou" separado de "gerador atrasou".
Para medir acima de 2000 req/s no lote é preciso uma máquina com mais núcleos para o gerador
(perfil de 8 núcleos).
