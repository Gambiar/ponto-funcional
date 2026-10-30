# Ponto Funcional

Trabalho final da disciplina de Programação Funcional (mestrado, UFPR).
Autores: Sergio Andrew Farias, Vinicius Camargo Prattes.

---

## O que é

Um serviço de **registro de ponto eletrônico** (servidores públicos registrando entrada e saída) submetido a um **experimento de carga controlado**, construído para responder a uma pergunta:

> **Usar conceitos de programação funcional muda a velocidade máxima que o serviço aguenta sem erros e a quantidade e o tipo de erros que aparecem quando ele passa desse limite?**

O cenário é realista para o problema: no início de cada turno (7h, 13h, 18h) milhares de pessoas registram ponto quase ao mesmo tempo. O serviço não pode perder registros, gravar duplicatas nem aceitar registros inválidos, e precisa continuar correto mesmo quando o banco de dados cai.

Para responder à pergunta, o **mesmo serviço** foi escrito de três formas e todas passam pelo **mesmo experimento**, que mede vazão, latência e cada erro, registro a registro.

---

## O que foi criado

| # | Componente | Para que serve | Onde |
|---|---|---|---|
| 1 | **Serviço de ponto (API HTTP)** em três versões com o mesmo contrato | objeto de estudo | `src/ponto/` (funcional), `src/ponto_imperativo/` (imperativa), `elixir/` (Elixir) |
| 2 | **Gerador de dados sintéticos com gabarito** | cria servidores e registros fictícios, com anomalias, e o desfecho esperado de cada um | `src/ponto/dados/gerador.py` |
| 3 | **Oráculo** | implementação de referência, sequencial e pura, que calcula o desfecho correto de qualquer conjunto de registros | `src/ponto/nucleo/referencia.py` |
| 4 | **Gerador de carga em malha aberta** e calibração | envia os registros numa taxa exata (req/s) e mede o próprio limite | `src/ponto/carga/rampa.py`, `calibrar.py` |
| 5 | **Reconciliação e taxonomia de erros** | compara o que foi enviado, o que o cliente recebeu e o que ficou no banco, e classifica cada erro | `src/ponto/dados/reconciliacao.py` |
| 6 | **Experimento automatizado** | rampa de taxas, cenários de falha, repetições, critérios de limite | `src/ponto/carga/experimento.py` |
| 7 | **Análise** | figuras e tabelas por implementação e comparativas | `src/ponto/analise/` |
| 8 | **Testes** | unitários e baseados em propriedades (Hypothesis), sem precisar de banco | `tests/` |
| 9 | **Ambiente reprodutível** | Docker Compose com limites fixos de CPU e memória | `docker-compose.yml`, `compose.*.yml`, `Makefile` |
| 10 | **Metodologia e registro de correções** | hipóteses, desenho do experimento e todas as correções feitas no processo | [`docs/metodologia.md`](docs/metodologia.md) |

### As três versões do serviço

| Versão | Ideia | Por que existe |
|---|---|---|
| **Python imperativo** | estado mutável compartilhado, laços, if/elif, regras misturadas com o acesso ao banco | **grupo de controle**: o jeito "tradicional" de escrever o mesmo serviço |
| **Python funcional** | **núcleo funcional** (funções puras, dados imutáveis, pattern matching, funções de ordem superior, recursão) e **casca imperativa** (rede, banco, fila) | a versão principal; mesmo runtime do controle, só muda o **estilo** |
| **Elixir** | linguagem funcional: imutabilidade garantida pela linguagem, processos leves da BEAM, fila como processo `GenServer` | mesmo estilo funcional, outro **runtime** |

Comparar imperativo × funcional (mesmo Python) isola o efeito do **estilo**. Comparar Python funcional × Elixir isola o efeito da **linguagem/runtime**.

---

## A lógica do serviço

Como um registro de ponto é processado, nas três versões:

1. **Chega** um JSON: `{id_evento, servidor, tipo, instante, dispositivo}`.
2. **Interpretar** (função pura): por pattern matching, converte o JSON num registro imutável ou recusa o formato (422).
3. **Validar** (função pura): as regras são funções guardadas numa lista; vale a primeira violada:
   tipo diferente de entrada/saída → `tipo_invalido`; servidor fora do cadastro → `servidor_inexistente`; antes das 6h → `fora_da_jornada`.
4. **Encaminhar**, conforme o modo:
   - **baseline**: grava na própria requisição e responde 201 com o desfecho;
   - **lote**: põe numa fila e responde **202 (aceito)** na hora. Se a fila estiver cheia, responde 503 (*back-pressure*). Um consumidor junta até N registros ou espera até T ms e grava o lote.
