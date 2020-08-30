import discord
from discord.ext import commands
from lib import emotes
import datetime
import sqlite3

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="핑")
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: {ctx.author.mention} - 퐁! 지연 시간 : `{round(self.bot.latency * 1000)}`ms")

def setup(bot):
    bot.add_cog(general(bot))