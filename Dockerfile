FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.22 /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONPATH=/app/backend

COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --frozen --no-dev
COPY backend ./backend

EXPOSE 8000
CMD ["uv", "run", "--no-dev", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
