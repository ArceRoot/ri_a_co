import discord
from discord.ext import commands
from lib import emotes
import sqlite3
import datetime
from pytz import timezone, utc


class support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="문의", aliases=["지원"])
    async def request(self, ctx, *args):
        o = sqlite3.connect("lib/riaco.sqlite")
        c = o.cursor()
        c.execute("SELECT owner FROM bot_config")
        r = c.fetchall()
        own = self.bot.get_user(int(r[0][0]))
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        content = "내용 : "
        for arg in args:
            content += f"{arg} "
        embed = discord.Embed(title="문의가 도착했어요!", color=0x95E1F4)
        embed.add_field(name="문의를 접수한 유저", value=f"{ctx.author} ( {ctx.author.id} )")
        embed.add_field(name="문의가 접수된 서버", value=f"{ctx.guild.name} ( {ctx.guild.id} )")
        embed.add_field(name="문의가 접수된 채널", value=f"{ctx.channel.name} ( {ctx.channel.id} )")
        embed.add_field(name="문의 내용", value=content)
        embed.add_field(name="문의 접수 완료 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))
        embed.set_author(name="문의 및 답변", icon_url=self.bot.user.avatar_url)
        await own.send(own.mention, embed=embed)
        await ctx.send(f"{emotes.success} {ctx.author.mention} - 개발자에게 전송했어요! 허위 문의 및 문의 명령어를 이유 없이 사용하시면 봇 사용이 제한될 수 있어요.")
    
    @commands.command(name="응답")
    async def answer(self, ctx, user: discord.User):
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        content = ""
        for arg in ctx.message.content.split(" ")[2:]:
            content += f"{arg} "
        embed = discord.Embed(title="개발자가 답변을 완료했어요!", color=0x95E1F4)
        embed.add_field(name="답변의 내용", value=content)
        embed.add_field(name="답변이 완료된 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))
        embed.set_author(name="문의 및 답변", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text="원하신다면 리아코 문의 명령어로 계속해서 문의하실 수 있어요!")
        try:
            await user.send(embed=embed)
        except:
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 해당 유저가 DM을 막아놓은 것 같아요. 전송에 실패했어요.")