| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.4 | 6.2 | 6.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.1 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 1.8 | 6.2 | 6.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 2.5 | 34.1 | 34.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.3 | 1.6 | True | True | True | True | 0 | 109.3 | 3519.9 | 5283.4 | 0.983811 | 0.999726 | 1202 | 20 | 26977 | False | False | False |
| baseline | 1500 | 1498.9 | 55.2 | False | True | True | True | 0 | 118.9 | 3687.6 | 5944.3 | 0.846989 | 0.983913 | 13644 | 1215 | 144334 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 3.0 | 3946.6 | 5954.2 | 0.771578 | 0.935616 | 3398 | 739 | 25938 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.8 | 1.4 | True | True | True | True | 0 | 1.7 | 9.8 | 51.5 | 0.663888 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 0.939717 | 0.994988 | 1344 | 105 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.765006 | 0.995054 | 6397 | 103 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.7 | 24.5 | 5248.7 | 0.664291 | 1.0 | 4994 | 0 | 0 | False | True | False |
| falha_real_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 5 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.940844 | 0 | 880 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.8 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.507394 | 0 | 7328 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.6 | 1.2 | True | True | True | True | 0 | 0.3 | 2.1 | 2.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.2 | 1.5 | True | True | True | True | 0 | 0.4 | 6.2 | 6.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.0 | 50.2 | False | True | True | False | gerador_atrasou | 0.4 | 26.5 | 26.5 | 1.0 | 0.999992 | 0 | 2 | 0 | True | True | False |
| lote_1000 | 6000 | 5982.8 | 237.5 | False | True | True | False | gerador_atrasou | 0.6 | 110.4 | 110.4 | 1.0 | 0.999994 | 0 | 2 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.3 | 1.1 | True | True | True | True | 0 | 0.3 | 2.2 | 2.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2995.0 | 1.6 | True | True | True | True | 0 | 0.3 | 5.1 | 5.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.1 | 59.2 | False | True | True | False | gerador_atrasou | 0.4 | 30.8 | 30.8 | 1.0 | 0.999992 | 0 | 2 | 0 | True | True | False |
| lote_200 | 6000 | 5976.5 | 265.7 | False | True | True | False | gerador_atrasou | 0.6 | 186.8 | 186.8 | 1.0 | 0.999989 | 0 | 4 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.3 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.2 | 1.2 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.3 | 1.2 | True | True | True | True | 0 | 0.3 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.3 | 1.8 | True | True | True | True | 0 | 0.4 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3992.9 | 44.4 | False | True | True | False | gerador_atrasou | 0.4 | 23.2 | 23.2 | 1.0 | 0.999992 | 0 | 2 | 0 | True | True | False |
| lote_50 | 6000 | 5950.3 | 351.1 | False | True | True | False | gerador_atrasou | 0.6 | 716.7 | 716.7 | 1.0 | 0.999966 | 0 | 12 | 0 | True | True | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 1000 |
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
