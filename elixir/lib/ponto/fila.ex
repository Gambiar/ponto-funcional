defmodule Ponto.Fila do
  @moduledoc """
  Fila com back-pressure (recusa quando cheia) num processo GenServer.

  O consumidor pede um lote com `coletar/2`: a resposta sai quando há `max`
  itens ou quando vencem `espera_ms` desde que o primeiro item ficou disponível
  — a mesma regra de `ProcessadorDeLotes._coletar` da versão Python.
  O estado é um valor imutável substituído a cada mensagem.
  """
  use GenServer

  def start_link(capacidade), do: GenServer.start_link(__MODULE__, capacidade, name: __MODULE__)

  def enfileirar(item), do: GenServer.call(__MODULE__, {:enfileirar, item})
  def coletar(max, espera_ms), do: GenServer.call(__MODULE__, {:coletar, max, espera_ms}, :infinity)
  def tamanho, do: GenServer.call(__MODULE__, :tamanho)

  @impl true
  def init(capacidade) do
    {:ok, %{q: :queue.new(), n: 0, cap: capacidade, esperando: nil, prazo: nil}}
  end

  @impl true
  def handle_call({:enfileirar, _}, _from, %{n: n, cap: cap} = s) when n >= cap, do: {:reply, false, s}

  def handle_call({:enfileirar, item}, _from, s),
    do: {:reply, true, servir(%{s | q: :queue.in(item, s.q), n: s.n + 1})}

  def handle_call({:coletar, max, espera}, from, s),
    do: {:noreply, servir(%{s | esperando: {from, max, espera}})}

  def handle_call(:tamanho, _from, s), do: {:reply, s.n, s}

  @impl true
  def handle_info({:prazo, ref}, %{prazo: {_, ref}, esperando: {from, max, _}} = s),
    do: {:noreply, entregar(s, from, max)}

  # prazo de um lote já entregue
  def handle_info({:prazo, _}, s), do: {:noreply, s}

  defp servir(%{esperando: nil} = s), do: s
  defp servir(%{esperando: {from, max, _}, n: n} = s) when n >= max, do: entregar(s, from, max)

  defp servir(%{esperando: {_, _, espera}, n: n, prazo: nil} = s) when n > 0 do
    ref = make_ref()
    %{s | prazo: {Process.send_after(self(), {:prazo, ref}, espera), ref}}
  end

  defp servir(s), do: s

  defp entregar(s, from, max) do
    k = min(max, s.n)
    {lote, resto} = :queue.split(k, s.q)
    with {timer, _} <- s.prazo, do: Process.cancel_timer(timer)
    GenServer.reply(from, :queue.to_list(lote))
    %{s | q: resto, n: s.n - k, esperando: nil, prazo: nil}
  end
end

defmodule Ponto.Consumidor do
  @moduledoc "Consome lotes da fila e grava, isolando registros corrompidos por bisseção."
  use Task, restart: :permanent
  require Logger
  alias Ponto.{Estado, Fila, Nucleo}

  def start_link(_), do: Task.start_link(&consumir/0)

  def consumir do
    cfg = Estado.config()
    lote = Fila.coletar(cfg.tamanho_lote, cfg.espera_ms)
    n = length(lote)
    Estado.incr(:em_processamento, n)

    try do
      gravar_isolando_falhas(Estado.gravador(), lote)
      Estado.incr(:lotes)
      Estado.incr(:registros_gravados_em_lote, n)
      Estado.incr(:soma_tamanhos, n)
    rescue
      erro ->
        Estado.incr(:registros_perdidos, n)
        Logger.error("lote de #{n} registros perdido: #{Exception.message(erro)}")
    after
      Estado.decr(:em_processamento, n)
      Estado.decr(:pendentes, n)
    end

    consumir()
  end

  @doc "Recursão de bisseção: profundidade máxima log2(tamanho do lote)."
  def gravar_isolando_falhas(gravar, lote) do
    gravar.(lote)
  rescue
    erro in Ponto.ErroDeDados ->
      case lote do
        [unico] ->
          Estado.incr(:registros_corrompidos)
          Logger.warning("registro #{Nucleo.registro(unico).id_evento} descartado: #{erro.message}")

        _ ->
          {esquerda, direita} = Nucleo.bissectar(lote)
          gravar_isolando_falhas(gravar, esquerda)
          gravar_isolando_falhas(gravar, direita)
      end
  end
end
