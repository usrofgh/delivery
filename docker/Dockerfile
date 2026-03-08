FROM python:3.13-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV PYTHONPATH="/app"

WORKDIR /app
COPY ../pyproject.toml ../uv.lock ./
RUN pip install uv
RUN uv sync
RUN rm pyproject.toml uv.lock

COPY src .