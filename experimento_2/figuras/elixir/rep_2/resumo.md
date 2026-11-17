| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.2 | 4.8 | 4.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.9 | 4.7 | 4.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.8 | 6.9 | 6.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 2.1 | 30.1 | 30.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.2 | 1.6 | True | True | True | True | 0 | 79.8 | 1978.0 | 5039.7 | 0.989795 | 0.999837 | 757 | 12 | 20137 | False | False | False |
| baseline | 1500 | 1499.0 | 15.2 | True | True | True | True | 0 | 115.2 | 3602.6 | 5915.1 | 0.914509 | 0.985791 | 7625 | 1159 | 83669 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.9 | 3744.4 | 5965.7 | 0.771565 | 0.939217 | 3395 | 697 | 24849 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 1.6 | 8.4 | 51.4 | 0.663572 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.8 | 1.4 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 0.939636 | 0.995029 | 1344 | 104 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 0.765017 | 0.995006 | 6396 | 104 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.6 | 17.2 | 5042.0 | 0.662091 | 1.0 | 5022 | 0 | 0 | False | True | False |
| falha_real_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 5 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.93803 | 0 | 921 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 0.507267 | 0 | 7323 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.3 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.7 | 1.3 | True | True | True | True | 0 | 0.3 | 5.7 | 5.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.4 | 47.5 | False | True | True | False | gerador_atrasou | 0.4 | 27.2 | 27.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 6000 | 5984.0 | 324.7 | False | True | True | False | gerador_atrasou | 0.6 | 457.2 | 457.2 | 1.0 | 0.999994 | 0 | 2 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.6 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.4 | 1.1 | True | True | True | True | 0 | 0.3 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.2 | 1.3 | True | True | True | True | 0 | 0.4 | 4.4 | 4.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.2 | 49.3 | False | True | True | False | gerador_atrasou | 0.4 | 26.6 | 26.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 6000 | 5982.6 | 239.4 | False | True | True | False | gerador_atrasou | 0.6 | 115.1 | 115.1 | 1.0 | 0.999994 | 0 | 2 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.6 | 0.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.3 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.3 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.2 | 14.4 | True | True | True | True | 0 | 0.4 | 9.4 | 9.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3993.6 | 56.5 | False | True | True | False | gerador_atrasou | 0.4 | 24.4 | 24.4 | 1.0 | 0.999992 | 0 | 2 | 0 | True | True | False |
| lote_50 | 6000 | 5949.4 | 240.5 | False | True | True | False | gerador_atrasou | 0.6 | 162.1 | 162.1 | 1.0 | 0.999989 | 0 | 4 | 0 | True | True | False |

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
