FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl git \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -U uv

COPY pyproject.toml /app/pyproject.toml
COPY README.md /app/README.md
COPY hyperlink_button /app/hyperlink_button
COPY tests /app/tests

# Install Python deps (un-pinned, as requested).
RUN uv pip install --system -e ".[dev]"

# Install Playwright + Chromium + system deps.
RUN python -m playwright install --with-deps chromium

CMD ["pytest", "-q"]
