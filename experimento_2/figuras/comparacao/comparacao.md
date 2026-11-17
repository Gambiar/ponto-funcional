## Limite (req/s), critério `ok_carga`

| cenário | python_imperativo | python_funcional | elixir |
|---|---|---|---|
| baseline | 1500 [1250–1500] (n=5) | 1250 [1250–1500] (n=5) | 1000 [1000–1250] (n=5) |
| falha_baseline_com_retry | nenhum | nenhum | nenhum |
| falha_baseline_sem_retry | nenhum | nenhum | nenhum |
| falha_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_com_retry_20s | nenhum | nenhum | nenhum |
| falha_com_retry_30s | nenhum | nenhum | nenhum |
| falha_real_baseline_sem_retry | nenhum | nenhum | nenhum |
| falha_real_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_real_sem_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_sem_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| lote_1000 | 3000 [3000–3000] (n=5) | 3000 [2500–3000] (n=5) | 3000 [3000–3000] (n=5) |
| lote_200 | 3000 [3000–3000] (n=5) | 3000 [3000–3000] (n=5) | 3000 [3000–3000] (n=5) |
| lote_50 | 3000 [3000–3000] (n=5) | 3000 [2500–3000] (n=5) | 3000 [3000–3000] (n=5) |

## Limite (req/s), critério `ok_integridade`

