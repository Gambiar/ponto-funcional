# Metodologia e registro de correções

Este documento descreve como o experimento está estruturado e registra **todas as correções** feitas ao longo do trabalho, com o problema encontrado, a evidência e o que mudou. As correções fazem parte do resultado: várias delas só apareceram porque o núcleo funcional, o oráculo e os testes de propriedade tornaram os erros visíveis.

Identificadores usados no código (comentários `(C3)`, `(C5)` etc.) apontam para as seções abaixo.

---

## 1. Pergunta e hipóteses

**Pergunta.** Aplicar conceitos de programação funcional (PF) a um pipeline de registro de ponto muda (a) a vazão máxima sem erros e (b) a quantidade e o tipo de erros sob carga?

A pergunta mistura dois efeitos, então o desenho os separa:

| Comparação | Isola o efeito de | Hipótese |
|---|---|---|
| Python imperativo × Python funcional | **estilo** (núcleo puro, imutabilidade, funções de ordem superior), com o mesmo runtime | **H1:** vazão e erros sob carga **não** diferem de forma relevante, porque o gargalo é I/O e banco, e os erros vêm da arquitetura, não do estilo. A diferença aparece em testabilidade e complexidade do código. |
| Python funcional × Elixir | **runtime/linguagem funcional** (BEAM: processos leves, escalonamento preemptivo, imutabilidade garantida) | **H2:** Elixir mantém latência de cauda (p99) menor perto da saturação, pelo escalonamento justo, sem mudar os tipos de erro de integridade, que dependem da arquitetura (fila, 202 antes de persistir). |
| baseline × lote (dentro de cada implementação) | **arquitetura** | **H3:** o lote aumenta a vazão, mas troca durabilidade por desempenho: sob falha do banco, o lote produz perda silenciosa e o baseline não. |

As hipóteses foram escritas antes das execuções finais, para que a análise não seja ajustada aos resultados.

---

## 2. Sistema avaliado

```
gerador de carga ──POST /registros──▶ API ──▶ interpretar ▶ validar ──┬── baseline: grava na requisição (201)
                                                                     └── lote: fila (202) ▶ consumidor ▶ grava em lote
                                                       retry com backoff ▶ PostgreSQL (1 transação por lote)
```

Regras de negócio: um registro por servidor, tipo e dia (os demais são `descartado:duplicado`); rejeição por `tipo_invalido`, `servidor_inexistente`, `fora_da_jornada` (antes das 6h) e `saida_sem_entrada`.

### Três implementações com o mesmo contrato

| Implementação | Caminho | Características |
|---|---|---|
| `python_imperativo` | `src/ponto_imperativo/api.py` | grupo de controle: um objeto com todo o estado mutável, laços com acumuladores, if/elif, retry inline, bisseção iterativa com pilha explícita. Não importa nada de `ponto.*`. |
| `python_funcional` | `src/ponto/` | núcleo puro (`nucleo/`: dataclasses congeladas, `match`, closures, `reduce`, recursão logarítmica) + casca imperativa (`casca/`). Retry e falha simulada como decoradores. |
| `elixir` | `elixir/` | núcleo puro em `Ponto.Nucleo`; fila como processo `GenServer` com estado imutável; retry, falha e tradução de erros compostos com `\|>`; contadores atômicos; Bandit + Postgrex. |

Fixos entre as implementações: endpoints HTTP e corpos de resposta, esquema e SQL, limites de contêiner (API 1 CPU, banco 2 CPUs, carga 2 CPUs), parâmetros (`TAMANHO_LOTE`, `ESPERA_MS`, `TENTATIVAS`, `FILA_CAPACIDADE`, `POOL_MAX`). A BEAM roda com `+S 1:1` (um escalonador), equivalente ao processo único do Uvicorn.

---

## 3. Dados sintéticos e gabarito

`ponto.dados.gerador` (semente fixa, reprodutível):

- servidores com IDs sequenciais `1..n`; cada um tem entrada num início de turno (7h, 13h ou 18h, desvio de 4 min) e saída cerca de 4h depois (desvio de 5 min); tudo num único dia, sem cruzar a meia-noite;
- uma fração (padrão 5%) recebe uma anomalia, sorteada uniformemente entre: duplicata (+1 a 50 s), tipo inválido, registro de madrugada, servidor fora do cadastro e saída sem entrada;
- **cada registro sai com o desfecho esperado** (gabarito), construído pela própria anomalia;
- `n = taxa × duração / 2,05`, com cerca de 2,05 registros por servidor, de modo que cada degrau envia `taxa × duração` registros.

