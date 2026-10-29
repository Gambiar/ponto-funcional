defmodule Ponto.Application do
  @moduledoc false
  use Application
  require Logger

  @impl true
  def start(_type, _args) do
    Ponto.Estado.iniciar(%{
      modo: env("MODO", "lote"),
      tamanho_lote: String.to_integer(env("TAMANHO_LOTE", "200")),
      espera_ms: String.to_integer(env("ESPERA_MS", "100")),
      tentativas: String.to_integer(env("TENTATIVAS", "8"))
    })

    filhos = [
      {Postgrex, [name: Ponto.DB, pool_size: String.to_integer(env("POOL_MAX", "20"))] ++ banco()},
      {Ponto.Fila, String.to_integer(env("FILA_CAPACIDADE", "10000"))},
      Ponto.Consumidor
    ]

    {:ok, sup} = Supervisor.start_link(filhos, strategy: :one_for_one, name: Ponto.Supervisor)

    # o banco pode demorar a aceitar conexões: o mesmo retry da gravação resolve
    Ponto.Retry.com_retry(&Ponto.Repo.criar_esquema/1, 10, base: 0.5).(nil)
    Ponto.Estado.definir_cadastro(Ponto.Repo.carregar_cadastro())

    # HTTP só sobe depois do esquema: a checagem de saúde passa a significar "pronto"
    {:ok, _} = Supervisor.start_child(sup, {Bandit, plug: Ponto.Api, port: 8000})
    Logger.warning("API Elixir pronta: #{inspect(Ponto.Estado.config())}")
    {:ok, sup}
  end

  defp env(nome, padrao), do: System.get_env(nome, padrao)

  defp banco do
    uri = URI.parse(env("DATABASE_URL", "postgresql://ponto:ponto@localhost:5432/ponto"))
    [usuario, senha] = String.split(uri.userinfo, ":", parts: 2)

    [
      hostname: uri.host,
      port: uri.port || 5432,
      username: usuario,
      password: senha,
      database: String.trim_leading(uri.path, "/")
    ]
  end
end
