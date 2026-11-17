| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.3 | 5.1 | 5.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.0 | 5.4 | 5.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.8 | 8.2 | 8.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 2.8 | 34.0 | 34.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.3 | 1.8 | True | True | True | True | 0 | 98.8 | 3421.1 | 5182.8 | 0.987163 | 0.999591 | 954 | 30 | 23118 | False | False | False |
| baseline | 1500 | 1499.0 | 13.2 | True | True | True | True | 0 | 116.2 | 3653.5 | 5885.5 | 0.903753 | 0.994116 | 8579 | 474 | 104786 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 2.3 | 3954.1 | 5963.2 | 0.77183 | 0.932643 | 3397 | 774 | 26079 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | True | True | True | 0 | 1.8 | 7.7 | 51.5 | 0.664092 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.939785 | 0.994947 | 1344 | 106 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.7655 | 0.995067 | 6396 | 103 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.7 | 2.0 | True | True | True | True | 0 | 1.9 | 16.9 | 3994.9 | 0.662346 | 1.0 | 5027 | 0 | 0 | False | True | False |
| falha_real_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 5 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.93619 | 0 | 950 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.503694 | 0 | 7389 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.3 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.3 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.3 | 1.5 | True | True | True | True | 0 | 0.3 | 3.5 | 3.5 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_1000 | 4000 | 3993.3 | 44.8 | False | True | True | False | gerador_atrasou | 0.4 | 24.9 | 24.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 6000 | 5979.4 | 261.2 | False | True | True | False | gerador_atrasou | 0.6 | 129.4 | 129.4 | 1.0 | 0.999978 | 0 | 8 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.3 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.1 | 1.8 | True | True | True | True | 0 | 0.4 | 6.1 | 6.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.1 | 45.4 | False | True | True | False | gerador_atrasou | 0.4 | 24.6 | 24.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 6000 | 5978.5 | 257.9 | False | True | True | False | gerador_atrasou | 0.6 | 135.4 | 135.4 | 1.0 | 0.999983 | 0 | 6 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.3 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.3 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.3 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.3 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.3 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.3 | 1.9 | True | True | True | True | 0 | 0.4 | 4.4 | 4.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3993.3 | 74.4 | False | True | True | False | gerador_atrasou | 0.4 | 35.0 | 35.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 6000 | 5970.3 | 256.6 | False | True | True | False | gerador_atrasou | 0.6 | 135.9 | 135.9 | 1.0 | 0.999994 | 0 | 2 | 0 | True | True | False |

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
| lote_1000 | 3000 | 3000 | 2500 |
| lote_200 | 3000 | 3000 | 3000 |
| lote_50 | 3000 | 3000 | 3000 |