| cenário | python_imperativo | python_funcional | elixir |
|---|---|---|---|
| baseline | 1250 [1000–1250] (n=5) | 1000 [1000–1000] (n=5) | 1000 [1000–1250] (n=5) |
| falha_baseline_com_retry | nenhum | nenhum | nenhum |
| falha_baseline_sem_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_com_retry | 500 [0–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_com_retry_20s | nenhum | nenhum | nenhum |
| falha_com_retry_30s | nenhum | nenhum | nenhum |
| falha_real_baseline_sem_retry | nenhum | nenhum | 500 [500–500] (n=5) |
| falha_real_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_real_sem_retry | nenhum | nenhum | nenhum |
| falha_sem_retry | nenhum | nenhum | nenhum |
| lote_1000 | 3000 [0–3000] (n=5) | 3000 [2500–3000] (n=5) | 3000 [3000–3000] (n=5) |
| lote_200 | 3000 [0–3000] (n=5) | 3000 [0–3000] (n=5) | 3000 [3000–3000] (n=5) |
| lote_50 | 0 [0–3000] (n=5) | 3000 [0–3000] (n=5) | 3000 [3000–3000] (n=5) |

## Limite (req/s), critério `sem_erros`

| cenário | python_imperativo | python_funcional | elixir |
|---|---|---|---|
| baseline | 500 [250–1000] (n=5) | 1000 [500–1000] (n=5) | 1000 [500–1250] (n=5) |
| falha_baseline_com_retry | nenhum | nenhum | nenhum |
| falha_baseline_sem_retry | nenhum | nenhum | nenhum |
| falha_com_retry | 500 [0–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_com_retry_20s | nenhum | nenhum | nenhum |
| falha_com_retry_30s | nenhum | nenhum | nenhum |
| falha_real_baseline_sem_retry | nenhum | nenhum | nenhum |
| falha_real_com_retry | 500 [500–500] (n=5) | 500 [500–500] (n=5) | 500 [500–500] (n=5) |
| falha_real_sem_retry | nenhum | nenhum | nenhum |
| falha_sem_retry | nenhum | nenhum | nenhum |
| lote_1000 | 3000 [0–3000] (n=5) | 2500 [2500–3000] (n=5) | 3000 [2500–3000] (n=5) |
| lote_200 | 3000 [0–3000] (n=5) | 2500 [0–2500] (n=5) | 3000 [3000–3000] (n=5) |
| lote_50 | 0 [0–3000] (n=5) | 2000 [0–3000] (n=5) | 3000 [3000–3000] (n=5) |

## Latência p99 (H2, C17)

Latência p99 das respostas 2xx (ms), mediana [mín–máx] das repetições, nos degraus válidos e sem erro de carga. p: Mann-Whitney exato bilateral; em negrito, p < 0,05. São muitos testes: um p isolado perto de 0,05 não basta, o que conta é a consistência ao longo das taxas.

| cenário | taxa | python_imperativo | python_funcional | elixir | p (imp×fun) | p (fun×ex) |
|---|---|---|---|---|---|---|
| baseline | 100 | 4.6 [4.1–5.3] | 4.0 [3.7–7.1] | 5.1 [4.8–6.9] | 0.167 | 0.151 |
| baseline | 250 | 4.4 [3.8–6.2] | 4.8 [3.6–6.4] | 4.7 [3.6–5.4] | 0.881 | 0.897 |
| baseline | 500 | 10.1 [6.2–12.6] | 9.5 [6.7–11.7] | 6.9 [6.2–8.2] | 0.690 | 0.151 |
| baseline | 1000 | 85.1 [57.0–120.1] | 168.0 [65.9–217.6] | 30.1 [20.3–34.1] | 0.151 | **0.008** |
| lote_1000 | 100 | 1.2 [1.0–1.3] | 1.1 [1.0–1.2] | 1.0 [0.9–2.0] | 0.905 | 0.230 |
| lote_1000 | 250 | 0.9 [0.8–1.0] | 0.9 [0.8–1.0] | 0.8 [0.7–0.9] | 1.000 | 0.206 |
| lote_1000 | 500 | 0.8 [0.7–1.2] | 0.9 [0.8–1.1] | 0.7 [0.6–0.8] | 0.421 | **0.024** |
| lote_1000 | 1000 | 1.1 [1.0–1.3] | 1.2 [1.1–1.3] | 0.7 [0.7–0.7] | 0.421 | **0.008** |
| lote_1000 | 1250 | 1.2 [1.1–1.3] | 1.7 [1.2–2.0] | 0.8 [0.8–0.9] | 0.111 | **0.008** |
| lote_1000 | 1500 | 1.5 [1.4–4.6] | 2.3 [1.7–2.7] | 0.9 [0.8–0.9] | 0.175 | **0.008** |
| lote_1000 | 1750 | 3.0 [2.6–5.3] | 6.0 [3.3–25.1] | 1.0 [0.9–1.3] | **0.048** | **0.008** |
| lote_1000 | 2000 | 5.3 [4.7–7.2] | 7.4 [6.1–8.0] | 1.2 [1.1–1.4] | **0.024** | **0.008** |
| lote_1000 | 2500 | 9.4 [8.2–12.4] | 13.1 [11.1–42.4] | 1.8 [1.4–2.1] | **0.032** | **0.008** |
| lote_1000 | 3000 | 46.1 [24.1–59.2] | 72.4 [57.8–75.1] | 5.7 [3.1–6.6] | 0.071 | **0.036** |
| lote_200 | 100 | 1.2 [1.0–1.3] | 1.1 [1.1–1.3] | 1.0 [0.8–1.0] | 0.905 | **0.008** |
| lote_200 | 250 | 0.9 [0.8–1.2] | 0.9 [0.8–1.1] | 0.9 [0.7–1.0] | 0.810 | 0.500 |
| lote_200 | 500 | 0.8 [0.8–1.0] | 0.9 [0.7–0.9] | 0.7 [0.6–0.8] | 1.000 | 0.071 |
| lote_200 | 1000 | 1.0 [1.0–1.2] | 1.1 [1.1–1.2] | 0.7 [0.6–0.8] | 0.159 | **0.008** |
| lote_200 | 1250 | 1.2 [1.1–1.6] | 1.4 [1.3–1.7] | 0.8 [0.7–1.0] | 0.373 | **0.008** |
| lote_200 | 1500 | 1.6 [1.4–2.1] | 2.2 [1.7–3.0] | 0.9 [0.8–1.0] | **0.016** | **0.008** |
| lote_200 | 1750 | 3.2 [2.9–4.2] | 4.8 [4.3–5.2] | 1.1 [0.9–1.1] | **0.008** | **0.008** |
| lote_200 | 2000 | 4.5 [3.2–7.7] | 7.0 [6.6–7.9] | 1.2 [1.0–1.2] | 0.079 | **0.008** |
| lote_200 | 2500 | 9.1 [8.4–10.8] | 12.9 [10.2–33.2] | 2.2 [1.8–2.6] | **0.016** | **0.008** |
| lote_200 | 3000 | 32.9 [17.1–43.0] | 77.5 [67.4–113.5] | 5.1 [3.5–6.1] | **0.008** | **0.008** |
| lote_50 | 100 | 1.2 [1.0–1.3] | 1.2 [1.0–1.3] | 0.9 [0.9–1.1] | 0.706 | **0.024** |
| lote_50 | 250 | 1.0 [0.8–1.0] | 1.0 [0.8–1.1] | 0.9 [0.8–0.9] | 0.921 | 0.206 |
| lote_50 | 500 | 0.8 [0.7–0.9] | 0.8 [0.8–1.0] | 0.7 [0.6–0.8] | 0.524 | **0.032** |
| lote_50 | 1000 | 1.1 [0.9–1.3] | 1.1 [1.0–1.3] | 0.7 [0.7–0.8] | 0.992 | **0.008** |
| lote_50 | 1250 | 1.6 [1.1–1.8] | 1.3 [1.2–1.4] | 0.8 [0.7–0.9] | 0.365 | **0.008** |
| lote_50 | 1500 | 1.6 [1.5–2.8] | 2.3 [1.8–4.1] | 0.9 [0.8–1.0] | 0.087 | **0.008** |
| lote_50 | 1750 | 3.3 [2.9–4.1] | 6.5 [3.5–6.8] | 1.1 [1.0–1.2] | **0.032** | **0.008** |
| lote_50 | 2000 | 6.0 [5.0–7.1] | 7.2 [7.0–8.4] | 1.2 [1.0–1.3] | **0.024** | **0.008** |
| lote_50 | 2500 | 10.5 [9.6–12.7] | 14.0 [12.2–23.7] | 1.9 [1.6–2.3] | **0.032** | **0.008** |
| lote_50 | 3000 | 41.3 [20.7–55.2] | 73.4 [61.0–101.0] | 5.1 [4.4–9.4] | **0.016** | **0.016** |

## Validade da execução (C13)

| implementação | degraus | válidos | api_reiniciou | fila_nao_drenou | gerador_atrasou | falha_execucao | registros perdidos pela fila | API saturou (válido, reprovado) |
|---|---|---|---|---|---|---|---|---|
| python_imperativo | 259 | 244 | 0 | 0 | 15 | 0 | 50660 | 19 |
| python_funcional | 252 | 235 | 0 | 0 | 17 | 0 | 50610 | 16 |
| elixir | 256 | 226 | 0 | 0 | 30 | 0 | 29262 | 3 |

Degraus inválidos:

| implementação | repetição | cenário | taxa | motivo |
|---|---|---|---|---|
| python_imperativo | rep_1 | lote_1000 | 4000 | gerador_atrasou |
| python_imperativo | rep_1 | lote_200 | 4000 | gerador_atrasou |
| python_imperativo | rep_1 | lote_50 | 4000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_1000 | 4000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_200 | 4000 | gerador_atrasou |
| python_imperativo | rep_2 | lote_50 | 4000 | gerador_atrasou |
| python_imperativo | rep_3 | lote_1000 | 4000 | gerador_atrasou |
| python_imperativo | rep_3 | lote_200 | 4000 | gerador_atrasou |
| python_imperativo | rep_3 | lote_50 | 4000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_1000 | 4000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_200 | 4000 | gerador_atrasou |
| python_imperativo | rep_4 | lote_50 | 4000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_1000 | 4000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_200 | 4000 | gerador_atrasou |
| python_imperativo | rep_5 | lote_50 | 4000 | gerador_atrasou |
| python_funcional | rep_1 | lote_1000 | 3000 | gerador_atrasou |
| python_funcional | rep_1 | lote_1000 | 4000 | gerador_atrasou |
| python_funcional | rep_1 | lote_200 | 4000 | gerador_atrasou |
| python_funcional | rep_1 | lote_50 | 3000 | gerador_atrasou |
| python_funcional | rep_1 | lote_50 | 4000 | gerador_atrasou |
| python_funcional | rep_2 | lote_1000 | 4000 | gerador_atrasou |
| python_funcional | rep_2 | lote_200 | 4000 | gerador_atrasou |
| python_funcional | rep_2 | lote_50 | 4000 | gerador_atrasou |
| python_funcional | rep_3 | lote_1000 | 4000 | gerador_atrasou |
| python_funcional | rep_3 | lote_200 | 4000 | gerador_atrasou |
| python_funcional | rep_3 | lote_50 | 4000 | gerador_atrasou |
| python_funcional | rep_4 | lote_1000 | 4000 | gerador_atrasou |
| python_funcional | rep_4 | lote_200 | 4000 | gerador_atrasou |
| python_funcional | rep_4 | lote_50 | 4000 | gerador_atrasou |
| python_funcional | rep_5 | lote_1000 | 3000 | gerador_atrasou |
| python_funcional | rep_5 | lote_1000 | 4000 | gerador_atrasou |
| python_funcional | rep_5 | lote_200 | 4000 | gerador_atrasou |
| elixir | rep_1 | lote_1000 | 4000 | gerador_atrasou |
| elixir | rep_1 | lote_1000 | 6000 | gerador_atrasou |
| elixir | rep_1 | lote_200 | 4000 | gerador_atrasou |
| elixir | rep_1 | lote_200 | 6000 | gerador_atrasou |
| elixir | rep_1 | lote_50 | 4000 | gerador_atrasou |
| elixir | rep_1 | lote_50 | 6000 | gerador_atrasou |
| elixir | rep_2 | lote_1000 | 4000 | gerador_atrasou |
| elixir | rep_2 | lote_1000 | 6000 | gerador_atrasou |
| elixir | rep_2 | lote_200 | 4000 | gerador_atrasou |
| elixir | rep_2 | lote_200 | 6000 | gerador_atrasou |
| elixir | rep_2 | lote_50 | 4000 | gerador_atrasou |
| elixir | rep_2 | lote_50 | 6000 | gerador_atrasou |
| elixir | rep_3 | lote_1000 | 4000 | gerador_atrasou |
| elixir | rep_3 | lote_1000 | 6000 | gerador_atrasou |
| elixir | rep_3 | lote_200 | 4000 | gerador_atrasou |
| elixir | rep_3 | lote_200 | 6000 | gerador_atrasou |
| elixir | rep_3 | lote_50 | 4000 | gerador_atrasou |
| elixir | rep_3 | lote_50 | 6000 | gerador_atrasou |
| elixir | rep_4 | lote_1000 | 4000 | gerador_atrasou |
| elixir | rep_4 | lote_1000 | 6000 | gerador_atrasou |
| elixir | rep_4 | lote_200 | 4000 | gerador_atrasou |
| elixir | rep_4 | lote_200 | 6000 | gerador_atrasou |
| elixir | rep_4 | lote_50 | 4000 | gerador_atrasou |
| elixir | rep_4 | lote_50 | 6000 | gerador_atrasou |
| elixir | rep_5 | lote_1000 | 4000 | gerador_atrasou |
| elixir | rep_5 | lote_1000 | 6000 | gerador_atrasou |
| elixir | rep_5 | lote_200 | 4000 | gerador_atrasou |
| elixir | rep_5 | lote_200 | 6000 | gerador_atrasou |
| elixir | rep_5 | lote_50 | 4000 | gerador_atrasou |
| elixir | rep_5 | lote_50 | 6000 | gerador_atrasou |

