| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.4 | 4.6 | 4.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.2 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 1.9 | 7.7 | 7.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.3 | 1.2 | True | True | True | True | 0 | 2.5 | 66.7 | 66.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1498.4 | 133.7 | False | True | True | False | gerador_atrasou | 121.1 | 3710.0 | 5963.1 | 0.814441 | 0.97807 | 16540 | 1592 | 160893 | False | False | False |
| baseline | 2000 | 1359.4 | 38876.3 | False | True | True | False | gerador_atrasou | 416.9 | 3782.4 | 41319.6 | 0.207754 | 0.994694 | 94145 | 131 | 132944 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 5.1 | True | True | True | True | 0 | 119.4 | 5453.0 | 5955.7 | 0.741125 | 0.92765 | 3843 | 796 | 31623 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 1.8 | 13.5 | 51.6 | 0.663119 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 0.939683 | 0.994941 | 1345 | 106 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.765345 | 0.994967 | 6396 | 105 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 0.502796 | 0 | 7381 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.4 | 31.4 | False | True | True | False | gerador_atrasou | 0.4 | 8.6 | 8.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 85.5 | False | True | True | False | gerador_atrasou | 0.4 | 78.2 | 78.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.8 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 30.3 | False | True | True | False | gerador_atrasou | 0.4 | 12.1 | 12.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.2 | 100.2 | False | True | True | False | gerador_atrasou | 0.4 | 80.0 | 80.0 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.3 | True | True | True | True | 0 | 0.4 | 3.3 | 3.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 44.5 | False | True | True | False | gerador_atrasou | 0.4 | 12.8 | 12.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2995.7 | 733.8 | False | True | True | False | gerador_atrasou | 0.4 | 909.0 | 5124.6 | 0.881685 | 0.999917 | 21080 | 13 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 1000 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 1000 | 1000 | 1000 |
| lote_200 | 1000 | 1000 | 1000 |
| lote_50 | 1500 | 1500 | 1500 |
