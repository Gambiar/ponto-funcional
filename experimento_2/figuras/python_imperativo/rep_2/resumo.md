| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 1.9 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.8 | True | True | True | True | 0 | 1.6 | 3.8 | 3.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.5 | 12.6 | 12.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 1.8 | 57.0 | 57.0 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1250 | 1249.4 | 1.2 | True | True | True | True | 0 | 2.2 | 277.4 | 277.4 | 1.0 | 0.999946 | 0 | 4 | 0 | True | True | False |
| baseline | 1500 | 1499.0 | 1.4 | True | True | True | True | 0 | 4.0 | 482.7 | 482.7 | 1.0 | 0.999753 | 0 | 22 | 0 | True | False | False |
| baseline | 1750 | 1748.6 | 203.1 | False | True | True | True | 0 | 248.0 | 5199.8 | 6016.9 | 0.637416 | 0.940323 | 37708 | 3956 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.9 | 3490.6 | 5964.6 | 0.775669 | 0.941967 | 3334 | 669 | 23697 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.7 | 11.1 | 51.6 | 0.663572 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 0.99852 | 0 | 22 | 6 | True | False | False |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 0.940085 | 0.995127 | 1334 | 102 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.765458 | 0.995008 | 6384 | 104 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.6 | 5162.6 | 5823.6 | 0.784417 | 0.997169 | 3204 | 33 | 0 | False | False | False |
| falha_real_com_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 0.502153 | 0 | 7399 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.506459 | 0 | 7335 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 0.999663 | 0 | 2 | 0 | True | False | False |
| lote_1000 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1248.9 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.9 | 1.1 | True | True | True | True | 0 | 0.4 | 2.6 | 2.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1997.5 | 1.1 | True | True | True | True | 0 | 0.4 | 5.4 | 5.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.4 | 9.2 | 9.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2996.0 | 3.5 | True | True | True | True | 0 | 0.5 | 46.1 | 46.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 4000 | 3992.5 | 97.9 | False | True | True | False | gerador_atrasou | 0.7 | 202.6 | 202.6 | 1.0 | 0.999949 | 0 | 12 | 0 | True | True | False |
| lote_1000 | 6000 | 5802.6 | 1588.0 | False | True | True | True | 0 | 97.5 | 5386.8 | 6896.2 | 0.514321 | 0.992938 | 173152 | 1295 | 0 | False | False | False |
| lote_200 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.2 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.8 | 1.1 | True | True | True | True | 0 | 0.4 | 3.5 | 3.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 4.3 | 4.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.4 | 8.4 | 8.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.3 | 7.7 | True | True | True | True | 0 | 0.5 | 43.0 | 43.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 4000 | 3992.4 | 95.7 | False | True | True | False | gerador_atrasou | 0.7 | 215.3 | 215.3 | 1.0 | 0.999899 | 0 | 24 | 0 | True | False | False |
| lote_200 | 6000 | 5734.7 | 3302.4 | False | True | True | True | 0 | 72.3 | 5517.2 | 9308.7 | 0.402294 | 0.996765 | 213091 | 464 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 0.998821 | 0 | 7 | 0 | True | False | False |
| lote_50 | 250 | 250.0 | 1.1 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.7 | 1.1 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.5 | 1.1 | True | True | True | True | 0 | 0.4 | 3.7 | 3.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 5.0 | 5.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2500 | 2497.6 | 1.1 | True | True | True | True | 0 | 0.4 | 9.6 | 9.6 | 1.0 | 0.999987 | 0 | 2 | 0 | True | True | False |
| lote_50 | 3000 | 2996.3 | 1.7 | True | True | True | True | 0 | 0.5 | 20.7 | 20.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 4000 | 3985.3 | 108.3 | False | True | True | False | gerador_atrasou | 0.7 | 236.2 | 236.2 | 1.0 | 0.999966 | 0 | 8 | 0 | True | True | False |
| lote_50 | 6000 | 5720.9 | 2555.3 | False | True | True | True | 0 | 73.0 | 6493.6 | 8422.6 | 0.177614 | 0.995025 | 293193 | 315 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1500 | 1250 | 500 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | None | None |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 3000 | None | None |
| lote_200 | 3000 | 3000 | 3000 |
| lote_50 | 3000 | None | None |
