from discord.ext import commands, tasks
import discord, datetime, json, os

BIRTHDAY_FILE = "data/birthdays.json"
CHANNEL_ID = int(os.getenv("BIRTHDAY_CHANNEL_ID"))
ROLE_ID = int(os.getenv("BIRTHDAY_ROLE_ID"))

def load_birthdays():
    if not os.path.exists(BIRTHDAY_FILE):
        return {}
    with open(BIRTHDAY_FILE, "r") as f:
        return json.load(f)

def save_birthdays(data):
    with open(BIRTHDAY_FILE, "w") as f:
        json.dump(data, f)

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_give.start()
        self.birthday_remove.start()

    @commands.command(name="誕生日登録")
    async def register(self, ctx, date: str):
        try:
            datetime.datetime.strptime(date, "%m/%d")
        except ValueError:
            await ctx.send("📛 フォーマットは MM/DD で指定してね (例: 06/07)")
            return

        bds = load_birthdays()
        bds[str(ctx.author.id)] = date
        save_birthdays(bds)
        await ctx.send(f"🎂 {ctx.author.display_name} さんの誕生日を {date} に登録したよ！")

    @commands.command(name="誕生日削除")
    async def delete_birthday(self, ctx):
        bds = load_birthdays()
        if str(ctx.author.id) in bds:
            del bds[str(ctx.author.id)]
            save_birthdays(bds)
            await ctx.send("🗑️ 誕生日を削除したよ！")
        else:
            await ctx.send("📛 登録されていません。")

    @commands.command(name="誕生日確認")
    async def show_birthday(self, ctx):
        bds = load_birthdays()
        date = bds.get(str(ctx.author.id))
        if date:
            await ctx.send(f"📅 あなたの誕生日は `{date}` に登録されてるよ！")
        else:
            await ctx.send("📛 まだ誕生日が登録されていません。")

    @tasks.loop(hours=24)
    async def birthday_give(self):
        await self.bot.wait_until_ready()
        today = datetime.datetime.now().strftime("%m/%d")
        bds = load_birthdays()

        for guild in self.bot.guilds:
            role = guild.get_role(ROLE_ID)
            channel = self.bot.get_channel(CHANNEL_ID)
            if not role or not channel:
                continue

            for uid, date in bds.items():
                if date == today:
                    member = guild.get_member(int(uid))
                    if member:
                        await member.add_roles(role, reason="🎂 誕生日ロール付与")
                        await channel.send(f"🎉 今日は {member.mention} の誕生日！おめでとう〜！ 🎂")

    @tasks.loop(hours=24)
    async def birthday_remove(self):
        await self.bot.wait_until_ready()
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d")
        bds = load_birthdays()

        for guild in self.bot.guilds:
            role = guild.get_role(ROLE_ID)
            if not role:
                continue

            for uid, date in bds.items():
                if date == yesterday:
                    member = guild.get_member(int(uid))
                    if member and role in member.roles:
                        await member.remove_roles(role, reason="🎂 誕生日ロール剥奪")

    @birthday_give.before_loop
    @birthday_remove.before_loop
    async def wait_until_midnight(self):
        now = datetime.datetime.now()
        target = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if now >= target:
            target += datetime.timedelta(days=1)
        await discord.utils.sleep_until(target)

    # === 🛠 デバッグ用コマンド（必要なときだけ有効化） ===

    # @commands.command(name="誕生日チェック")
    # async def birthday_check(self, ctx):
    #     await self.bot.wait_until_ready()
    #     today = datetime.datetime.now().strftime("%m/%d")
    #     bds = load_birthdays()
    #
    #     print("🔍 Botが認識しているチャンネル一覧:")
    #     for guild in self.bot.guilds:
    #         for channel in guild.channels:
    #             print(f"{channel.name} - ID: {channel.id}")

    # @commands.command(name="誕生日剥奪チェック")
    # async def birthday_remove_force(self, ctx):
    #     await self.bot.wait_until_ready()
    #     yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d")
    #     bds = load_birthdays()
    #
    #     for guild in self.bot.guilds:
    #         role = guild.get_role(ROLE_ID)
    #         if not role:
    #             continue
    #
    #         for uid, date in bds.items():
    #             if date == yesterday:
    #                 member = guild.get_member(int(uid))
    #                 if member and role in member.roles:
    #                     await member.remove_roles(role, reason="🎂 誕生日ロール剥奪")
    #
    #     await ctx.send("✅ ロール剥奪処理を実行したよ")

async def setup(bot):
    await bot.add_cog(Birthday(bot))
