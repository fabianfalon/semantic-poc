# syntax=docker/dockerfile:1.4
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip         pip install --upgrade pip && pip install -r requirements.txt

FROM base AS final
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
