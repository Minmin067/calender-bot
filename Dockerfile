# ベースイメージ
FROM python:3.11-slim

# タイムゾーン設定とシステム依存パッケージのインストール
ENV TZ=Asia/Tokyo

RUN apt-get update && apt-get install -y \
    tzdata \
    build-essential \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# ソースコードのコピー
COPY . /app

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# 実行コマンド（.envが必要なため注意）
CMD ["python", "bot.py"]
