"""Teste de contrato: confere se uma implementação da API cumpre o mesmo contrato (C14).

Não é teste de carga: 20 req/s por poucos segundos. Roda contra a API que estiver
de pé (funcional, imperativa ou Elixir) e compara cada desfecho gravado com o
gabarito e o oráculo. Se as três versões passam, uma diferença no experimento vem
do estilo ou do runtime, e não de uma regra implementada de outro jeito.

    python -m ponto.carga.contrato            # usa API_URL e DATABASE_URL
    make contrato-elixir                       # sobe banco + API Elixir e roda
"""
from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

import aiohttp

from .experimento import API, Cenario, _admin, rodar_degrau

CHAVES_ESTADO = {"instancia", "config", "fila", "em_processamento", "ocioso", "em_andamento", "retries",
                 "lote_medio", "enfileirados", "recusados", "lotes", "registros_gravados_em_lote",
                 "registros_perdidos", "registros_corrompidos"}

# (nome, cenário, exige acerto total do gabarito original)
CASOS = [
    ("baseline", Cenario("contrato_baseline", modo="baseline", taxas=(20,), duracao=5, anomalias=0.2), True),
    ("lote", Cenario("contrato_lote", modo="lote", lote=50, taxas=(20,), duracao=5, anomalias=0.2), True),
    # queda de 2 s coberta pelo retry: nada pode se perder
    ("lote com falha e retry", Cenario("contrato_falha", modo="lote", lote=50, taxas=(20,), duracao=6,
                                       anomalias=0.2, falha_em=1, falha_seg=2.0), False),
    # a mesma queda, real (C17): as três APIs têm de reconhecer os erros do driver e repetir
    ("lote com queda real e retry", Cenario("contrato_falha_real", modo="lote", lote=50, taxas=(20,), duracao=6,
                                            anomalias=0.2, falha_em=1, falha_seg=2.0, falha_tipo="real"), False),
]


async def _checar_http() -> list[str]:
    problemas = []
    async with aiohttp.ClientSession() as s:
        estado = await _admin(s, "GET", "/admin/estado")
        if faltando := CHAVES_ESTADO - set(estado):
            problemas.append(f"/admin/estado sem as chaves {sorted(faltando)}")
        async with s.post(f"{API}/registros", json={"lixo": 1}) as r:
            corpo = await r.json(content_type=None)
            if r.status != 422 or corpo.get("erro") != "payload_invalido":
                problemas.append(f"payload inválido: esperado 422 payload_invalido, veio {r.status} {corpo}")
    return problemas


async def verificar() -> list[str]:
    problemas = await _checar_http()
    with tempfile.TemporaryDirectory() as tmp:
        for nome, c, exige_gabarito in CASOS:
            r = await rodar_degrau(c, c.taxas[0], Path(tmp))
            erros = {k: v for k, v in r.items() if k.startswith("n_")}
            ok = r["sem_erros"] and r["degrau_valido"] and (not exige_gabarito or r["acerto_gabarito"] == 1)
            print(f"  [{'OK ' if ok else 'ERR'}] {nome}: {r['registros']} registros, "
                  f"acerto_gabarito={r['acerto_gabarito']}, retries={r['retries']}, {erros or 'sem erros'}"
                  + (f", incidente={r['incidente']}" if r["incidente"] else ""))
            if not ok:
                problemas.append(f"{nome}: {erros or r['incidente'] or 'gabarito divergente'}")
            if c.falha_em is not None and r["retries"] == 0:
                problemas.append(f"{nome}: a falha não provocou nenhum retry")
    return problemas


def main() -> None:
    print(f"contrato da API em {API}")
    problemas = asyncio.run(verificar())
    for p in problemas:
        print(f"  FALHA: {p}")
    print("contrato OK" if not problemas else f"{len(problemas)} problema(s)")
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