5. **Gravar** numa única transação: ordenar por horário (em duplicatas, o mais antigo vence), inserir entradas, consultar quais servidores têm entrada no dia, rejeitar saídas sem entrada, inserir saídas e **decidir o desfecho** de cada registro (função pura): `gravado`, `descartado:duplicado` ou `rejeitado:<motivo>`.
6. **Resiliência**, composta em camadas sobre a gravação (funções de ordem superior): **retry** com espera exponencial se o banco estiver fora; **falha simulada** para o experimento; e **bisseção recursiva**, que divide o lote ao meio até isolar um registro corrompido, gravando todo o resto.

A ideia central da versão funcional é que **toda decisão de negócio é uma função pura** (sem banco, rede ou relógio). Isso permite testar as regras sem infraestrutura e, principalmente, escrever um **oráculo** que diz qual seria o resultado correto, contra o qual qualquer versão pode ser conferida.

---

## A lógica do experimento

```
para cada implementação, repetição, cenário e taxa (req/s):
  1. gerar base sintética nova + gabarito (semente fixa → reprodutível)
  2. zerar banco e cadastro; configurar a API (modo, lote, tentativas)
  3. disparar a base na taxa alvo, em malha aberta (opcional: derrubar o banco no segundo 5)
  4. esperar a API terminar de gravar tudo
  5. ler o banco e reconciliar registro a registro
  6. calcular métricas e decidir se o degrau passou → próxima taxa
```

Três decisões sustentam a validade da medição:

- **Malha aberta:** cada requisição sai no horário agendado, mesmo que as anteriores não tenham respondido. Se o gerador esperasse as respostas, um servidor lento reduziria a carga sem ninguém perceber e a saturação ficaria escondida.
- **Gabarito + oráculo:** existem duas definições independentes do resultado correto (a que o gerador construiu e a que o oráculo calcula), e um teste garante que concordam.
- **Esperado ajustado:** se a API recusou a entrada de um servidor (503), rejeitar a saída dele é **correto**. Por isso o esperado é recalculado pelo oráculo só com o que de fato entrou no sistema, separando **erros de carga** (o registro nem entrou) de **erros de integridade** (entrou e foi processado errado ou perdido).

Cada registro termina numa categoria: `correto`, erros de carga (`recusado:fila_cheia`, `timeout`, `processado_sem_confirmacao`...) ou erros de integridade (`perda_silenciosa`, `divergente:saida_antes_da_entrada`...). A tabela completa está em [Taxonomia de erros](#taxonomia-de-erros).

---

## Metodologia (resumo)

**Hipóteses**, escritas antes das execuções finais:

| | Comparação | Hipótese |
|---|---|---|
| **H1** | imperativo × funcional (estilo) | vazão e erros sob carga **não** mudam, porque o gargalo é o banco e os erros vêm da arquitetura. O ganho do estilo funcional aparece em testabilidade e clareza. |
| **H2** | Python funcional × Elixir (runtime) | Elixir mantém a latência de cauda (p99) menor perto da saturação; os tipos de erro não mudam. |
| **H3** | baseline × lote (arquitetura) | o lote aguenta mais carga, mas troca durabilidade por vazão: sob queda do banco, perde registros já confirmados (202). |

**Variáveis.**
Independentes: implementação, modo (baseline/lote), tamanho do lote, taxa de requisições, duração da queda do banco, retry ligado ou desligado.
Dependentes: limite de taxa (por três critérios: carga, integridade e estrito), latência p50/p95/p99 (com e sem timeouts), disponibilidade, integridade e contagem por categoria de erro.
Controladas: mesmo contrato HTTP, SQL, dados, gerador de carga e limites de CPU (API 1, banco 2, carga 2); um único consumidor da fila; um escalonador na BEAM.

**Rigor.** 5 repetições com sementes diferentes (mediana [mín–máx]); degraus de 60 s; calibração do gerador e descarte dos degraus em que ele atrasou (> 20 ms p99); tolerância explícita para erros de integridade (10⁻⁴).

**Ameaças à validade.** Compressão de tempo (um dia enviado em segundos), uma única máquina, dados sintéticos, falha simulada em vez de queda real. Ver [Limitações](#limitações-ameaças-à-validade).

O desenho completo e o **registro de todas as correções** feitas ao longo do trabalho (bugs B1–B5 e correções de método C1–C11, com o problema, a evidência e o que mudou) estão em [`docs/metodologia.md`](docs/metodologia.md). As correções fazem parte do resultado: várias só apareceram porque o núcleo puro, o oráculo e os testes de propriedade tornaram os erros visíveis.

### Estado atual

- Versões Python: 43 testes passando.
- Versão Elixir: escrita, ainda **não compilada nem executada** (aguarda o ambiente Docker).
- `exemplo/`: resultados de uma execução **anterior** às correções metodológicas; servem para mostrar a evolução do método, não como resultado final.

---

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

## Fluxo detalhado e regras de negócio

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
