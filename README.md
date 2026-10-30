# Ponto Funcional

Pipeline de registro de ponto em Python, estruturado como **núcleo funcional e casca imperativa**, com experimento automatizado que mede **até qual taxa de requisições o serviço opera sem erros** e **mapeia os tipos de erro** que surgem depois desse limite.

Trabalho final da disciplina de Programação Funcional (UFPR).
Autores: Sergio Andrew Farias, Vinicius Camargo Prattes.

---

> Metodologia detalhada, hipóteses e registro de todas as correções: [`docs/metodologia.md`](docs/metodologia.md).

## Como rodar

Requisito: Docker com Docker Compose (Linux, macOS ou Windows). Nada mais precisa ser instalado.

```bash
docker compose up -d --build --wait db api                                   # 1. sobe banco e API
docker compose run --rm --no-deps --entrypoint pytest carga -q                # 2. testes
docker compose run --rm carga ponto.carga.experimento --suite padrao          # 3. experimentos (~15-25 min)
docker compose run --rm carga ponto.analise.graficos                          # 4. figuras
docker compose down                                                           # 5. desliga
```

Com `make`: `make subir`, `make testes`, `make experimento`, `make graficos`, ou `make tudo`.

Para conferir rapidamente se o ambiente funciona (~2 min):

```bash
docker compose run --rm carga ponto.carga.experimento --cenario rapido --taxas 100,500,1000 --duracao 10
```

Em máquinas modestas, reduza as taxas da suíte: `--suite padrao --escala 0.5`.

Resultados ficam em `resultados/` e figuras em `figuras/`.

---

## O que o sistema faz

```
Gerador de carga ──POST /registros──▶ API (FastAPI)
                                        │
                                        ▼
                         interpretar ─▶ validar          (núcleo, funções puras)
                                        │
                     ┌──────────────────┴──────────────────┐
              modo "baseline"                         modo "lote"
       grava na própria requisição          asyncio.Queue (back-pressure: 503 se cheia)
                     │                                     │
                     │                      consumidor junta N registros ou espera T ms
                     └──────────────────┬──────────────────┘
                                        ▼
                     retry com backoff ─▶ gravar lote (PostgreSQL, 1 transação)
                                        │
                     decisões de desfecho (núcleo, funções puras)
```

Regras de negócio (desfechos possíveis de cada registro):

| Situação | Desfecho |
|---|---|
| Registro válido | `gravado` |
| Mesmo servidor, tipo e dia já gravado | `descartado:duplicado` |
| Tipo diferente de entrada/saída | `rejeitado:tipo_invalido` |
| Servidor fora do cadastro | `rejeitado:servidor_inexistente` |
| Antes das 6h | `rejeitado:fora_da_jornada` |
| Saída sem entrada no dia | `rejeitado:saida_sem_entrada` |

---

## Conceitos de programação funcional no código

| Conceito | Onde |
|---|---|
| Funções de primeira classe | `nucleo/validacao.py`: regras são funções numa lista; `dados/gerador.py`: dicionário `ANOMALIAS` de funções; `casca/fila.py`: configuração passada como funções |
| Funções de ordem superior | `criar_validador`, `regra_servidor`, `regra_jornada` (fábricas/closures); decoradores `com_retry` e `com_falha_simulada` em `util/retry.py` |
| Funções nomeadas e anônimas | `def` nas regras; `lambda` em `regra_servidor`, `ordenar`, `separar_saidas`, `desfechos_esperados` |
| Pattern matching | `interpretar` (padrão estrutural sobre dict), `regra_tipo`, `desfecho` (padrões de classe com guarda), `categorizar` (tuplas), `gravar_isolando_falhas` (padrão de sequência) |
| Recursão | `particionar` (divisão e conquista, profundidade log n), `gravar_isolando_falhas` (bisseção recursiva para isolar registro corrompido) |
| Processamento de coleções | `map`, `filter`, `next`, `reduce`, `groupby`, compreensões em todo o núcleo |
| Imutabilidade | `@dataclass(frozen=True)`, `frozenset`, `NamedTuple`; o oráculo dobra (`reduce`) um estado imutável |

O núcleo (`src/ponto/nucleo/`) não acessa rede, banco nem relógio, por isso é testado sem infraestrutura.

---

## Base sintética e gabarito

`ponto.dados.gerador` cria servidores fictícios (IDs sequenciais), cada um com entrada e saída concentradas nos inícios de turno (7h, 13h, 18h). Uma fração (padrão 5%) recebe uma anomalia. **Cada registro sai com o desfecho esperado** (`gabarito.csv`). A geração usa semente fixa, então é reprodutível.

