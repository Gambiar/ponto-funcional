| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.6 | 5.4 | 5.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.0 | 5.5 | 5.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.8 | 15.1 | 15.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.3 | True | True | True | True | 0 | 2.2 | 290.1 | 290.1 | 1.0 | 0.999865 | 0 | 8 | 0 | True | False | False |
| baseline | 1500 | 1169.6 | 16042.1 | False | True | True | False | gerador_atrasou | 358.5 | 10189.2 | 20848.2 | 0.483817 | 0.966887 | 46010 | 1428 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 3.7 | True | True | True | True | 0 | 2.3 | 3912.4 | 5963.6 | 0.771897 | 0.933432 | 3396 | 765 | 23622 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | True | True | True | 0 | 2.1 | 8.3 | 51.7 | 0.664159 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 0.6 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 0.7 | 1.4 | 1.4 | 0.940188 | 0.995139 | 1335 | 102 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 0.6 | 1.3 | 1.3 | 0.76572 | 0.995164 | 6390 | 101 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 0.6 | 1.4 | 1.4 | 1.0 | 0.501478 | 0 | 7422 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 1.0 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.3 | True | True | True | True | 0 | 0.8 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 0.6 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 0.5 | 2.8 | 2.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.8 | 28.6 | False | True | True | False | gerador_atrasou | 0.5 | 43.6 | 43.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.0 | 68.6 | False | True | True | False | gerador_atrasou | 0.6 | 176.6 | 176.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 1.0 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.8 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 0.6 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.2 | 1.2 | True | True | True | True | 0 | 0.5 | 2.7 | 2.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1498.1 | 43.1 | False | True | True | False | gerador_atrasou | 0.5 | 70.2 | 70.2 | 1.0 | 0.999955 | 0 | 4 | 0 | True | True | False |
| lote_200 | 2000 | 1998.1 | 125.7 | False | True | True | False | gerador_atrasou | 0.6 | 249.7 | 249.7 | 1.0 | 0.999966 | 0 | 4 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 1.0 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 0.6 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.2 | 1.2 | True | True | True | True | 0 | 0.5 | 2.7 | 2.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 39.0 | False | True | True | False | gerador_atrasou | 0.5 | 141.0 | 141.0 | 1.0 | 0.999978 | 0 | 2 | 0 | True | True | False |
| lote_50 | 2000 | 1998.3 | 88.6 | False | True | True | False | gerador_atrasou | 0.6 | 437.4 | 437.4 | 1.0 | 0.999882 | 0 | 14 | 0 | True | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 500 | 500 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 1000 | 1000 | 1000 |
| lote_200 | 1000 | 1000 | 1000 |
| lote_50 | 1000 | 1000 | 1000 |
