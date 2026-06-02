FROM python:3.11-slim

# Install system dependencies for GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    binutils \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL library path so Django can find it
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Collect static files (skipped here, runs as part of release in Railway)
WORKDIR /app/backend

# Railway sets $PORT at runtime
EXPOSE 8000

CMD gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
