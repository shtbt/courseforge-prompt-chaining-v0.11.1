FROM python:3.12-slim

# uv gives Docker the same dependency manager used by local development.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml README.md ./
RUN uv sync --no-dev

COPY main.py ./
COPY app ./app
COPY examples ./examples

CMD ["uv", "run", "--no-dev", "python", "main.py"]
