FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ARG APP_DIR=/app

RUN apt-get update

RUN apt-get upgrade -y
RUN apt-get autoremove --purge

RUN apt-get install -y --no-install-recommends \
    build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml $APP_DIR/pyproject.toml
COPY uv.lock $APP_DIR/uv.lock
COPY app $APP_DIR/app
WORKDIR $APP_DIR

RUN uv sync

ENTRYPOINT ["uv", "run", "fastapi"]