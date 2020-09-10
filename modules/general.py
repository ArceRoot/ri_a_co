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
    
    @commands.command(name="초대")
    async def invite(self, ctx):
        await ctx.send(f"{emotes.profile} {ctx.author.mention} - 아래 링크를 통해 봇을 초대하실 수 있어요.\nhttps://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2147483647&scope=bot")

def setup(bot):
    bot.add_cog(general(bot))