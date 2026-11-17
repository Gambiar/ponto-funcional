| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.2 | 4.6 | 4.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 1.9 | 6.2 | 6.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 11.9 | 11.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 1.9 | 85.1 | 85.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.3 | 338.1 | 338.1 | 1.0 | 0.999919 | 0 | 6 | 0 | True | True | False |
| baseline | 1500 | 1498.9 | 3.2 | True | True | True | True | 0 | 65.6 | 1586.6 | 1586.6 | 1.0 | 0.999551 | 0 | 40 | 0 | True | False | False |
| baseline | 1750 | 1748.0 | 229.9 | False | True | True | True | 0 | 279.7 | 5443.8 | 6046.7 | 0.554685 | 0.94364 | 46323 | 3252 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 2.1 | 3750.6 | 5961.3 | 0.778009 | 0.942761 | 3305 | 663 | 23212 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.5 | 6.6 | 51.4 | 0.664092 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.940143 | 0.995044 | 1336 | 104 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.8 | 0.766013 | 0.99507 | 6382 | 103 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 2.0 | 5087.6 | 5781.9 | 0.782106 | 0.997424 | 3244 | 30 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 0.498186 | 0 | 7471 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 0.510478 | 0 | 7288 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1248.8 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.5 | 1.1 | True | True | True | True | 0 | 0.4 | 4.0 | 4.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.4 | 4.7 | 4.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.4 | 1.1 | True | True | True | True | 0 | 0.4 | 8.2 | 8.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.1 | 2.5 | True | True | True | True | 0 | 0.5 | 24.5 | 24.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.1 | 107.5 | False | True | True | False | gerador_atrasou | 0.7 | 237.8 | 237.8 | 1.0 | 0.999983 | 0 | 4 | 0 | True | True | False |
| lote_1000 | 6000 | 4564.9 | 20897.9 | False | True | True | True | 0 | 56.9 | 5833.7 | 26562.6 | 0.656464 | 0.994146 | 122479 | 1370 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 0.999664 | 0 | 2 | 0 | True | False | False |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 3.2 | 3.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 4.5 | 4.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.5 | 1.1 | True | True | True | True | 0 | 0.4 | 9.1 | 9.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.1 | 3.0 | True | True | True | True | 0 | 0.5 | 32.9 | 32.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.1 | 102.6 | False | True | True | False | gerador_atrasou | 0.7 | 212.3 | 212.3 | 1.0 | 0.999941 | 0 | 14 | 0 | True | True | False |
| lote_200 | 6000 | 5732.4 | 3228.1 | False | True | True | True | 0 | 105.4 | 6289.5 | 8636.9 | 0.359917 | 0.996158 | 228205 | 493 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 0.997145 | 0 | 17 | 0 | True | False | False |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1498.8 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 3.3 | 3.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.4 | 6.0 | 6.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.2 | 1.2 | True | True | True | True | 0 | 0.5 | 10.5 | 10.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.2 | 5.1 | True | True | True | True | 0 | 0.5 | 41.3 | 41.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3993.0 | 106.4 | False | True | True | False | gerador_atrasou | 0.8 | 219.6 | 219.6 | 1.0 | 0.999907 | 0 | 22 | 0 | True | True | False |
| lote_50 | 6000 | 5878.2 | 1249.3 | False | True | True | True | 0 | 126.7 | 5734.4 | 6976.5 | 0.175624 | 0.99342 | 293910 | 412 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1500 | 1250 | 1000 |
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
| lote_200 | 3000 | None | None |
| lote_50 | 3000 | None | None |
