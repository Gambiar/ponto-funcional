| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.0 | 5.0 | 5.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.8 | 3.6 | 3.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.7 | 6.4 | 6.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 2.0 | 20.3 | 20.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 5.8 | 183.4 | 183.4 | 1.0 | 1.0 | 0 | 0 | 267 | True | True | True |
| baseline | 1500 | 1499.1 | 13.3 | True | True | True | True | 0 | 113.6 | 3621.0 | 5836.6 | 0.919079 | 0.998669 | 7213 | 109 | 80744 | False | False | False |
| baseline | 1750 | 1742.8 | 113.0 | False | True | True | True | 0 | 118.1 | 3760.4 | 5973.7 | 0.773932 | 0.972354 | 23488 | 2223 | 216180 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.9 | 3710.7 | 5961.9 | 0.771236 | 0.935278 | 3396 | 741 | 24541 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.5 | 6.9 | 51.4 | 0.663186 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.6 | 0.6 | 0.939728 | 0.995037 | 1344 | 104 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.7 | 0.6 | 0.765345 | 0.994967 | 6396 | 105 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 15.2 | 5496.1 | 0.662243 | 1.0 | 5014 | 0 | 0 | False | True | False |
| falha_real_com_retry | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 4 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.6 | 0.6 | 1.0 | 0.949208 | 0 | 754 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.502863 | 0 | 7380 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 4.2 | True | True | True | True | 0 | 0.5 | 2.0 | 2.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.6 | 0.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.3 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.3 | 1.3 | True | True | True | True | 0 | 0.3 | 3.1 | 3.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.4 | 40.3 | False | True | True | False | gerador_atrasou | 0.4 | 20.4 | 20.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 6000 | 5949.9 | 227.5 | False | True | True | False | gerador_atrasou | 0.5 | 100.0 | 100.0 | 1.0 | 0.999989 | 0 | 4 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.3 | 0.6 | 0.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.3 | 0.6 | 0.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.6 | 1.2 | True | True | True | True | 0 | 0.3 | 2.6 | 2.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.4 | 1.3 | True | True | True | True | 0 | 0.3 | 3.5 | 3.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.2 | 52.9 | False | True | True | False | gerador_atrasou | 0.4 | 25.4 | 25.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 6000 | 5984.2 | 292.5 | False | True | True | False | gerador_atrasou | 0.6 | 391.7 | 391.7 | 1.0 | 0.999944 | 0 | 20 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.6 | 0.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.3 | 2.0 | 2.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.3 | 1.4 | True | True | True | True | 0 | 0.4 | 4.8 | 4.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3993.3 | 44.4 | False | True | True | False | gerador_atrasou | 0.4 | 23.3 | 23.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 6000 | 5984.0 | 232.2 | False | True | True | False | gerador_atrasou | 0.6 | 99.2 | 99.2 | 1.0 | 0.999994 | 0 | 2 | 0 | True | True | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1250 | 1250 | 1250 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | 500 | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 3000 | 3000 | 3000 |
| lote_200 | 3000 | 3000 | 3000 |
| lote_50 | 3000 | 3000 | 3000 |