**Duas especificações independentes.** O gabarito (construído) e o oráculo `nucleo/referencia.py` (implementação sequencial que dobra um estado imutável por servidor) precisam concordar. Isso é verificado em `test_gabarito_do_gerador_coincide_com_oraculo`, com 30% de anomalias.

---

## 4. Geração de carga

`ponto.carga.rampa.disparar`, em **malha aberta**: o registro *i* é agendado para `i / taxa` segundos, e o envio acontece no horário mesmo que as respostas anteriores não tenham chegado. Isso evita a *coordinated omission*, em que um servidor lento reduz a carga sem ninguém perceber.

- **Taxa constante:** o agendamento usa a posição na lista, não o horário do registro (ver C10).
- **Validade do gerador:** cada degrau registra o atraso p99 entre o horário agendado e o envio real. Acima de 20 ms (`--atraso-max`), o degrau é marcado `gerador_valido=False` e não conta para o limite (C3).
- **Calibração:** `make calibrar` mede, contra um servidor nulo (`eco`), a taxa máxima que o gerador sustenta. Esse teto deve ser reportado no artigo.

---

## 5. Procedimento por degrau

Para cada cenário e taxa (`ponto.carga.experimento`):

1. gera uma base nova com gabarito (semente `seed + taxa`);
2. configura a API (modo, lote, tentativas) e espera que ela fique ociosa, sem fila e sem requisições em curso, para que requisições atrasadas do degrau anterior não caiam no banco novo;
3. reinicia o banco (`TRUNCATE`) e o cadastro;
4. dispara a carga, injetando a falha no segundo `falha_em` quando o cenário pede;
5. espera a fila esvaziar;
6. lê a tabela `eventos` (um desfecho por evento) e reconcilia cada registro.

A rampa para depois de 2 degraus seguidos reprovados (em carga, integridade ou validade do gerador).

---

## 6. Reconciliação e taxonomia de erros

Para cada registro, `ponto.dados.reconciliacao` compara três fontes: o que foi **enviado**, o que o **cliente recebeu** e o que ficou **no banco**.

**Esperado ajustado.** O oráculo é recalculado só sobre os registros que chegaram ao sistema (2xx ou presentes no banco). Assim, se uma entrada foi recusada com 503, rejeitar a saída correspondente é o comportamento **correto**, e não um erro em cascata.

| Categoria | Tipo | Significado |
|---|---|---|
| `recusado:fila_cheia`, `recusado:banco_indisponivel` | carga | 503 explícito: o cliente sabe e pode reenviar |
| `timeout`, `falha_conexao` | carga | o cliente desistiu ou não conectou |
| `processado_sem_confirmacao` | carga | o cliente viu erro, mas o registro foi gravado (C1) |
| `perda_silenciosa` | integridade | a API respondeu 2xx e o registro não está no banco |
| `divergente:cascata_de_perda` | integridade | registro processado errado porque outro do mesmo servidor se perdeu |
| `divergente:saida_antes_da_entrada` | integridade | concorrência: a saída foi processada antes de a entrada ser gravada |
| `divergente:ordem_invertida` | integridade* | a duplicata foi gravada no lugar do original (*dominado pela compressão de tempo, C6) |

### Métricas por degrau

| Métrica | Definição |
|---|---|
| `taxa_obtida` | registros enviados ÷ instante do último envio (C2) |
| `atraso_gerador_p99_ms`, `gerador_valido` | validade do degrau (C3) |
| `lat_p50/p95/p99_ms` | latência das respostas 2xx |
| `lat_p99_todas_ms` | latência p99 de todas as requisições, incluindo timeouts (C4) |
| `disponibilidade` | aceitos (2xx) ÷ enviados |
| `integridade` | 1 − erros de integridade ÷ aceitos (C1) |
| `taxa_erro_integridade`, `erros_de_integridade_sem_ordem` | base dos critérios (C5, C6) |
| `retries`, `perdidos_servidor`, `lote_medio` | contadores internos da API (B1) |

### Critérios de "limite" (C5)

O limite de um cenário é a maior taxa antes do primeiro degrau reprovado, considerando só degraus com `gerador_valido`.

| Critério | Passa quando |
|---|---|
| `ok_carga` | `erros_de_carga == 0` |
| `ok_integridade` | nenhum erro estrutural (perda, cascata, saída antes da entrada) **e** `taxa_erro_integridade ≤ 10⁻⁴` |
| `sem_erros` | todos os registros corretos (critério estrito original, mantido para comparação) |

---

## 7. Cenários

