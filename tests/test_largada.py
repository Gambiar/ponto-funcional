"""C16: com vários processos, a largada só acontece depois que todos têm a agenda,
então o começo do degrau não sai num surto atrasado."""
import asyncio

from aiohttp import web

from ponto.carga.rampa import disparar
from ponto.dados.gerador import gerar


async def _rodar(registros, taxa):
    async def eco(_):
        return web.json_response({"ok": True}, status=202)

    app = web.Application()
    app.router.add_post("/registros", eco)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    porta = site._server.sockets[0].getsockname()[1]
    try:
        return await disparar(registros, taxa, f"http://127.0.0.1:{porta}/registros", processos=2)
    finally:
        await runner.cleanup()


def test_varios_processos_partem_juntos_e_no_horario():
    registros = gerar(100, seed=1).registros  # ~200 registros a 200 req/s: ~1 s, carga mínima
    envios = asyncio.run(_rodar(registros, 200))
    assert len(envios) == len(registros)
    assert all(e.status == 202 for e in envios)
    primeiros = sorted(envios, key=lambda e: e.t_agendado)[:10]
    assert max(e.t_envio - e.t_agendado for e in primeiros) < 0.05
