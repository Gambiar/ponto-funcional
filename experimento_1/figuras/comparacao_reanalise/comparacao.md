> **Reanálise (C16):** degraus revalidados com o atraso do gerador medido depois da largada.

Atraso p99 do gerador medido só depois dos 2 s iniciais de cada degrau (C16).

| implementação | degraus | válidos (original) | válidos (reanálise) | revalidados |
|---|---|---|---|---|
| python_imperativo | 150 | 109 | 137 | 28 |
| python_funcional | 159 | 119 | 146 | 27 |
| elixir | 149 | 103 | 135 | 32 |

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
| lote_200 | 2000 [2000–2000] (n=4) | 2000 [500–2000] (n=5) | 2000 [2000–3000] (n=4) |
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

## Latência p99 (H2, C17)

Latência p99 das respostas 2xx (ms), mediana [mín–máx] das repetições, nos degraus válidos e sem erro de carga. p: Mann-Whitney exato bilateral; em negrito, p < 0,05. São muitos testes: um p isolado perto de 0,05 não basta, o que conta é a consistência ao longo das taxas.

| cenário | taxa | python_imperativo | python_funcional | elixir | p (imp×fun) | p (fun×ex) |
|---|---|---|---|---|---|---|
| baseline | 100 | 4.5 [4.0–4.7] | 4.7 [4.0–7.7] | 5.6 [4.1–7.8] | 0.468 | 0.548 |
| baseline | 250 | 5.1 [3.6–8.5] | 5.1 [4.6–10.8] | 5.5 [4.0–7.1] | 0.833 | 0.937 |
| baseline | 500 | 8.1 [7.2–11.0] | 13.1 [9.2–15.1] | 6.6 [6.0–7.7] | 0.056 | **0.008** |
| baseline | 1000 | 167.7 [114.5–222.1] | 202.0 [165.8–273.0] | 66.5 [41.2–96.6] | 0.421 | **0.008** |
| lote_1000 | 100 | 1.3 [1.2–1.5] | 1.3 [1.3–1.7] | 1.2 [1.1–1.4] | 0.524 | 0.286 |
| lote_1000 | 250 | 1.1 [0.9–1.2] | 1.1 [1.0–1.5] | 1.0 [0.9–1.1] | 0.984 | 0.286 |
| lote_1000 | 500 | 1.0 [0.8–1.1] | 1.0 [1.0–1.2] | 0.9 [0.8–1.0] | 0.603 | **0.040** |
| lote_1000 | 1000 | 1.3 [1.2–1.4] | 1.7 [1.5–2.2] | 0.9 [0.8–1.0] | **0.008** | **0.008** |
| lote_1000 | 1500 | 4.7 [4.5–5.1] | 5.6 [4.2–9.9] | 1.4 [1.4–2.0] | 0.135 | **0.016** |
| lote_1000 | 2000 | 11.4 [9.9–37.0] | 40.7 [17.7–104.0] | 6.2 [5.0–7.1] | 0.056 | **0.016** |
| lote_200 | 100 | 1.4 [1.3–1.7] | 1.3 [1.3–1.5] | 1.2 [1.1–1.3] | 0.762 | **0.032** |
| lote_200 | 250 | 1.0 [0.9–1.2] | 1.1 [1.1–1.4] | 1.1 [0.9–1.2] | 0.119 | 0.397 |
| lote_200 | 500 | 1.0 [0.9–1.0] | 1.0 [0.9–1.3] | 0.9 [0.8–0.9] | 0.683 | 0.079 |
| lote_200 | 1000 | 1.4 [1.2–1.5] | 1.6 [1.5–2.1] | 0.9 [0.9–1.0] | 0.079 | **0.029** |
| lote_200 | 1500 | 4.7 [3.0–5.3] | 5.5 [4.3–7.4] | 1.8 [1.5–2.3] | 0.175 | **0.016** |
| lote_200 | 2000 | 14.7 [12.1–17.3] | 36.9 [15.1–67.5] | 6.8 [5.3–8.4] | 0.095 | **0.016** |
| lote_50 | 100 | 1.3 [1.3–1.5] | 1.3 [1.2–1.6] | 1.2 [1.1–1.3] | 0.696 | 0.246 |
| lote_50 | 250 | 1.0 [1.0–1.3] | 1.1 [1.0–1.3] | 0.9 [0.9–1.2] | 0.661 | 0.079 |
| lote_50 | 500 | 0.9 [0.9–1.0] | 1.0 [0.9–1.4] | 0.9 [0.8–1.1] | 0.679 | 0.190 |
| lote_50 | 1000 | 1.4 [1.3–1.4] | 1.4 [1.4–2.2] | 1.0 [0.9–1.1] | 0.268 | **0.008** |
| lote_50 | 1500 | 4.9 [4.7–6.2] | 6.9 [5.4–9.2] | 1.6 [1.3–6.0] | 0.071 | **0.016** |
| lote_50 | 2000 | 36.6 [27.4–37.2] | 40.3 [16.8–76.9] | 5.4 [4.2–7.1] | 0.571 | **0.008** |

## Validade da execução (C13)

| implementação | degraus | válidos | api_reiniciou | fila_nao_drenou | gerador_atrasou | falha_execucao | registros perdidos pela fila | API saturou (válido, reprovado) |
|---|---|---|---|---|---|---|---|---|
| python_imperativo | 150 | 137 | 0 | 0 | 8 | 5 | 25561 | 9 |
| python_funcional | 159 | 146 | 0 | 0 | 11 | 2 | 25566 | 7 |
| elixir | 149 | 135 | 0 | 11 | 3 | 0 | 25489 | 14 |

Degraus inválidos:

| implementação | repetição | cenário | taxa | motivo |
|---|---|---|---|---|
| python_imperativo | rep_1 | lote_50 | 100 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_1 | lote_50 | 250 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_2 | lote_1000 | 3000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_200 | 100 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_2 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_50 | 100 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_2 | lote_50 | 250 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_imperativo | rep_3 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_1000 | 3000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_1000 | 3000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_200 | 3000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_1 | baseline | 2000 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_funcional | rep_1 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_1 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_2 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_2 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_3 | lote_1000 | 3000 | gerador_atrasou |
| python_funcional | rep_3 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_3 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_4 | baseline | 2000 | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] |
| python_funcional | rep_4 | lote_1000 | 3000 | gerador_atrasou |
| python_funcional | rep_4 | lote_200 | 1000 | gerador_atrasou |
| python_funcional | rep_4 | lote_200 | 3000 | gerador_atrasou |
| python_funcional | rep_4 | lote_50 | 3000 | gerador_atrasou |
| elixir | rep_1 | lote_1000 | 3000 | gerador_atrasou |
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
| elixir | rep_2 | lote_50 | 3000 | fila_nao_drenou |
| elixir | rep_4 | lote_200 | 3000 | gerador_atrasou |
| elixir | rep_4 | lote_50 | 3000 | gerador_atrasou |