| Cenário | Modo | Taxas (req/s) | Falha | Tentativas | Objetivo |
|---|---|---|---|---|---|
| `baseline` | baseline | 100 → 3000 | — | 8 | referência sem fila |
| `lote_50`, `lote_200`, `lote_1000` | lote | 100 → 3000 | — | 8 | efeito do tamanho do lote |
| `falha_com_retry` | lote | 500 | 10 s a partir de 5 s | 8 | recuperação com retry |
| `falha_sem_retry` | lote | 500 | 10 s | 1 | perda sem retry |
| `falha_com_retry_20s`, `_30s` | lote | 500 | 20 s, 30 s | 8 | onde o retry deixa de bastar (C8) |
| `falha_baseline_com_retry`, `_sem_retry` | baseline | 500 | 10 s | 8 / 1 | grupo de comparação de durabilidade (C7) |

Execução completa para o artigo:

```bash
make calibrar                                   # teto do gerador
# para cada implementação (ver README, "Comparação entre implementações"):
docker compose run --rm --no-deps carga ponto.carga.experimento \
    --suite padrao --repeticoes 5 --duracao-suite 60 --saida resultados/<impl>
docker compose run --rm --no-deps carga ponto.analise.comparar
```

---

## 8. Análise

- **Limites:** mediana entre repetições, com mínimo e máximo (`ponto.analise.comparar`), para cada critério separadamente.
- **Latência:** curva p99 × taxa, com a mediana das repetições, em escala log. Reportar também `lat_p99_todas_ms`.
- **Erros:** contagem por categoria e componente (`mapa_de_erros.png`).
- **Código (H1):** linhas de código, complexidade ciclomática e número de pontos de mutação compartilhada por implementação. Ferramentas sugeridas: `radon` para Python e `mix credo` ou contagem manual para Elixir.
- Diferenças menores que a dispersão entre repetições **não** devem ser interpretadas.

---

## 9. Registro de correções

### 9.1 Bugs de código

| ID | Problema | Como foi encontrado | Correção |
|---|---|---|---|
| **B1** | A coluna `retries` saía sempre 0. Em `/admin/estado`, `**asdict(contadores)` vinha depois de `"retries": estado.retries` e o sobrescrevia com `Contadores.retries`, que nunca era incrementado. | O cenário `falha_com_retry` mostrava `retries=0`, embora tivesse se recuperado de 10 s de queda. | Campo duplicado removido de `Contadores` (`casca/fila.py`). |
| **B2** | O teste `test_reenvio_nao_muda_o_que_foi_gravado` afirmava uma propriedade **falsa**. | Contraexemplo construído à mão: saída `a` e entrada `b` no mesmo instante; o desempate por id processa a saída primeiro (rejeitada) e o reenvio `a-r`, 1 s depois, é gravado legitimamente. O Hypothesis não encontrou o caso por ser raro (mesmo servidor, mesmo minuto, ids em ordem desfavorável). | A propriedade foi reformulada como "o reenvio nunca regrava uma chave já gravada", e o contraexemplo virou teste (`test_reenvio_pode_gravar_saida_antes_rejeitada`). |
| **B3** | O `.gitignore` ignorava `resultados/` e `figuras/` em qualquer pasta, deixando `exemplo/` fora do repositório. | Revisão do primeiro commit. | Padrões restritos à raiz (`/resultados/`). |
| **B4** | A versão Elixir consultava as entradas existentes **antes** de inserir as entradas do próprio lote, o que faria saídas do mesmo lote serem rejeitadas. | Revisão do código antes do primeiro build. | Ordem igual à da versão Python: inserir entradas, consultar e depois inserir saídas. |

### 9.2 Correções metodológicas

