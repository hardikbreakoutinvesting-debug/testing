# ── Stage 1: dependency builder ───────────────────────────────────────────────
FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: Apache + mod_wsgi runtime ────────────────────────────────────────
FROM python:3.14-slim AS runtime

# Install Apache2 and mod_wsgi for Python 3
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 \
        libapache2-mod-wsgi-py3 && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /install /usr/local

# ── App lives here (also the volume mount point used in CD pipeline) ──────────
WORKDIR /var/www/calculator-app

COPY templates/  ./templates/
COPY calculator/ ./calculator/
COPY app.py      ./app.py
COPY wsgi.py     ./wsgi.py

# ── Apache configuration ───────────────────────────────────────────────────────
COPY apache/calculator.conf /etc/apache2/sites-available/000-default.conf
RUN a2enmod wsgi headers && \
    a2dissite 000-default 2>/dev/null || true && \
    a2ensite  000-default

# Apache runs as www-data; grant read access to app files
RUN chown -R www-data:www-data /var/www/calculator-app

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
