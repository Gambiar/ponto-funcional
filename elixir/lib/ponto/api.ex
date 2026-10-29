defmodule Ponto.Api do
  @moduledoc "API HTTP (casca). Mesmo contrato de `ponto.casca.api`."
  use Plug.Router
  require Logger
  alias Ponto.{Estado, Fila, Nucleo, Repo, Retry}

  plug :match
  plug Plug.Parsers, parsers: [:json], pass: ["*/*"], json_decoder: Jason
  plug :dispatch

  post "/registros" do
    # o contador garante que o experimento só reinicia o banco sem requisições em curso
    Estado.incr(:em_andamento)

    try do
      case Nucleo.interpretar(conn.body_params) do
        nil -> responder(conn, 422, %{erro: "payload_invalido"})
        registro -> processar(conn, Estado.validar().(registro), Estado.config().modo)
      end
    after
      Estado.decr(:em_andamento)
    end
  end

  get "/saude" do
    responder(conn, 200, %{ok: true})
  end

  post "/admin/config" do
    campos =
      for {k, v} <- conn.body_params, k in ~w(modo tamanho_lote espera_ms tentativas), into: %{},
        do: {String.to_existing_atom(k), v}

    responder(conn, 200, Estado.configurar(Map.merge(Estado.config(), campos)))
  end

  post "/admin/reset" do
    n = conn.body_params["servidores"]
    {:ok, _} = Repo.reiniciar(n)
    Estado.definir_cadastro(MapSet.new(1..n))
    Estado.zerar()
    responder(conn, 200, %{servidores: n})
  end

  post "/admin/falha" do
    segundos =
      case Float.parse(to_string(conn.params["segundos"] || "10")) do
        {s, _} -> s
        :error -> 10.0
      end

    Estado.falhar_por(segundos)
    Logger.warning("falha simulada do banco por #{segundos} s")
    responder(conn, 200, %{segundos: segundos})
  end

  get "/admin/estado" do
    lotes = Estado.ler(:lotes)

    responder(conn, 200, %{
      config: Estado.config(),
      fila: Fila.tamanho(),
      em_processamento: Estado.ler(:em_processamento),
      ocioso: Estado.ler(:pendentes) == 0 and Estado.ler(:em_andamento) == 0,
      em_andamento: Estado.ler(:em_andamento),
      retries: Estado.ler(:retries),
      lote_medio: if(lotes > 0, do: Float.round(Estado.ler(:soma_tamanhos) / lotes, 1), else: 0),
      enfileirados: Estado.ler(:enfileirados),
      recusados: Estado.ler(:recusados),
      lotes: lotes,
      registros_gravados_em_lote: Estado.ler(:registros_gravados_em_lote),
      registros_perdidos: Estado.ler(:registros_perdidos),
      registros_corrompidos: Estado.ler(:registros_corrompidos)
    })
  end

  match _ do
    responder(conn, 404, %{erro: "nao_encontrado"})
  end

  # ------------------------------------------------------------------ modos

  defp processar(conn, resultado, "lote") do
    Estado.incr(:pendentes)

    if Fila.enfileirar(resultado) do
      Estado.incr(:enfileirados)
      responder(conn, 202, %{id_evento: Nucleo.registro(resultado).id_evento, situacao: "enfileirado"})
    else
      Estado.decr(:pendentes)
      Estado.incr(:recusados)
      responder(conn, 503, %{erro: "fila_cheia"})
    end
  end

  defp processar(conn, resultado, "baseline") do
    [{id, desfecho, motivo}] = Estado.gravador().([resultado])
    responder(conn, 201, %{id_evento: id, desfecho: desfecho, motivo: motivo})
  rescue
    Ponto.ErroDeDados ->
      responder(conn, 422, %{erro: "dado_corrompido"})

    erro ->
      if Retry.conexao?(erro),
        do: responder(conn, 503, %{erro: "banco_indisponivel"}),
        else: reraise(erro, __STACKTRACE__)
  end

  defp processar(conn, _resultado, outro), do: responder(conn, 500, %{erro: "modo desconhecido: #{outro}"})

  defp responder(conn, status, corpo) do
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(status, Jason.encode!(corpo))
  end
end
