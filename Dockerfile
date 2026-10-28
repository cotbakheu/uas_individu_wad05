FROM node:22-alpine AS frontend-build

WORKDIR /workspace/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./backend/
COPY backend/src ./backend/src
RUN pip install --no-cache-dir uv
RUN uv sync --project /app/backend --no-dev

COPY backend/ ./backend/
COPY --from=frontend-build /workspace/frontend/dist ./frontend/dist

WORKDIR /app/backend
ENV PATH="/app/backend/.venv/bin:$PATH"
CMD ["sh", "-c", "uvicorn app.main:app --app-dir src --host 0.0.0.0 --port ${PORT:-8000}"]
