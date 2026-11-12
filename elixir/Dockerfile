# mesma versão em que o contrato foi testado localmente (Elixir 1.20.3, OTP 29)
FROM elixir:1.20.3-otp-29-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV MIX_ENV=prod LANG=C.UTF-8
WORKDIR /app
RUN mix local.hex --force && mix local.rebar --force

# mix.lock fixa as versões das dependências testadas (as mesmas em toda máquina)
COPY mix.exs mix.lock ./
COPY config ./config
RUN mix deps.get --only prod && mix deps.compile

COPY lib ./lib
COPY test ./test
RUN mix compile

EXPOSE 8000
CMD ["mix", "run", "--no-halt"]
