import discord
from discord.ext import commands
from lib import emotes
import datetime
import sqlite3

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="핑")
    async def ping(ctx):
        await ctx.send(f"{self.bot.latency * 1000}ms")