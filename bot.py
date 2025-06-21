# bot.py

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class CustomBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.birthday")
        await self.load_extension("cogs.whatday")

bot = CustomBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")

bot.run(os.getenv("DISCORD_TOKEN"))
