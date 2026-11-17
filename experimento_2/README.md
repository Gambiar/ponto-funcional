# Experimento 2: execução final (16–17/nov/2026)

Segunda execução da comparação completa (`make comparacao`), no commit `2fe8ae5` (C1–C17), com os
defeitos do [experimento 1](../experimento_1/README.md) corrigidos (C16) e as mudanças da revisão
contra a proposta (C17). **Estes são os números do artigo**; os do experimento 1 ficam como
resultado preliminar.

## Ambiente

| | |
|---|---|
| Máquina | a mesma do experimento 1: VM VMware, 4 vCPUs Intel Xeon Gold 6348 @ 2,60 GHz, 15 GiB, Linux 6.4 (SLES), Docker 28.5.1, Compose 2.22 |
| Perfil de CPU | `compose.4cpu.yml` (C15): banco núcleo 0, API núcleo 1, gerador núcleos 2–3 com 2 processos |
| Desenho | 3 implementações × 5 repetições intercaladas × 13 cenários, degraus de 60 s, rampa de 12 degraus (100 a 6000 req/s), banco novo a cada implementação |
| Duração | 22h23 → 11h54 (cerca de 13h30) |
| Testes | 63 em Python e 16 em Elixir, todos passando (`logs/testes.log`) |
| Contrato (C14) | as três APIs passaram (início de `logs/execucao.log`) |
| Calibração do gerador | cumpre a agenda até 3000 req/s com degraus de 60 s (atraso p99 de 13 ms; 126 ms a 4000) (`logs/calibracao.txt`) |

Única configuração local no servidor: um `.env` com `API_PORTA=127.0.0.1:8010`, porque a porta 8000
estava ocupada por outro serviço. Não altera a medição (o gerador fala com a API pela rede interna do
Compose).

## Conteúdo

```
resultados/<impl>/rep_<k>/<cenario>/   resumo.csv + config.json (sem envios_*.csv e erros_*.csv, ~6,7 GB)
figuras/comparacao/                    comparacao.md (limites, p99 com Mann-Whitney, validade),
                                       codigo.md (métricas de código, H1), comparacao_p99.png, validade.png
figuras/<impl>/rep_<k>/                figuras e resumo.md de cada repetição
logs/                                  execucao.log, calibracao.txt, ambiente.txt, testes.log
logs/api/<impl>_rep_<k>.log.gz         log da API de cada repetição (C17), compactado
```

## Validade da execução

| implementação | degraus | válidos | api_reiniciou | fila_nao_drenou | gerador_atrasou | falha_execucao | API saturou (válido, reprovado) |
|---|---|---|---|---|---|---|---|
| python_imperativo | 259 | 244 (94%) | 0 | 0 | 15 | 0 | 19 |
| python_funcional | 252 | 235 (93%) | 0 | 0 | 17 | 0 | 16 |
| elixir | 256 | 226 (88%) | 0 | 0 | 30 | 0 | 3 |

No experimento 1 eram 73%, 75% e 69%. As correções de C16 eliminaram as três fontes de degraus
inválidos sem relação com a API: nenhuma falha de execução (portas), nenhuma fila presa (contador do
Elixir) e nenhum atraso de largada. Os degraus com `gerador_atrasou` estão todos a 4000 req/s ou mais
(acima do teto calibrado), exceto 3 do funcional a 3000. O Elixir tem mais degraus inválidos porque
**não** saturou a 3000 e 4000 no lote: a rampa seguiu até 6000, onde o gerador não acompanha.

## Resultados

Limite em req/s, critério `ok_carga`, mediana [mín–máx] das repetições (tabelas pelos três critérios
em `figuras/comparacao/comparacao.md`):

| cenário | imperativo | funcional | Elixir | experimento 1 (reanálise) |
|---|---|---|---|---|
| baseline | 1500 [1250–1500] | 1250 [1250–1500] | 1000 [1000–1250] | 1000 |
| lote_50 / 200 / 1000 | 3000 | 3000 | 3000 | ≥ 2000 |

No lote, 3000 req/s é o teto do gerador: o degrau seguinte (4000) é inválido, então o limite é
**≥ 3000** nas três implementações. O defeito de largada (C16a) é o que segurava o experimento 1 em
1000–1500 (original) e 2000 (reanálise).

Latência p99 das respostas 2xx (ms), mediana [mín–máx], e p do teste de Mann-Whitney exato
(n = 5 contra 5; o menor p possível é 0,008). Tabela completa em `figuras/comparacao/comparacao.md`:

| degrau | imperativo | funcional | Elixir | p imp×fun | p fun×Elixir |
|---|---|---|---|---|---|
| baseline, 500 req/s | 10,1 [6,2–12,6] | 9,5 [6,7–11,7] | 6,9 [6,2–8,2] | 0,690 | 0,151 |
| baseline, 1000 req/s | 85,1 [57,0–120,1] | 168,0 [65,9–217,6] | 30,1 [20,3–34,1] | 0,151 | **0,008** |
| lote_200, 1000 req/s | 1,0 [1,0–1,2] | 1,1 [1,1–1,2] | 0,7 [0,6–0,8] | 0,159 | **0,008** |
| lote_200, 1500 req/s | 1,6 [1,4–2,1] | 2,2 [1,7–3,0] | 0,9 [0,8–1,0] | **0,016** | **0,008** |
| lote_200, 2000 req/s | 4,5 [3,2–7,7] | 7,0 [6,6–7,9] | 1,2 [1,0–1,2] | 0,079 | **0,008** |
| lote_200, 2500 req/s | 9,1 [8,4–10,8] | 12,9 [10,2–33,2] | 2,2 [1,8–2,6] | **0,016** | **0,008** |
| lote_200, 3000 req/s | 32,9 [17,1–43,0] | 77,5 [67,4–113,5] | 5,1 [3,5–6,1] | **0,008** | **0,008** |

