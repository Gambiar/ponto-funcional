| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.0 | 5.0 | 5.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.8 | True | True | True | True | 0 | 1.6 | 5.8 | 5.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 9.2 | 9.2 | 1.0 | 0.999933 | 0 | 2 | 0 | True | True | False |
| baseline | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 2.0 | 120.1 | 120.1 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.3 | 322.6 | 322.6 | 1.0 | 0.999919 | 0 | 6 | 0 | True | True | False |
| baseline | 1500 | 1499.0 | 7.9 | True | True | True | True | 0 | 179.2 | 2326.4 | 2327.2 | 0.99991 | 0.999237 | 8 | 68 | 0 | False | False | False |
| baseline | 1750 | 1748.1 | 247.6 | False | True | True | True | 0 | 319.2 | 5422.1 | 6036.9 | 0.561777 | 0.942274 | 45580 | 3373 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.9 | 3554.0 | 5964.2 | 0.771578 | 0.934483 | 3398 | 752 | 23563 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.5 | 10.1 | 51.5 | 0.663888 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.940076 | 0.99499 | 1336 | 105 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.76541 | 0.995201 | 6386 | 100 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.6 | 5023.1 | 5789.8 | 0.777494 | 0.994812 | 3310 | 60 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 0.503092 | 0 | 7392 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 0.507663 | 0 | 7324 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 0.999326 | 0 | 4 | 0 | True | False | False |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 3.0 | 3.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.4 | 1.2 | True | True | True | True | 0 | 0.4 | 10.0 | 10.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.1 | 11.0 | True | True | True | True | 0 | 0.5 | 56.6 | 56.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3992.9 | 115.5 | False | True | True | False | gerador_atrasou | 0.7 | 213.0 | 213.0 | 1.0 | 0.999966 | 0 | 8 | 0 | True | True | False |
| lote_1000 | 6000 | 5904.7 | 628.6 | False | True | True | True | 0 | 52.8 | 4225.3 | 6115.4 | 0.428642 | 0.99037 | 203601 | 1471 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1248.9 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.4 | 3.1 | 3.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 5.5 | 5.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.5 | 1.3 | True | True | True | True | 0 | 0.4 | 9.8 | 9.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2995.3 | 3.2 | True | True | True | True | 0 | 0.5 | 32.8 | 32.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3991.7 | 113.3 | False | True | True | False | gerador_atrasou | 0.7 | 276.6 | 276.6 | 1.0 | 0.999907 | 0 | 22 | 0 | True | True | False |
| lote_200 | 6000 | 5767.4 | 2908.9 | False | True | True | True | 0 | 112.3 | 6245.2 | 8671.5 | 0.335963 | 0.995798 | 236627 | 503 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 0.999831 | 0 | 1 | 0 | True | False | False |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.2 | 1.1 | True | True | True | True | 0 | 0.4 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.6 | 1.1 | True | True | True | True | 0 | 0.4 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.1 | 7.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.3 | 1.2 | True | True | True | True | 0 | 0.5 | 12.5 | 12.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.1 | 14.7 | True | True | True | True | 0 | 0.5 | 49.7 | 49.7 | 1.0 | 0.999978 | 0 | 4 | 0 | True | True | False |
| lote_50 | 4000 | 3992.5 | 118.1 | False | True | True | False | gerador_atrasou | 0.7 | 236.2 | 236.2 | 1.0 | 0.999941 | 0 | 14 | 0 | True | True | False |
| lote_50 | 6000 | 5687.6 | 2640.7 | False | True | True | True | 0 | 111.3 | 6257.4 | 8140.7 | 0.174471 | 0.996638 | 294174 | 209 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1250 | 1250 | 250 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 3000 | None | None |
| lote_200 | 3000 | 3000 | 3000 |
| lote_50 | 3000 | None | None |
