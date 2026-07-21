FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

RUN uv pip install diploma-frontend/dist/diploma-frontend-0.6.tar.gz

WORKDIR /app/megano

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
