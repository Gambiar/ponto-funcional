| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.1 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.8 | True | True | True | True | 0 | 1.6 | 4.4 | 4.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.5 | 10.1 | 10.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 1.8 | 103.9 | 103.9 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.4 | 350.9 | 350.9 | 1.0 | 0.999731 | 0 | 20 | 0 | True | False | False |
| baseline | 1500 | 1497.8 | 4.3 | True | True | True | True | 0 | 107.8 | 1588.0 | 1588.0 | 1.0 | 0.999035 | 0 | 86 | 0 | True | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.8 | 3903.0 | 5962.1 | 0.774933 | 0.934351 | 3349 | 757 | 23501 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.5 | 8.1 | 51.6 | 0.664046 | 1.0 | 4999 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 1.0 | 0.94016 | 0.994795 | 1333 | 109 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.765467 | 0.995009 | 6384 | 104 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.7 | 5114.4 | 5766.2 | 0.792944 | 0.998051 | 3081 | 23 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.2 | 1.2 | 1.0 | 0.494691 | 0 | 7519 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 0.497177 | 0 | 7482 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.9 | 1.1 | True | True | True | True | 0 | 0.4 | 4.6 | 4.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.1 | 1.1 | True | True | True | True | 0 | 0.4 | 7.2 | 7.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.4 | 1.3 | True | True | True | True | 0 | 0.5 | 12.4 | 12.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.5 | 9.2 | True | True | True | True | 0 | 0.5 | 59.2 | 59.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3992.9 | 120.8 | False | True | True | False | gerador_atrasou | 0.9 | 252.9 | 252.9 | 1.0 | 0.999966 | 0 | 8 | 0 | True | True | False |
| lote_1000 | 6000 | 3714.0 | 45335.7 | False | True | True | True | 0 | 87.0 | 16133.0 | 54995.6 | 0.374762 | 0.991552 | 222955 | 1129 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1498.6 | 1.1 | True | True | True | True | 0 | 0.4 | 2.1 | 2.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 4.2 | 4.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.7 | 7.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.3 | 1.2 | True | True | True | True | 0 | 0.5 | 10.8 | 10.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.1 | 11.9 | True | True | True | True | 0 | 0.5 | 40.2 | 40.2 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_200 | 4000 | 3991.0 | 120.9 | False | True | True | False | gerador_atrasou | 1.0 | 307.0 | 307.0 | 1.0 | 0.999891 | 0 | 26 | 0 | True | False | False |
| lote_200 | 6000 | 4922.6 | 13018.1 | False | True | True | True | 0 | 122.3 | 5995.1 | 22603.1 | 0.436776 | 0.996507 | 200841 | 544 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 1.1 | True | True | True | True | 0 | 0.4 | 2.8 | 2.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.4 | 2.9 | 2.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1997.7 | 1.1 | True | True | True | True | 0 | 0.4 | 6.9 | 6.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.4 | 1.2 | True | True | True | True | 0 | 0.5 | 12.7 | 12.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2995.9 | 12.0 | True | True | True | True | 0 | 0.5 | 55.2 | 55.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3992.6 | 121.2 | False | True | True | False | gerador_atrasou | 0.8 | 273.2 | 273.2 | 1.0 | 0.999949 | 0 | 12 | 0 | True | True | False |
| lote_50 | 6000 | 5018.6 | 12819.4 | False | True | True | True | 0 | 112.7 | 5943.6 | 21748.2 | 0.250533 | 0.99803 | 267254 | 176 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1500 | 1000 | 500 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 3000 | 3000 | 3000 |
| lote_200 | 3000 | 3000 | 2500 |
| lote_50 | 3000 | 3000 | 3000 |
