# cogs/whatday.py

from discord.ext import commands, tasks
import discord, requests, os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

CHANNEL_ID = int(os.getenv("WHATDAY_CHANNEL_ID"))

def scrape_today():
    url = "https://zatsuneta.com/category/anniversary.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    today_str = datetime.now().strftime("%-m月%-d日")  # 例: 6月21日

    result = []
    for a in soup.find_all("a"):
        title = a.get("title", "")
        if today_str in title:
            result.append(a.text.strip())

    # 重複を削除
    unique = list(dict.fromkeys(result))

    # 不要な行を除外:
    # - ページ見出し「今日 2月26日（木）の記念日・年中行事」
    # - 日付だけの「26」などの数字のみの行
    filtered = []
    for text in unique:
        # 見出し行（「今日 ～ の記念日・年中行事」）はスキップ
        if "今日 " in text and "の記念日・年中行事" in text:
            continue
        # 数字だけの行（カレンダーの日付リンクなど）はスキップ
        if text.isdigit():
            continue
        filtered.append(text)

    return filtered

class WhatDay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_daily_message.start()

    @tasks.loop(hours=24)
    async def send_daily_message(self):
        await self.bot.wait_until_ready()
        try:
            items = scrape_today()
        except Exception as e:
            print(f"[WhatDay] Failed to scrape: {e}")
            return

        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            if items:
                msg = f"📅 {datetime.now().strftime('%-m月%-d日')}はこんな日：\n- " + "\n- ".join(items)
            else:
                msg = f"📅 {datetime.now().strftime('%-m月%-d日')}は特にイベントが見つかりませんでした。"
            await channel.send(msg)

    # 以下はテスト用コマンド。運用時は無効化
    # @commands.command(name="今日なに詳細")
    # async def whatday_full(self, ctx):
    #     try:
    #         items = scrape_today()
    #     except Exception as e:
    #         await ctx.send(f"⚠️ スクレイピングに失敗しました: {e}")
    #         return

    #     if items:
    #         msg = f"📅 {datetime.now().strftime('%-m月%-d日')}はこんな日：\n- " + "\n- ".join(items)
    #     else:
    #         msg = f"📅 {datetime.now().strftime('%-m月%-d日')}は特にイベントが見つかりませんでした。"

    #     await ctx.send(msg)

    @send_daily_message.before_loop
    async def wait_until_midnight(self):
        now = datetime.now()
        target = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)
        await discord.utils.sleep_until(target)

async def setup(bot):
    await bot.add_cog(WhatDay(bot))
