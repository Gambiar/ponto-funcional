FROM elixir:1.17-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV MIX_ENV=prod LANG=C.UTF-8
WORKDIR /app
RUN mix local.hex --force && mix local.rebar --force

COPY mix.exs ./
COPY config ./config
RUN mix deps.get --only prod && mix deps.compile

COPY lib ./lib
RUN mix compile

EXPOSE 8000
CMD ["mix", "run", "--no-halt"]
