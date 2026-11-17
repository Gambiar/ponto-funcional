| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.3 | 6.9 | 6.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.9 | 4.0 | 4.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 1.9 | 8.0 | 8.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 2.2 | 27.7 | 27.7 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1250 | 1249.3 | 1.8 | True | True | True | True | 0 | 110.6 | 3442.6 | 5289.4 | 0.987113 | 0.999754 | 957 | 18 | 24383 | False | False | False |
| baseline | 1500 | 1498.3 | 41.0 | False | True | True | True | 0 | 117.8 | 3679.0 | 5945.9 | 0.874722 | 0.986828 | 11167 | 1027 | 125020 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 2.3 | 3876.3 | 5963.3 | 0.771976 | 0.930617 | 3393 | 797 | 25582 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | True | True | True | 0 | 1.8 | 7.2 | 51.4 | 0.664046 | 1.0 | 4999 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.939621 | 0.994984 | 1345 | 105 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 0.765026 | 0.99491 | 6396 | 106 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.7 | 12.4 | 4465.5 | 0.663306 | 1.0 | 5010 | 0 | 0 | False | True | False |
| falha_real_com_retry | 500 | 499.8 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 5 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.954368 | 0 | 679 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 0.497782 | 0 | 7473 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.0 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.3 | 1.1 | True | True | True | True | 0 | 0.3 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.3 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.4 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.1 | 2.2 | True | True | True | True | 0 | 0.4 | 6.6 | 6.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.2 | 47.6 | False | True | True | False | gerador_atrasou | 0.4 | 24.4 | 24.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 6000 | 5984.4 | 228.9 | False | True | True | False | gerador_atrasou | 0.5 | 107.7 | 107.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.8 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.3 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.1 | 1.6 | True | True | True | True | 0 | 0.4 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.1 | 48.7 | False | True | True | False | gerador_atrasou | 0.4 | 25.5 | 25.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 6000 | 5983.9 | 558.1 | False | True | True | False | gerador_atrasou | 0.6 | 1137.0 | 1137.0 | 1.0 | 0.999966 | 0 | 12 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.3 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.2 | 1.9 | True | True | True | True | 0 | 0.4 | 5.1 | 5.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3992.9 | 44.5 | False | True | True | False | gerador_atrasou | 0.4 | 25.3 | 25.3 | 1.0 | 0.999992 | 0 | 2 | 0 | True | True | False |
| lote_50 | 6000 | 5983.8 | 261.2 | False | True | True | False | gerador_atrasou | 0.6 | 132.9 | 132.9 | 1.0 | 0.999989 | 0 | 4 | 0 | True | True | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 500 |
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
