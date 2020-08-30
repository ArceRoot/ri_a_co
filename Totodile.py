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
#    "modules.mod",
#    "modules.notify",
#    "modules.set",
    "modules.eventhandle",
    "modules.dev",
    "modules.support",
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
    activity = discord.Game(r[0][3])
    if r[0][2] == "온라인":
        status = discord.Status.online
    if r[0][2] == "자리비움":
        status = discord.Status.idle
    if r[0][2] == "다른 용무 중":
        status = discord.Status.do_not_disturb
    if r[0][2] == "오프라인":
        status = discord.Status.invisible
    await bot.change_presence(status=status, activity=activity, afk=True)
    now = datetime.datetime.now()
    c.execute(f"UPDATE bot_config SET started = '{now}'")
    o.commit()
    o.close()

@bot.event
async def on_message(msg):
    o = sqlite3.connect('lib/riaco.sqlite')
    c = o.cursor()
    c.execute(f"SELECT * FROM blacklist WHERE user = {msg.author.id}")
    rows = c.fetchall()
    if not rows:
        await bot.process_commands(msg)
    elif msg.content.startswith("리아코 문의"):
        await bot.process_commands(msg)
    else:
        admin = bot.get_user(int(rows[0][1]))
        await msg.channel.send(f"{emotes.secure} {msg.author.mention} - 봇 사용이 차단되셔서 취소되었어요. 이의는 `리아코 문의` 명령어를 사용하셔서 전송해주세요.\n사유 : {rows[0][2]}\n처리한 관리자 : {admin}\n차단된 시각 : {rows[0][3]}")

bot.run(Token)
