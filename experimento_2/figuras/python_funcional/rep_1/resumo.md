| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.1 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.7 | 4.9 | 4.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.7 | 9.5 | 9.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.4 | 1.2 | True | True | True | True | 0 | 2.3 | 208.7 | 208.7 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1250 | 1249.4 | 1.4 | True | True | True | True | 0 | 3.2 | 511.9 | 511.9 | 1.0 | 0.999623 | 0 | 28 | 0 | True | False | False |
| baseline | 1500 | 1498.2 | 155.6 | False | True | True | True | 0 | 343.1 | 5486.4 | 5987.1 | 0.662905 | 0.946505 | 30048 | 3161 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.4 | True | True | True | True | 0 | 1.7 | 3481.2 | 5963.2 | 0.771573 | 0.930145 | 3399 | 802 | 23851 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.8 | 1.7 | True | True | True | True | 0 | 1.4 | 4.3 | 51.5 | 0.663978 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.94016 | 0.994986 | 1333 | 105 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.76543 | 0.994912 | 6385 | 106 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.6 | 5070.1 | 5790.3 | 0.782191 | 0.996907 | 3241 | 36 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.7 | 1.7 | 1.0 | 0.498387 | 0 | 7464 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 0.496169 | 0 | 7497 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 2.0 | 2.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 2.7 | 2.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 6.0 | 6.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.2 | 1.1 | True | True | True | True | 0 | 0.4 | 7.4 | 7.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.3 | 1.2 | True | True | True | True | 0 | 0.5 | 17.3 | 17.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.0 | 30.8 | False | True | True | False | gerador_atrasou | 0.6 | 107.3 | 107.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3992.5 | 137.6 | False | True | True | False | gerador_atrasou | 4.6 | 292.3 | 292.3 | 1.0 | 0.999958 | 0 | 10 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.0 | 1.1 | True | True | True | True | 0 | 0.4 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 3.0 | 3.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 5.0 | 5.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1997.9 | 1.1 | True | True | True | True | 0 | 0.4 | 7.1 | 7.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.1 | 1.2 | True | True | True | True | 0 | 0.5 | 18.5 | 18.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.1 | 13.9 | True | True | True | True | 0 | 0.5 | 77.5 | 77.5 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_200 | 4000 | 3992.7 | 119.5 | False | True | True | False | gerador_atrasou | 1.0 | 266.6 | 266.6 | 1.0 | 0.999874 | 0 | 30 | 0 | True | False | False |
| lote_200 | 6000 | 3260.6 | 50133.5 | False | True | True | True | 0 | 81.6 | 5399.7 | 55919.4 | 0.497681 | 0.996828 | 179123 | 563 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 0.996975 | 0 | 18 | 0 | True | False | False |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 3.8 | 3.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.5 | 6.6 | 6.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.5 | 8.3 | 8.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2496.9 | 1.3 | True | True | True | True | 0 | 0.5 | 17.8 | 17.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.0 | 25.9 | False | True | True | False | gerador_atrasou | 0.6 | 144.8 | 144.8 | 1.0 | 0.999966 | 0 | 6 | 0 | True | True | False |
| lote_50 | 4000 | 3989.0 | 140.6 | False | True | True | False | gerador_atrasou | 1.3 | 318.8 | 318.8 | 1.0 | 0.999891 | 0 | 26 | 0 | True | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1250 | 1000 | 500 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 2500 | 2500 | 2500 |
| lote_200 | 3000 | 3000 | 2500 |
| lote_50 | 2500 | None | None |
