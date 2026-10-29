defmodule Ponto.Estado do
  @moduledoc """
  Estado da casca: configuração, validador e gravador em `:persistent_term`
  (leitura sem cópia, escrita rara) e contadores atômicos em `:counters`.
  """
  require Logger
  alias Ponto.{Nucleo, Repo, Retry}

  @indices %{
    em_andamento: 1,
    pendentes: 2,
    em_processamento: 3,
    enfileirados: 4,
    recusados: 5,
    lotes: 6,
    registros_gravados_em_lote: 7,
    registros_perdidos: 8,
    registros_corrompidos: 9,
    retries: 10,
    soma_tamanhos: 11,
    falha_ate: 12
  }
  @zeraveis [:enfileirados, :recusados, :lotes, :registros_gravados_em_lote, :registros_perdidos,
             :registros_corrompidos, :retries, :soma_tamanhos, :falha_ate]

  def iniciar(config) do
    :persistent_term.put({__MODULE__, :inicio}, System.monotonic_time(:millisecond))
    :persistent_term.put({__MODULE__, :contadores}, :counters.new(map_size(@indices), [:write_concurrency]))
    definir_cadastro(MapSet.new())
    configurar(config)
  end

  # ------------------------------------------------------------ contadores

  defp ref, do: :persistent_term.get({__MODULE__, :contadores})
  def incr(chave, n \\ 1), do: :counters.add(ref(), @indices[chave], n)
  def decr(chave, n \\ 1), do: :counters.sub(ref(), @indices[chave], n)
  def ler(chave), do: :counters.get(ref(), @indices[chave])
  def zerar, do: Enum.each(@zeraveis, &:counters.put(ref(), @indices[&1], 0))

  # relógio relativo ao início (sempre >= 0), para caber no contador
  def agora, do: System.monotonic_time(:millisecond) - :persistent_term.get({__MODULE__, :inicio})
  def falhar_por(segundos), do: :counters.put(ref(), @indices[:falha_ate], agora() + round(segundos * 1000))

  # ------------------------------------------------------------ configuração

  def config, do: :persistent_term.get({__MODULE__, :config})
  def validar, do: :persistent_term.get({__MODULE__, :validar})
  def gravador, do: :persistent_term.get({__MODULE__, :gravador})

  def configurar(config) do
    :persistent_term.put({__MODULE__, :config}, config)
    :persistent_term.put({__MODULE__, :gravador}, montar_gravador(config.tentativas))
    config
  end

  def definir_cadastro(cadastro) do
    :persistent_term.put({__MODULE__, :validar}, Nucleo.criar_validador(Nucleo.regras_padrao(cadastro)))
  end

  @doc "Compõe o gravador a partir de funções menores (equivale aos decoradores Python)."
  def montar_gravador(tentativas) do
    (&Repo.gravar_lote/1)
    |> Retry.traduzir_erros()
    |> Retry.com_falha_simulada(&agora/0, fn -> ler(:falha_ate) end)
    |> Retry.com_retry(tentativas,
      ao_falhar: fn n, erro ->
        incr(:retries)
        Logger.warning("tentativa #{n} falhou: #{Exception.message(erro)}")
      end
    )
  end
end
