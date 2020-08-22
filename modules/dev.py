import discord
from discord.ext import commands
import sqlite3
import ast
import asyncio
import aiohttp
import datetime
import os
import emotes


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class dev(commands.Cog):
    def __init__(self, bot)
        self.bot = bot
        
    @commands.command()
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
    
def setup(bot):
    bot.add_cog(dev(bot))
