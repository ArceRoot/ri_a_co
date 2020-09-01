import discord
from discord.ext import commands
import sqlite3
import ast
import asyncio
import aiohttp
import datetime
import os
from lib import emotes
from pytz import timezone, utc

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Thanks to nitros12
    @commands.command(name="실행")
    @commands.is_owner()
    async def evaluate(self, ctx, *, cmd):
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'sqlite3': sqlite3,
            'asyncio': asyncio,
            'datetime': datetime,
            'aiohttp': aiohttp,
            'os': os
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        if result is not None:
            await ctx.send(f"{emotes.console} {ctx.author.mention} - 구문 실행을 성공적으로 마쳤어요.\n```{result}```")
        else:
            await ctx.send(f"{emotes.console} {ctx.author.mention} - 구문 실행을 성공적으로 마쳤지만, 반환된 값이 없어요.")
    
    @commands.command(name="hellothisisverification")
    async def ver(self, ctx):
        info = await self.bot.application_info()
        owner = info.owner
        await ctx.send(f"{owner} ( {owner.id} )")
    
    @commands.command(name="블랙")
    @commands.is_owner()
    async def add_blacklist(self, ctx, user: discord.User):
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        times = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        reason = ""
        for arg in ctx.message.content.split(" ")[3:]:
            reason += f"{arg} "
        o = sqlite3.connect("lib/riaco.sqlite")
        c = o.cursor()
        c.execute(f"INSERT INTO blacklist(user, admin, reason, datetime) VALUES({user.id}, {ctx.author.id}, '{reason}', '{times}')")
        o.commit()
        o.close()
        await ctx.send(f"{emotes.success} {ctx.author.mention} - 해당 유저를 봇 명령어 사용 차단 목록에 추가했어요. 더 이상 해당 유저는 명령어를 사용하실 수 없어요.")
    
    @commands.command(name="언블랙")
    @commands.is_owner()
    async def remove_blacklist(self, ctx, user: discord.User):
        o = sqlite3.connect("lib/riaco.sqlite")
        c = o.cursor()
        c.execute(f"DELETE FROM blacklist WHERE user = {user.id}")
        o.commit()
        o.close()
        await ctx.send(f"{emotes.success} {ctx.author.mention} - 해당 유저의 봇 사용 차단을 취소했어요.")

def setup(bot):
    bot.add_cog(dev(bot))
