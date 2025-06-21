# 📆 Calendar Bot for Discord

Discord上で「誕生日祝い」と「今日は何の日？」を自動通知するシンプルなBotです。  
Python製 + Discord API + Docker対応。

---

## 🚀 主な機能

### 🎂 誕生日祝い
- `!誕生日登録 MM/DD` でユーザー自身の誕生日を登録
- 当日 0:00 に祝福メッセージとロールを自動付与
- 翌日 0:00 にロールを自動で剥奪

### 🗓️ 今日の記念日
- [ざつねた.com](https://zatsuneta.com/category/anniversary.html) から記念日情報を毎日スクレイピング
- 毎日 0:00 に「今日は何の日？」を通知
- 重複した記念日は除去済み

---

## ⚙️ セットアップ方法

### 1. リポジトリをクローン

```bash
git clone https://github.com/Minmin067/calendar-bot.git
cd calendar-bot
```
### 2. .env ファイルを作成
以下の内容で .env をルートに配置：
```
DISCORD_TOKEN=（あなたのBotトークン）
BIRTHDAY_CHANNEL_ID=（誕生日メッセージ用チャンネルID）
BIRTHDAY_ROLE_ID=（誕生日ロールのID）
WHATDAY_CHANNEL_ID=（記念日通知用チャンネルID）
```

### 3. Dockerで起動
```
docker compose up -d --build
```

### 利用コマンド一覧
| コマンド           | 内容                    |
| -------------- | --------------------- |
| `!誕生日登録 MM/DD` | 自身の誕生日を登録（例: `06/07`） |
| `!誕生日削除`       | 登録された誕生日を削除           |
| `!誕生日確認`       | 現在登録されている誕生日を確認       |
| `!今日なに詳細`      | 今日の記念日一覧を即時取得（デバッグ用）  |
!今日なに詳細 は開発時の確認用。不要なら cogs/whatday.py でコメントアウトして運用してください。

### 🛠 技術スタック
- Python 3.11
- discord.py
- BeautifulSoup4（記念日スクレイピング）
- Docker / Docker Compose
- .tasks.loop() + sleep_until() により 0:00 定期実行を実現

### 👤 Author
- Github: Minmin067
