FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    binutils \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/backend

# Collect static files at build time
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
