# Stage 1: Install dependencies
FROM python:3.10-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.10-slim
RUN useradd -m -u 1000 appuser
WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY app/ .

RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]