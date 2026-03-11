FROM python:3.11-slim

# Reliable defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# DigitalOcean App Platform binds PORT for you (defaults to 8080)
EXPOSE 8080

# Run with Gunicorn in production
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:${PORT} app:app"]
