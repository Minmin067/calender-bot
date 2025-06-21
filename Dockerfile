# Dockerfile

FROM python:3.11-slim

# 必要なシステム依存パッケージ（scrapingに必要）
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
