FROM python:3.13-slim-bookworm

# Dev container for building/testing the Streamlit component.
# - Python 3.13
# - uv for dependency management
# - node/npm for frontend build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install a modern Node.js for building the frontend (Vite).
# We rely on NodeSource to avoid the older Debian-packaged Node.
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
  && apt-get update \
  && apt-get install -y --no-install-recommends nodejs \
  && rm -rf /var/lib/apt/lists/*

# Install uv (binary) into /root/.local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH=/root/.local/bin:$PATH

WORKDIR /work

CMD ["bash", "-lc", "sleep infinity"]
