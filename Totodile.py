import discord
from discord.ext import commands
from lib import emotes
import sqlite3
import datetime


bot = commands.Bot(command_prefix=commands.when_mentioned_or("리아코 "), description="아 뭐라고 적지")
modules = [
#    "modules.mod",
#    "modules.notify",
#    "modules.set",
    "modules.eventhandle",
    "modules.dev",
#    "modules.support",
#    "modules.learning",
    "modules.general"
]

@bot.event
async def on_ready():
    for m in modules:
        bot.load_extension(m)
    print(bot.user)
    print(bot.user.id)
    print("READY")
    o = sqlite3.connect("lib/riaco.sqlite")
    c = o.cursor()
    c.execute("SELECT * FROM bot_config")
    r = c.fetchall()
    status = None
    activity = discord.Game(r[0][1])
    if r[0][0] == "온라인":
        status = discord.Status.online
    if r[0][0] == "자리비움":
        status = discord.Status.idle
    if r[0][0] == "다른 용무 중":
        status = discord.Status.do_not_disturb
    if r[0][0] == "오프라인":
        status = discord.Status.invisible
    await bot.change_presence(status=status, activity=activity, afk=True)
    now = datetime.datetime.now()
    c.execute(f"UPDATE bot_config SET started = '{now}'")
    o.commit()
    o.close()

bot.run("Token")