```bash
docker compose run --rm carga ponto.dados.gerador --servidores 40000 --anomalias 0.05 --saida dados
```

Há duas especificações independentes do comportamento correto: o gabarito construído pelo gerador e o **oráculo** (`nucleo/referencia.py`), uma implementação sequencial de referência. Um teste confirma que ambas concordam.

---

## Experimento

Para cada taxa da rampa (`ponto.carga.experimento`):

1. gera uma base nova com gabarito;
2. reinicia o banco e configura a API (modo, tamanho do lote, retry);
3. envia a base na taxa alvo, em **malha aberta** (cada requisição sai no horário agendado, mesmo que as anteriores não tenham respondido, para não mascarar a saturação);
4. espera a fila esvaziar;
5. lê o banco e reconcilia cada registro.

A rampa para depois de dois degraus seguidos reprovados (em carga, em integridade ou por atraso do gerador).

### Cenários da suíte padrão

| Cenário | Descrição |
|---|---|
| `baseline` | um `INSERT` por requisição, sem fila |
| `lote_50`, `lote_200`, `lote_1000` | fila + gravação em lotes de tamanhos diferentes |
| `falha_com_retry` | 500 req/s; banco indisponível por 10 s a partir do 5º segundo; 8 tentativas com backoff |
| `falha_sem_retry` | igual, com 1 tentativa |
| `falha_com_retry_20s`, `falha_com_retry_30s` | quedas mais longas que o backoff acumulado (16,2 s) |
| `falha_baseline_com_retry`, `falha_baseline_sem_retry` | a mesma queda no modo baseline (grupo de comparação de durabilidade) |

A falha é simulada pela API (`POST /admin/falha`), então funciona em qualquer máquina. Também é possível derrubar o banco de verdade durante um teste com `docker compose stop db` e `docker compose start db`.

### Taxonomia de erros

A reconciliação compara três coisas: o que foi enviado, o que o cliente recebeu e o que ficou no banco. Para separar erros em cascata, o esperado é recalculado pelo oráculo considerando só os registros que de fato chegaram ao sistema.

| Categoria | Significado | Componente |
|---|---|---|
| `recusado:fila_cheia` | API recusou (503) por back-pressure; o cliente sabe e pode reenviar | fila |
| `recusado:banco_indisponivel` | 503 no modo baseline após esgotar tentativas | banco |
| `timeout` / `falha_conexao` | cliente desistiu ou não conectou | API (saturação) |
| `processado_sem_confirmacao` | cliente viu erro, mas o registro foi gravado | API |
| `perda_silenciosa` | API respondeu sucesso, mas o registro não está no banco | persistência |
| `divergente:cascata_de_perda` | registro processado errado porque outro do mesmo servidor se perdeu (ex.: a entrada sumiu, a saída foi rejeitada) | persistência |
| `divergente:saida_antes_da_entrada` | saída processada antes de a entrada ser gravada | concorrência |
| `divergente:ordem_invertida` | duplicata gravada no lugar do registro original | concorrência |

Métricas por degrau:

- **disponibilidade**: fração de requisições aceitas (2xx);
- **integridade**: entre os aceitos, fração processada corretamente;
- **latência**: p50/p95/p99 das respostas 2xx e `lat_p99_todas_ms` (inclui timeouts);
- **validade**: `gerador_valido` é falso quando o gerador atrasou mais de 20 ms (p99) em relação à agenda.

O **limite** do cenário é a maior taxa antes do primeiro degrau reprovado, contando só degraus com gerador válido, por três critérios:
`ok_carga` (nenhum erro de carga), `ok_integridade` (nenhuma perda ou divergência estrutural e taxa de erro ≤ 10⁻⁴) e `sem_erros` (todos os registros corretos). Detalhes em [`docs/metodologia.md`](docs/metodologia.md).

### Arquivos gerados

```
resultados/<cenario>/
  config.json         parâmetros
  resumo.csv          uma linha por taxa (latências, disponibilidade, integridade, contagem por categoria)
  envios_<taxa>.csv   cada requisição: horário agendado e real, latência, status
  erros_<taxa>.csv    cada registro com erro: categoria, esperado, obtido, componente
figuras/
  latencia_p99.png  correcao.png  mapa_de_erros.png  falha_linha_do_tempo.png  resumo.md
```

---

## Comparação entre implementações

Para separar o efeito do **estilo funcional** do efeito do **runtime funcional**, a mesma API existe em três versões, com contrato HTTP, esquema de banco, gerador de carga e reconciliação idênticos:

