| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.3 | 4.6 | 4.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 1.9 | 4.9 | 4.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.7 | 10.5 | 10.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.2 | 1.2 | True | True | True | True | 0 | 2.4 | 198.9 | 198.9 | 1.0 | 0.999933 | 0 | 4 | 0 | True | True | False |
| baseline | 1500 | 1384.7 | 4448.1 | False | True | True | False | gerador_atrasou | 393.5 | 6568.9 | 11212.3 | 0.62454 | 0.962564 | 33467 | 2084 | 0 | False | False | False |
| baseline | 2000 | 1628.4 | 30716.8 | False | True | True | False | gerador_atrasou | 8.4 | 5728.0 | 52357.2 | 0.217995 | 0.99973 | 92928 | 7 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.8 | 4062.4 | 5956.6 | 0.781273 | 0.944818 | 3247 | 640 | 23237 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.5 | 5.9 | 51.6 | 0.663119 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.2 | 1.1 | 0.940222 | 0.994944 | 1333 | 106 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.765748 | 0.994969 | 6385 | 105 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 0.502055 | 0 | 7392 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.7 | 15.8 | True | True | True | True | 0 | 0.5 | 44.4 | 44.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.2 | 94.8 | False | True | True | False | gerador_atrasou | 0.5 | 130.4 | 130.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.5 | 596.1 | False | True | True | False | gerador_atrasou | 1.0 | 1497.0 | 1497.0 | 1.0 | 0.999877 | 0 | 22 | 0 | True | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 7.3 | True | True | True | True | 0 | 0.5 | 8.8 | 8.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.3 | 84.5 | False | True | True | False | gerador_atrasou | 0.5 | 131.3 | 131.3 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_200 | 3000 | 2995.7 | 713.1 | False | True | True | False | gerador_atrasou | 1.1 | 1324.2 | 1324.2 | 1.0 | 0.999787 | 0 | 38 | 0 | True | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 0.5 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 1.2 | True | True | True | True | 0 | 0.4 | 7.3 | 7.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.3 | 42.1 | False | True | True | False | gerador_atrasou | 0.5 | 70.2 | 70.2 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_50 | 3000 | 2995.7 | 738.8 | False | True | True | False | gerador_atrasou | 1.1 | 2516.5 | 2516.5 | 1.0 | 0.999753 | 0 | 44 | 0 | True | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 500 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 1500 | 1500 | 1500 |
| lote_200 | 1500 | 1500 | 1500 |
| lote_50 | 1500 | 1500 | 1500 |
