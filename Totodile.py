import discord
from discord.ext import commands
from lib import emotes
import sqlite3
import datetime

o = sqlite3.connect("lib/riaco.sqlite")
c = o.cursor()
c.execute("SELECT Token FROM bot_config")
r = c.fetchall()
Token = r[0][0]
o.close()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("리아코 "), description="아 뭐라고 적지")
modules = [
    "modules.verify",
    "modules.mod",
    "modules.set",
    "modules.eventhandle",
    "modules.dev",
    "modules.support",
    "modules.general",
  # "modules.learning",
  # "modules.notify",
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
    activity = discord.Game(r[0][3])
    if r[0][2] == "온라인 / Online":
        status = discord.Status.online
    if r[0][2] == "자리비움 / Idle":
        status = discord.Status.idle
    if r[0][2] == "다른 용무 중 / Do not disturb":
        status = discord.Status.do_not_disturb
    if r[0][2] == "오프라인 / Offline":
        status = discord.Status.invisible
    await bot.change_presence(status=status, activity=activity, afk=True)
    now = datetime.datetime.now()
    c.execute(f"UPDATE bot_config SET started = '{now}'")
    o.commit()
    o.close()

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    if msg.channel.type == discord.ChannelType.private:
        return

    if msg.content.startswith("리아코 ") or msg.content.startswith(f"<@{bot.user.id}> ") or msg.content.startswith(f"<@!{bot.user.id}> "):
        o = sqlite3.connect('lib/riaco.sqlite')
        c = o.cursor()
        c.execute(f"SELECT * FROM blacklist WHERE user = {msg.author.id}")
        rows = c.fetchall()
        if not rows:
            await bot.process_commands(msg)
        elif msg.channel.id == 750332023205265538 and msg.content.split(" ")[1] == "인증":
            await bot.process_commands(msg)
        else:
            admin = bot.get_user(int(rows[0][1]))
            await msg.channel.send(f"{emotes.secure} {msg.author.mention} - 봇 사용이 차단되셔서 취소되었어요. 이의는 Discord 지원 서버에서 제기하실 수 있어요. https://discord.gg/BSByMCw\n사유 : {rows[0][2]}\n처리한 관리자 : {admin}\n차단된 시각 : {rows[0][3]}")

bot.run(Token)
