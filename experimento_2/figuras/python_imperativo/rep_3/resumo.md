| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 1.7 | 4.5 | 4.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.6 | True | True | True | True | 0 | 1.5 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.4 | 6.2 | 6.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 1.6 | 59.3 | 59.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.0 | 264.8 | 264.8 | 1.0 | 0.999919 | 0 | 6 | 0 | True | True | False |
| baseline | 1500 | 1499.1 | 1.3 | True | True | True | True | 0 | 3.8 | 488.5 | 488.5 | 1.0 | 0.999776 | 0 | 20 | 0 | True | False | False |
| baseline | 1750 | 1748.2 | 193.2 | False | True | True | True | 0 | 243.2 | 5357.0 | 5990.3 | 0.638848 | 0.940505 | 37523 | 3949 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.6 | 3506.8 | 5963.4 | 0.772718 | 0.934356 | 3374 | 753 | 23667 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.4 | 5.3 | 51.4 | 0.663186 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.999461 | 0 | 8 | 6 | True | False | False |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.939683 | 0.995084 | 1345 | 103 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.8 | 0.765822 | 0.995066 | 6383 | 103 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 5099.2 | 5790.8 | 0.779387 | 0.997753 | 3275 | 26 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.8 | 1.5 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 0.500505 | 0 | 7415 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.501246 | 0 | 7404 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 3.0 | 3.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.4 | 4.7 | 4.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.5 | 1.1 | True | True | True | True | 0 | 0.4 | 9.4 | 9.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.2 | 1.6 | True | True | True | True | 0 | 0.4 | 24.1 | 24.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.1 | 122.9 | False | True | True | False | gerador_atrasou | 0.7 | 210.5 | 210.5 | 1.0 | 0.999983 | 0 | 4 | 0 | True | True | False |
| lote_1000 | 6000 | 5681.5 | 3020.9 | False | True | True | True | 0 | 97.2 | 5748.4 | 9082.5 | 0.609062 | 0.996018 | 139416 | 865 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.0 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.4 | 2.9 | 2.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 3.2 | 3.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.4 | 1.1 | True | True | True | True | 0 | 0.4 | 8.4 | 8.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2995.7 | 3.3 | True | True | True | True | 0 | 0.4 | 17.1 | 17.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3993.4 | 101.9 | False | True | True | False | gerador_atrasou | 0.6 | 210.5 | 210.5 | 1.0 | 0.999958 | 0 | 10 | 0 | True | True | False |
| lote_200 | 6000 | 5958.2 | 567.8 | False | True | True | True | 0 | 29.7 | 4876.9 | 6044.2 | 0.196352 | 0.997686 | 286596 | 162 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 0.997647 | 0 | 14 | 0 | True | False | False |
| lote_50 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1498.9 | 1.1 | True | True | True | True | 0 | 0.4 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.4 | 3.2 | 3.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.4 | 5.6 | 5.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.6 | 1.2 | True | True | True | True | 0 | 0.4 | 10.2 | 10.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.2 | 2.6 | True | True | True | True | 0 | 0.5 | 26.4 | 26.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3992.8 | 99.0 | False | True | True | False | gerador_atrasou | 0.7 | 193.0 | 193.0 | 1.0 | 0.999924 | 0 | 18 | 0 | True | True | False |
| lote_50 | 6000 | 5720.6 | 2342.5 | False | True | True | True | 0 | 94.8 | 6039.2 | 8418.1 | 0.190708 | 0.996383 | 288609 | 246 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1500 | 1250 | 1000 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | None | None |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 3000 | 3000 | 3000 |
| lote_200 | 3000 | 3000 | 3000 |
| lote_50 | 3000 | None | None |
