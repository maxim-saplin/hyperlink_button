FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Ensure `uv sync` uses a consistent venv location.
# This matters when mounting the repo into /app during `docker run`.
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -Ls https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src
COPY examples /app/examples
COPY tests /app/tests

RUN uv venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

RUN uv sync --dev

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "examples/basic_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
