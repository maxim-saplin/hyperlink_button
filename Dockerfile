FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml README.md MANIFEST.in /app/
COPY hyperlink_button /app/hyperlink_button
COPY examples /app/examples

RUN python -m pip install --upgrade pip \
  && python -m pip install .

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "examples/demo_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