| ID | Problema | Evidência | Correção |
|---|---|---|---|
| **C1** | `processado_sem_confirmacao` (o cliente viu timeout, mas o registro foi gravado) não contava nem como erro de carga nem como erro de integridade, e entrava no denominador da `integridade`, ao contrário do que a documentação dizia ("entre os aceitos"). | Baseline a 1000 req/s: `erros_de_carga = 0` com 6271 timeouts no cliente. | "Aceitos" passa a significar 2xx. Erro de carga = enviados − aceitos. Integridade calculada sobre os aceitos. |
| **C2** | `taxa_obtida` dividia os envios pela duração **incluindo a espera pelas respostas**, e por isso media latência, não taxa de envio. | Baseline: 762 req/s a 1000 e 839 a 1500, embora o gerador envie no horário. | Calculada até o último envio. A duração com respostas fica em `duracao_envio_s`. |
| **C3** | O gerador de carga (um processo aiohttp) saturava antes da API, então os limites acima de cerca de 1500 req/s mediam o gerador. | Atraso p99 do gerador de 100 a 213 ms a 2000 req/s e de 6,5 a 9,7 s a 3000. | Coluna `gerador_valido` (atraso p99 ≤ 20 ms); degraus inválidos não contam para o limite. Novo `ponto.carga.calibrar` + serviço `eco` para medir o teto do gerador. |
| **C4** | O p99 considerava só respostas 2xx (viés de sobrevivência): quanto pior o sistema, mais timeouts são excluídos e melhor o p99 parece. | — | Nova coluna `lat_p99_todas_ms`, incluindo timeouts e erros. |
| **C5** | "Limite sem erros" com tolerância zero misturava carga e integridade, e um único registro decidia o resultado. | `lote_200` teve limite 1000 por causa de **2** `ordem_invertida` entre 29.700 registros. | Critérios separados (`ok_carga`, `ok_integridade` com tolerância de 10⁻⁴); `sem_erros` mantido como critério estrito. |
| **C6** | `ordem_invertida` é dominada pela compressão de tempo: o dia (7h–22h) é enviado em 20 s (cerca de 2700×), e duplicatas com 1 a 50 s de intervalo chegam com 0,4 a 18 ms de diferença, quando requisições concorrentes podem chegar fora de ordem na rede. | Todos os erros dos modos lote até 2000 req/s são `ordem_invertida`. | Reportada à parte (`erros_de_integridade_sem_ordem`); entra no critério só pela tolerância. Fica documentada como ameaça à validade. |
| **C7** | Faltava o grupo de comparação para durabilidade: só o modo lote era testado sob falha. | — | Cenários `falha_baseline_com_retry` e `falha_baseline_sem_retry`. No baseline, a falha vira 503, que o cliente vê. No lote, vira perda silenciosa após o 202 (H3). |
| **C8** | O resultado "com retry, zero perda" era garantido por construção: 8 tentativas acumulam 0,2+0,4+…+5+5 = 16,2 s de backoff, que cobrem a queda de 10 s. | — | Cenários com queda de 20 s e 30 s. A 500 req/s, a fila de 10 mil também enche em cerca de 20 s. |
| **C9** | Uma execução por cenário, sem medida de dispersão; degraus de 20 s talvez curtos para o regime estável da fila. | Diferenças entre `lote_50/200/1000` menores que o ruído esperado. | `--repeticoes N` (sementes diferentes, em `rep_k/`); `--duracao-suite 60`; `comparar` reporta mediana [mín–máx]. |
| **C10** | Os picos de turno (7h, 13h, 18h) não produziam picos de carga: o envio é agendado pela posição na lista. | Leitura de `rampa.disparar`. | Decisão: o experimento é descrito como **taxa constante**. Os turnos afetam só a ordem dos registros. Agendar pelo horário do registro fica como trabalho futuro. |

### 9.3 Limitações conhecidas (ameaças à validade)

- **Oráculo e sistema compartilham as regras** (`regras_padrao`) na versão funcional: um bug de regra não aparece no esperado ajustado, só em `acerto_gabarito`. Para as versões imperativa e Elixir, o oráculo é independente.
- **Falha simulada** dentro da API, e não queda real do banco. Recomenda-se ao menos uma execução com `docker compose stop db` (erros de pool e transação interrompida).
- **Uma única máquina:** os limites de CPU somam 5 núcleos dentro da VM do Docker Desktop (WSL2). Reportar CPU, RAM e configuração do WSL.
- **Ordem fixa dos degraus**, do menor para o maior, sem reiniciar a API: há efeito de aquecimento, pequeno.
- **Dados sintéticos** num único dia; não exercitam virada de dia nem múltiplos dias.
- **Um processo na API:** a fila vive na memória, e um 202 se perde se o processo cair (vale para as três implementações).
- **Python:** imutabilidade por convenção, sem otimização de chamada de cauda (por isso só há recursão logarítmica), GIL.

---

## 10. O que a PF mostrou durante o processo

Achados que valem para a discussão do artigo, independentemente dos números de vazão:

1. **O núcleo puro permitiu um oráculo.** Como as regras não tocam banco nem relógio, foi possível escrever uma implementação sequencial de referência e reconciliar cada registro. Sem isso, as categorias da seção 6 não existiriam.
2. **Os testes de propriedade revelaram um erro de especificação (B2)**, e não de implementação: a intuição de que o reenvio é idempotente estava errada num caso de empate. O contraexemplo virou documentação executável.
3. **Funções de ordem superior tornaram a resiliência configurável:** retry e falha simulada são camadas compostas sobre a gravação (decoradores em Python, `|>` em Elixir), trocadas em execução por `/admin/config`.
4. **O bug B1 é de estado mutável compartilhado** (duas fontes para o mesmo contador, uma sobrescrevendo a outra) e aconteceu justamente na casca imperativa, fora do núcleo funcional.
