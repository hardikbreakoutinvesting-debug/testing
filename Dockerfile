# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.14-slim AS builder

WORKDIR /app

# Install dependencies into an isolated prefix so we can copy only them later
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.14-slim AS runtime

# Security: run as non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY templates/ ./templates/
COPY calculator/ ./calculator/
COPY app.py .

# Switch to non-root user
USER appuser

# Expose Flask port
EXPOSE 9000

# Use gunicorn for production
ENV FLASK_APP=app.py
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "--timeout", "60", "app:app"]
