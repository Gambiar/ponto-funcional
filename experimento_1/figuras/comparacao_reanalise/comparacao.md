> **Reanálise (C16):** degraus revalidados com o atraso do gerador medido depois da largada.

Atraso p99 do gerador medido só depois dos 2 s iniciais de cada degrau (C16).

| implementação | degraus | válidos (original) | válidos (reanálise) | revalidados |
|---|---|---|---|---|
| python_imperativo | 150 | 109 | 128 | 19 |
| python_funcional | 159 | 119 | 139 | 20 |
| elixir | 149 | 103 | 122 | 19 |

## Limite (req/s), critério `ok_carga`

| cenário | python_imperativo | python_funcional | elixir |
|---|---|---|---|
| baseline | 1000 [1000–1500] (n=5) | 1000 [1000–1000] (n=5) | 1000 [1000–1000] (n=5) |
| falha_baseline_com_retry | nenhum | nenhum | nenhum |
| falha_baseline_sem_retry | nenhum | nenhum | nenhum |
| falha_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=4) |
| falha_com_retry_20s | nenhum | nenhum | nenhum |
| falha_com_retry_30s | nenhum | nenhum | nenhum |
| falha_sem_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=4) |
| lote_1000 | 2000 [2000–2000] (n=5) | 2000 [2000–2000] (n=5) | 2000 [2000–2000] (n=4) |
| lote_200 | 2000 [2000–2000] (n=4) | 2000 [500–2000] (n=5) | 2000 [2000–2000] (n=4) |
| lote_50 | 2000 [2000–2000] (n=3) | 2000 [2000–2000] (n=5) | 2000 [2000–2000] (n=5) |

## Limite (req/s), critério `ok_integridade`

| cenário | python_imperativo | python_funcional | elixir |
|---|---|---|---|
| baseline | 1000 [1000–1000] (n=5) | 1000 [500–1000] (n=5) | 1000 [1000–1000] (n=5) |
| falha_baseline_com_retry | nenhum | nenhum | nenhum |
| falha_baseline_sem_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=4) |
| falha_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=4) |
| falha_com_retry_20s | nenhum | nenhum | nenhum |
| falha_com_retry_30s | nenhum | nenhum | nenhum |
| falha_sem_retry | nenhum | nenhum | nenhum |
| lote_1000 | 2000 [2000–2000] (n=5) | 2000 [2000–2000] (n=5) | 2000 [2000–2000] (n=4) |
| lote_200 | 2000 [2000–2000] (n=4) | 2000 [500–2000] (n=5) | 2000 [2000–2000] (n=4) |
| lote_50 | 2000 [2000–2000] (n=3) | 2000 [1500–2000] (n=5) | 2000 [2000–2000] (n=5) |

## Limite (req/s), critério `sem_erros`

| cenário | python_imperativo | python_funcional | elixir |
|---|---|---|---|
| baseline | 500 [250–1000] (n=5) | 500 [500–1000] (n=5) | 1000 [1000–1000] (n=5) |
| falha_baseline_com_retry | nenhum | nenhum | nenhum |
| falha_baseline_sem_retry | nenhum | nenhum | nenhum |
| falha_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=4) |
| falha_com_retry_20s | nenhum | nenhum | nenhum |
| falha_com_retry_30s | nenhum | nenhum | nenhum |
| falha_sem_retry | nenhum | nenhum | nenhum |
| lote_1000 | 2000 [1500–2000] (n=5) | 2000 [1500–2000] (n=5) | 2000 [2000–2000] (n=4) |
| lote_200 | 1500 [1000–2000] (n=4) | 1500 [500–1500] (n=5) | 1500 [1000–1500] (n=4) |
| lote_50 | 1500 [1000–2000] (n=3) | 1500 [1000–1500] (n=5) | 1500 [1000–2000] (n=5) |

## Validade da execução (C13)

| implementação | degraus | válidos | api_reiniciou | fila_nao_drenou | gerador_atrasou | falha_execucao | registros perdidos pela fila |
|---|---|---|---|---|---|---|---|
| python_imperativo | 150 | 128 | 0 | 0 | 17 | 5 | 25561 |
| python_funcional | 159 | 139 | 0 | 0 | 18 | 2 | 25566 |
| elixir | 149 | 122 | 0 | 11 | 17 | 0 | 25489 |

