import discord
from discord.ext import commands
import emotes


modules = [
    "modules.mod",
    "modules.notify",
    "modules.set",
    "modules.eventhandle",
    "modules.dev",
    "modules.support",
    "modules.learning"
]

@bot.event
async def on_ready():
    for m in modules:
        bot.load_extension(m)
    print(bot.user.id)
    print("READY")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("v0.0.1 | Develop"), afk=True)

bot.run("Token")
