| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 1.8 | 3.7 | 3.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.7 | True | True | True | True | 0 | 1.6 | 4.8 | 4.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.4 | 7.1 | 7.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 1.8 | 65.9 | 65.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.2 | 339.6 | 339.6 | 1.0 | 0.999812 | 0 | 14 | 0 | True | False | False |
| baseline | 1500 | 1499.0 | 1.3 | True | True | True | True | 0 | 5.0 | 524.0 | 524.0 | 1.0 | 0.999484 | 0 | 46 | 0 | True | False | False |
| falha_baseline_com_retry | 500 | 499.8 | 2.1 | True | True | True | True | 0 | 1.5 | 3504.6 | 5960.4 | 0.772381 | 0.936246 | 3379 | 731 | 23489 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.3 | 6.8 | 51.6 | 0.663119 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.940266 | 0.994944 | 1332 | 106 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.8 | 0.765895 | 0.995018 | 6381 | 104 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 5017.0 | 5788.8 | 0.779387 | 0.995765 | 3275 | 49 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 0.498484 | 0 | 7445 | 0 | True | False | False |
| falha_sem_retry | 500 | 500.0 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.509128 | 0 | 7287 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.7 | 1.2 | True | True | True | True | 0 | 0.4 | 25.1 | 25.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.4 | 8.0 | 8.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.4 | 1.1 | True | True | True | True | 0 | 0.4 | 11.1 | 11.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.1 | 5.6 | True | True | True | True | 0 | 0.5 | 57.8 | 57.8 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_1000 | 4000 | 3993.2 | 115.5 | False | True | True | False | gerador_atrasou | 1.2 | 261.9 | 261.9 | 1.0 | 0.999958 | 0 | 10 | 0 | True | True | False |
| lote_1000 | 6000 | 5330.1 | 13996.0 | False | True | True | True | 0 | 57.2 | 6477.9 | 22408.4 | 0.610663 | 0.995711 | 138845 | 934 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.4 | 5.2 | 5.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.4 | 6.6 | 6.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.6 | 1.2 | True | True | True | True | 0 | 0.5 | 10.2 | 10.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.3 | 12.3 | True | True | True | True | 0 | 0.5 | 72.2 | 72.2 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_200 | 4000 | 3992.9 | 104.1 | False | True | True | False | gerador_atrasou | 1.0 | 221.2 | 221.2 | 1.0 | 0.999857 | 0 | 34 | 0 | True | False | False |
| lote_200 | 6000 | 5705.1 | 3513.1 | False | True | True | True | 0 | 118.1 | 5934.9 | 10013.2 | 0.405623 | 0.995417 | 211966 | 663 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 3.5 | 3.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.1 | 7.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.5 | 13.6 | 13.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.2 | 4.3 | True | True | True | True | 0 | 0.5 | 64.3 | 64.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3992.9 | 124.1 | False | True | True | False | gerador_atrasou | 0.8 | 247.9 | 247.9 | 1.0 | 0.999958 | 0 | 10 | 0 | True | True | False |
| lote_50 | 6000 | 4727.9 | 18187.3 | False | True | True | True | 0 | 61.3 | 6345.8 | 22931.0 | 0.293052 | 0.997684 | 252111 | 242 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1500 | 1000 | 1000 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 3000 | 3000 | 2500 |
| lote_200 | 3000 | 3000 | 2500 |
| lote_50 | 3000 | 3000 | 3000 |