Degraus inválidos:

| implementação | repetição | cenário | taxa | motivo |
|---|---|---|---|---|
| python_imperativo | rep_1 | baseline | 1500 | gerador_atrasou |
| python_imperativo | rep_1 | baseline | 2000 | gerador_atrasou |
| python_imperativo | rep_1 | lote_50 | 100 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_1 | lote_50 | 250 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_2 | baseline | 2000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_1000 | 3000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_200 | 100 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_2 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_50 | 100 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_2 | lote_50 | 250 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_3 | baseline | 1500 | gerador_atrasou |
| python_imperativo | rep_3 | baseline | 2000 | gerador_atrasou |
| python_imperativo | rep_3 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_4 | baseline | 1500 | gerador_atrasou |
| python_imperativo | rep_4 | baseline | 2000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_1000 | 3000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_5 | baseline | 1500 | gerador_atrasou |
| python_imperativo | rep_5 | baseline | 2000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_1000 | 3000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_1 | baseline | 1500 | gerador_atrasou |
| python_funcional | rep_1 | baseline | 2000 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_funcional | rep_1 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_1 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_2 | baseline | 1500 | gerador_atrasou |
| python_funcional | rep_2 | baseline | 2000 | gerador_atrasou |
| python_funcional | rep_2 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_2 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_3 | baseline | 1500 | gerador_atrasou |
| python_funcional | rep_3 | baseline | 2000 | gerador_atrasou |
| python_funcional | rep_3 | lote_1000 | 3000 | gerador_atrasou |
| python_funcional | rep_3 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_3 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_4 | baseline | 1500 | gerador_atrasou |
| python_funcional | rep_4 | baseline | 2000 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_funcional | rep_4 | lote_1000 | 3000 | gerador_atrasou |
| python_funcional | rep_4 | lote_200 | 1000 | gerador_atrasou |
| python_funcional | rep_4 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_4 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_5 | baseline | 1500 | gerador_atrasou |
| elixir | rep_1 | baseline | 1500 | gerador_atrasou |
| elixir | rep_1 | baseline | 2000 | gerador_atrasou |
| elixir | rep_1 | lote_1000 | 3000 | gerador_atrasou |
| elixir | rep_1 | lote_200 | 3000 | gerador_atrasou |
| elixir | rep_2 | baseline | 1500 | gerador_atrasou |
| elixir | rep_2 | baseline | 2000 | gerador_atrasou |
| elixir | rep_2 | falha_baseline_com_retry | 500 | fila_nao_drenou |
| elixir | rep_2 | falha_baseline_sem_retry | 500 | fila_nao_drenou |
| elixir | rep_2 | falha_com_retry | 500 | fila_nao_drenou |
| elixir | rep_2 | falha_com_retry_20s | 500 | fila_nao_drenou |
| elixir | rep_2 | falha_com_retry_30s | 500 | fila_nao_drenou |
| elixir | rep_2 | falha_sem_retry | 500 | fila_nao_drenou |
| elixir | rep_2 | lote_1000 | 100 | fila_nao_drenou |
| elixir | rep_2 | lote_1000 | 250 | fila_nao_drenou |
| elixir | rep_2 | lote_200 | 100 | fila_nao_drenou |
| elixir | rep_2 | lote_200 | 250 | fila_nao_drenou |
| elixir | rep_2 | lote_50 | 3000 | fila_nao_drenou; gerador_atrasou |
| elixir | rep_3 | baseline | 1500 | gerador_atrasou |
| elixir | rep_3 | baseline | 2000 | gerador_atrasou |
| elixir | rep_3 | lote_50 | 3000 | gerador_atrasou |
| elixir | rep_4 | baseline | 1500 | gerador_atrasou |
| elixir | rep_4 | baseline | 2000 | gerador_atrasou |
| elixir | rep_4 | lote_200 | 3000 | gerador_atrasou |
| elixir | rep_4 | lote_50 | 3000 | gerador_atrasou |
| elixir | rep_5 | baseline | 1500 | gerador_atrasou |
| elixir | rep_5 | baseline | 2000 | gerador_atrasou |
| elixir | rep_5 | lote_200 | 3000 | gerador_atrasou |

