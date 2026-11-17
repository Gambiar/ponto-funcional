| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 1.9 | 4.0 | 4.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.7 | True | True | True | True | 0 | 1.5 | 4.4 | 4.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.5 | 11.7 | 11.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 1.8 | 93.7 | 93.7 | 1.0 | 0.999933 | 0 | 4 | 0 | True | True | False |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.2 | 347.3 | 347.3 | 1.0 | 0.999865 | 0 | 10 | 0 | True | False | False |
| baseline | 1500 | 1498.5 | 7.2 | True | True | True | True | 0 | 243.4 | 2552.6 | 2553.5 | 0.999865 | 0.998946 | 12 | 94 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.6 | 3429.1 | 5960.9 | 0.776486 | 0.940178 | 3325 | 691 | 23680 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.4 | 8.9 | 51.4 | 0.663888 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.940031 | 0.995085 | 1337 | 103 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.765557 | 0.994962 | 6382 | 105 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.7 | 5054.3 | 5830.5 | 0.787443 | 0.997951 | 3162 | 24 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 0.502823 | 0 | 7396 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 0.507999 | 0 | 7319 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 4.5 | 4.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.2 | 7.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.4 | 1.2 | True | True | True | True | 0 | 0.5 | 13.1 | 13.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.0 | 5.5 | True | True | True | True | 0 | 0.5 | 72.4 | 72.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3984.7 | 126.2 | False | True | True | False | gerador_atrasou | 1.7 | 313.8 | 313.8 | 1.0 | 0.999907 | 0 | 22 | 0 | True | True | False |
| lote_1000 | 6000 | 4030.3 | 35666.6 | False | True | True | True | 0 | 52.7 | 5718.1 | 44051.8 | 0.558903 | 0.997098 | 157183 | 578 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1498.7 | 1.1 | True | True | True | True | 0 | 0.4 | 2.2 | 2.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 4.3 | 4.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.9 | 7.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.5 | 33.2 | 33.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.2 | 6.7 | True | True | True | True | 0 | 0.5 | 67.4 | 67.4 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_200 | 4000 | 3992.3 | 126.9 | False | True | True | False | gerador_atrasou | 1.1 | 331.2 | 331.2 | 1.0 | 0.999933 | 0 | 16 | 0 | True | True | False |
| lote_200 | 6000 | 4643.0 | 13304.9 | False | True | True | True | 0 | 115.0 | 5486.1 | 22553.4 | 0.402188 | 0.996002 | 213028 | 573 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 2.2 | 2.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 6.5 | 6.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.2 | 7.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.4 | 1.2 | True | True | True | True | 0 | 0.5 | 14.0 | 14.0 | 1.0 | 0.999987 | 0 | 2 | 0 | True | True | False |
| lote_50 | 3000 | 2995.7 | 6.4 | True | True | True | True | 0 | 0.6 | 61.0 | 61.0 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_50 | 4000 | 3992.6 | 126.7 | False | True | True | False | gerador_atrasou | 0.9 | 303.3 | 303.3 | 1.0 | 0.99984 | 0 | 38 | 0 | True | False | False |
| lote_50 | 6000 | 5408.2 | 5622.1 | False | True | True | True | 0 | 139.8 | 5840.3 | 13127.5 | 0.222786 | 0.996851 | 276957 | 250 | 0 | False | False | False |

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
| lote_1000 | 3000 | 3000 | 3000 |
| lote_200 | 3000 | 3000 | 2500 |
| lote_50 | 3000 | 3000 | 2000 |