Cenários de falha a 500 req/s, mediana das 5 repetições (as duas versões Python diferem em menos de 1%):

| cenário | Python: disp. / integr. / perdidos | Elixir: disp. / integr. / perdidos |
|---|---|---|
| baseline, queda simulada de 10 s, sem retry | 0,66 / 1,00 / 0 | 0,66 / 1,00 / 0 |
| baseline, queda simulada de 10 s, com retry | 0,77 / 0,94 / 0 (~3400 `processado_sem_confirmacao`) | 0,77 / 0,94 / 0 |
| baseline, queda **real** de 10 s, sem retry | 0,78 / 0,997 / 0 (~700 `processado_sem_confirmacao`) | 0,66 / 1,00 / 0 |
| lote, queda simulada de 10 s, sem retry | 1,00 / 0,51 / 5006 | 1,00 / 0,50 / 4993 |
| lote, queda **real** de 10 s, sem retry | 1,00 / 0,50 / 5036 | 1,00 / **0,94 / 765** |
| lote, queda simulada ou real de 10 s, com retry | 1,00 / 1,00 / 0 | 1,00 / 1,00 / 0 |
| lote, quedas simuladas de 20 s e 30 s, com retry | 0,94 e 0,77 / 0,995 / 53 | 0,94 e 0,77 / 0,995 / 53 |

Integridade no lote, degraus válidos até 2500 req/s: **nenhum** erro no Elixir; 49 registros no
imperativo (8 degraus) e 23 no funcional (4 degraus), quase todos `divergente:ordem_invertida` no
`lote_50`, inclusive a 100 req/s. Por isso o limite `ok_integridade` do imperativo no `lote_50` tem
mediana 0.

Métricas de código (`figuras/comparacao/codigo.md`): o funcional tem 542 linhas contra 336 do
imperativo, mas 1,3 decisão por função contra 3,3, 42 pontos de mutação compartilhada contra 74 e 53%
de funções isoláveis contra 22%; os núcleos puros (Python e Elixir) são 100% isoláveis.

## Achado: por que o Elixir satura antes no baseline

Os logs da API (C17) mostram de 31 mil a 48 mil avisos por repetição no Elixir:

```
tentativa 1 falhou: [Ponto.Supervisor] connection not available and request was dropped
from queue after 101ms. This means requests are coming in and your connection pool cannot serve them fast enough.
```

Eles se concentram nos primeiros minutos de cada repetição, exatamente nos degraus de 1250 e
1500 req/s do `baseline` (o primeiro cenário da suíte), com um resíduo em `falha_baseline_com_retry`.
O pool do Postgrex (DBConnection) faz *load shedding*: quando a espera por conexão passa do alvo
(`queue_target`, padrão de 50 ms) por um intervalo inteiro, ele descarta as requisições que esperam
mais que o dobro disso. No baseline, cada requisição precisa de uma conexão; perto da saturação, o
Elixir passa a falhar rápido e entrar em retry, o que gera erros de carga (limite menor) e p99 de
segundos a 1250 req/s. O pool do asyncpg não descarta: deixa a requisição esperar até o timeout do
cliente, com latência maior, mas sem erro, até 1250–1500 req/s. É uma diferença de política do
driver, não do estilo nem do escalonador. Não foi testada com outra configuração (`queue_target`
maior ou `pool_size` diferente); fica como próximo passo.

O mesmo comportamento de pool provavelmente explica a queda real sem retry no lote (765 perdidos no
Elixir contra cerca de 5000 no Python): o Postgrex reconecta em segundo plano (`backoff_max` de 1 s,
C17) e segura parte das consultas até a conexão voltar, enquanto o asyncpg falha na hora.

## Conclusões

- **H1 (estilo): confirmada na vazão, nos erros e na estrutura do código, com um custo.** Limites e
  comportamento sob falha iguais nas duas versões Python; código funcional mais isolável e com menos
  decisões por função. O p99 do funcional é maior perto da saturação, agora com diferença
  significativa em 11 das 15 combinações de cenário de lote e taxa entre 1500 e 3000 req/s (no
  experimento 1 era só tendência). Até 1250 req/s, nenhuma diferença significativa.
- **H2 (runtime): confirmada no lote, não no baseline saturado.** O Elixir tem p99 de 1,4 a 15×
  menor no lote de 1000 a 3000 req/s, com p = 0,008 em todas essas taxas no `lote_200`, e nenhum erro
  de integridade no lote. Não aguenta mais carga (mesmo limite) e, no baseline, satura antes por
  causa do pool (achado acima).
- **H3 (arquitetura): confirmada.** O lote aguenta pelo menos 2 a 3× a vazão do baseline e, sem retry,
  confirma 202 para cerca de 5000 registros que se perdem numa queda de 10 s; com retry, nenhuma
  perda enquanto a queda cabe no backoff (16,2 s). O retry no baseline continua gerando
  `processado_sem_confirmacao` (backoff de 16,2 s contra 5 s de timeout do cliente, C11).

## Limitações e próximos passos

- O teto do gerador nesta máquina (3000 req/s) é o limite medido do lote: as APIs podem aguentar
  mais. Medir acima disso exige o perfil de 8 núcleos (`compose.cpuset.yml`).
- Testar o baseline do Elixir com `queue_target` maior ou outro `pool_size`, para confirmar o papel do
  *load shedding* do DBConnection.
- Investigar a origem das `ordem_invertida` no `lote_50` das versões Python (e a ausência delas no
  Elixir).
- Queda real só de 10 s; as de 20 s e 30 s continuam simuladas.