| Implementação | Onde | O que muda |
|---|---|---|
| `python_imperativo` | `src/ponto_imperativo/api.py` | grupo de controle: sem núcleo puro, estado mutável, laços, if/elif, retry inline, bisseção iterativa |
| `python_funcional` | `src/ponto/` | núcleo puro + casca imperativa (versão principal) |
| `elixir` (em validação: ainda não executada) | `elixir/` | linguagem funcional: dados imutáveis, pattern matching nativo, fila como processo GenServer, Bandit + Postgrex |

```bash
make comparacao          # calibra o gerador, roda a suíte nas três versões (5 repetições × 60 s)
                         # e gera todas as figuras
make comparacao REPETICOES=1 DURACAO=20   # versão rápida para conferir o ambiente
```

Saídas:

```
resultados/<impl>/rep_<k>/<cenario>/   resumo.csv, envios_<taxa>.csv, erros_<taxa>.csv, config.json
figuras/<impl>/rep_<k>/                latencia_p99.png, correcao.png, mapa_de_erros.png,
                                       falha_linha_do_tempo.png, resumo.md (limites pelos 3 critérios)
figuras/comparacao/                    comparacao.md (limites: mediana [mín–máx] por implementação),
                                       comparacao_p99.png
```

Ou, passo a passo (troca só o serviço `api`):

```bash
docker compose up -d --build --wait db api
docker compose run --rm --no-deps carga ponto.carga.experimento --suite padrao --saida resultados/python_funcional
docker compose -f docker-compose.yml -f compose.imperativo.yml up -d --build --wait db api
docker compose run --rm --no-deps carga ponto.carga.experimento --suite padrao --saida resultados/python_imperativo
docker compose -f docker-compose.yml -f compose.elixir.yml up -d --build --wait db api
docker compose run --rm --no-deps carga ponto.carga.experimento --suite padrao --saida resultados/elixir
docker compose run --rm --no-deps carga ponto.analise.graficos --tudo
docker compose run --rm --no-deps carga ponto.analise.comparar
```

Para o artigo, acrescente `--repeticoes 5 --duracao-suite 60` a cada `ponto.carga.experimento` (é o que o `make comparacao` faz).

A API Elixir roda com `+S 1:1` (um escalonador), para disputar a mesma fatia de CPU (`cpus: 1`) que o processo único do Uvicorn. Compare medianas e dispersão entre as repetições: diferenças de poucos registros entre execuções únicas são ruído.

## Estrutura

```
src/ponto/                 versão funcional (principal)
  nucleo/                  funções puras: modelos, validação, lotes, oráculo
  casca/                   API, fila, repositório (efeitos)
  util/retry.py            decoradores de retry e de falha simulada
  dados/                   gerador com gabarito, reconciliação
  carga/                   gerador de carga em malha aberta, experimento, calibração
  analise/                 figuras por pasta de resultados, comparação entre implementações
src/ponto_imperativo/      versão imperativa (grupo de controle)
elixir/                    versão Elixir (mix, Dockerfile próprio)
compose.*.yml              trocam o serviço api pela versão imperativa ou Elixir
docs/metodologia.md        hipóteses, métodos e registro de correções
exemplo/                   resultados de uma execução anterior às correções metodológicas
tests/                     pytest + Hypothesis
```

## Configuração

Variáveis do serviço `api` no `docker-compose.yml`: `MODO`, `TAMANHO_LOTE`, `ESPERA_MS`, `TENTATIVAS`, `FILA_CAPACIDADE`, `CONSUMIDORES`, `POOL_MAX`. Os quatro primeiros também mudam em execução por `POST /admin/config`.

Os contêineres têm limite de CPU e memória (API: 1 CPU; banco: 2 CPUs; carga: 2 CPUs) para que os resultados sejam comparáveis entre máquinas.

## Limitações (ameaças à validade)

- **Compressão de tempo:** a base representa um dia inteiro, enviado em segundos. Entrada e saída do mesmo servidor ficam muito mais próximas do que na realidade, o que favorece erros de concorrência como `saida_antes_da_entrada` e `ordem_invertida` (cliques duplos que na base distam até 50 s chegam ao servidor com milissegundos de diferença).
- **Uma única máquina:** gerador de carga, API e banco disputam o mesmo hardware, mesmo com limites por contêiner. Verifique a coluna `atraso_gerador_p99_ms`: se for alta, o gerador é o gargalo.
- **Dados sintéticos** podem não reproduzir todos os padrões reais.
- **Python:** sem otimização de chamada de cauda (recursão limitada a ~1000 níveis; por isso só há recursão de profundidade logarítmica), GIL (mitigado por I/O assíncrono) e imutabilidade por convenção.
- **Um worker Uvicorn:** a fila vive na memória do processo. Um registro aceito (202) se perde se o processo cair antes de gravar.
