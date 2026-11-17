| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 1.9 | 3.8 | 3.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.7 | True | True | True | True | 0 | 1.6 | 3.6 | 3.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.8 | 1.7 | True | True | True | True | 0 | 1.8 | 10.8 | 10.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.4 | 1.1 | True | True | True | True | 0 | 2.1 | 168.0 | 168.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 4.6 | 450.3 | 450.3 | 1.0 | 0.999703 | 0 | 22 | 0 | True | False | False |
| baseline | 1500 | 1498.9 | 146.8 | False | True | True | True | 0 | 286.2 | 5219.9 | 5980.4 | 0.677647 | 0.951754 | 28751 | 2916 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.5 | 3411.4 | 5959.2 | 0.772642 | 0.939127 | 3379 | 699 | 23780 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.3 | 8.9 | 51.4 | 0.663504 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 0.4 | 0.8 | 0.7 | 0.94013 | 0.994984 | 1333 | 105 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.765384 | 0.995104 | 6386 | 102 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 4888.0 | 5790.0 | 0.777419 | 0.99775 | 3308 | 26 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 0.502422 | 0 | 7395 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 0.507132 | 0 | 7325 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.4 | 3.3 | 3.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.4 | 6.1 | 6.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.5 | 1.1 | True | True | True | True | 0 | 0.4 | 11.1 | 11.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.3 | 5.5 | True | True | True | True | 0 | 0.5 | 75.1 | 75.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3993.0 | 113.3 | False | True | True | False | gerador_atrasou | 1.4 | 255.9 | 255.9 | 1.0 | 0.999983 | 0 | 4 | 0 | True | True | False |
| lote_1000 | 6000 | 5176.3 | 17832.7 | False | True | True | True | 0 | 35.9 | 4963.7 | 28596.8 | 0.635864 | 0.995068 | 129820 | 1118 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 0.999832 | 0 | 1 | 0 | True | False | False |
| lote_200 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 2.2 | 2.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 4.8 | 4.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.4 | 6.6 | 6.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2495.1 | 1.2 | True | True | True | True | 0 | 0.5 | 12.9 | 12.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.1 | 4.9 | True | True | True | True | 0 | 0.5 | 78.3 | 78.3 | 1.0 | 0.999978 | 0 | 4 | 0 | True | True | False |
| lote_200 | 4000 | 3992.2 | 121.9 | False | True | True | False | gerador_atrasou | 1.0 | 286.1 | 286.1 | 1.0 | 0.999882 | 0 | 28 | 0 | True | False | False |
| lote_200 | 6000 | 4900.0 | 18889.2 | False | True | True | True | 0 | 60.8 | 8229.9 | 27943.6 | 0.452587 | 0.997124 | 195161 | 464 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 5.0 | 5.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.5 | 1.1 | True | True | True | True | 0 | 0.4 | 7.0 | 7.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2495.9 | 1.1 | True | True | True | True | 0 | 0.5 | 12.2 | 12.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.3 | 10.7 | True | True | True | True | 0 | 0.5 | 82.6 | 82.6 | 1.0 | 0.999978 | 0 | 4 | 0 | True | True | False |
| lote_50 | 4000 | 3992.3 | 138.6 | False | True | True | False | gerador_atrasou | 1.0 | 273.7 | 273.7 | 1.0 | 0.999848 | 0 | 36 | 0 | True | False | False |
| lote_50 | 6000 | 5974.4 | 1022.8 | False | True | True | True | 0 | 146.2 | 5619.0 | 6805.4 | 0.138965 | 0.996246 | 306972 | 186 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1250 | 1000 | 1000 |
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
| lote_50 | 3000 | 3000 | 2500 |
