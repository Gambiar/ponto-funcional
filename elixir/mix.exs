defmodule Ponto.MixProject do
  use Mix.Project

  def project do
    [
      app: :ponto,
      version: "0.1.0",
      elixir: "~> 1.15",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      # testes sem iniciar a aplicação: não precisam de banco nem da porta 8000
      aliases: [test: "test --no-start"]
    ]
  end

  def application do
    [extra_applications: [:logger, :crypto], mod: {Ponto.Application, []}]
  end

  defp deps do
    [
      {:bandit, "~> 1.5"},
      {:plug, "~> 1.16"},
      {:jason, "~> 1.4"},
      {:postgrex, "~> 0.19"}
    ]
  end
end
