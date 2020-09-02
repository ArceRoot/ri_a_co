import discord
from discord.ext import commands
from lib import emotes
import aiohttp
import sqlite3
import string
import random


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 이 명령어는 봇 관리자만 사용할 수 있어요.")
        elif isinstance(error, commands.MissingPermissions):
            a = ""
            for p in error.perms:
                if p != error.perms[len(error.perms) - 1]:
                    a += f"{p}, "
                else:
                    a += f"{p}"
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 이 명령어를 실행하실 권한이 없어요. 이 명령어는 아래 권한을 필요로 해요.\n```{a}```")
        elif isinstance(error, commands.BotMissingPermissions):
            a = ""
            for p in error.perms:
                if p != error.perms[len(error.perms) - 1]:
                    a += f"{p}, "
                else:
                    a += f"{p}"
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 봇이 명령어를 처리할 수 없었어요. 아래 권한이 봇에게 주어졌는지 확인해주세요.\n```{a}```")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":hourglass_flowing_sand: {ctx.author.mention} - 명령어가 쿨다운 중에 있어요. 앞으로 {round(error.retry_after)}초 후에 다시 시도하실 수 있어요.")
        else:
            code = ""
            for i in range(6):
                b = random.choice(string.ascii_letters)
                code += b
            async with aiohttp.ClientSession() as session:
                o = sqlite3.connect("lib/riaco.sqlite")
                c = o.cursor()
                c.execute("SELECT * FROM bot_config")
                r = c.fetchall()
                w = discord.Webhook.from_url(r[0][5], adapter=discord.AsyncWebhookAdapter(session))
                await w.send(f':no_entry_sign: - 봇 실행 중 오류 발생! `{code}`\n```{error}```', username='리아코_')
            await ctx.send(f"{emotes.secure} {ctx.author.mention} - 명령어 실행 중 알 수 없는 오류가 발생했어요. `리아코 문의` 명령어로 `{code}` 코드를 전달해주세요.")
        
def setup(bot):
    bot.add_cog(events(bot))
