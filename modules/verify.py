import discord
from discord.ext import commands
import sqlite3
from lib import emotes
from captcha.image import ImageCaptcha
import asyncio
import random

class auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="인증")
    @commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
    async def authenticate(self, ctx):
        o = sqlite3.connect('lib/riaco.sqlite')
        c = o.cursor()
        c.execute(f"SELECT * FROM guilds WHERE guild = {ctx.guild.id}")
        rows = c.fetchall()
        role = ctx.guild.get_role(rows[0][2])
        if role is not None and role not in ctx.author.roles:
            await ctx.message.delete()
            img = ImageCaptcha()
            code = ""
            for i in range(7):
                rd = random.randint(1, 3)
                a = ""
                if rd == 1:
                    a = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
                #elif rd == 2:
                #    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                else:
                    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                b = random.choice(a)
                code += b
            img.write(code, f"temp/{ctx.author.id}.png")
            m = await ctx.send(f":stopwatch: {ctx.author.mention} - 60초 안에 보안 코드를 입력해주세요.", file=discord.File(f"temp/{ctx.author.id}.png"))

            def check(msg):
                return msg.channel == ctx.channel and msg.author == ctx.author
        
            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                await m.edit(content=f"{emotes.fail} {ctx.author.mention} - 인증 시간이 초과되었어요.")
                await asyncio.sleep(3)
                await m.delete()
            else:
                await msg.delete()
                if msg.content == code:
                    await m.edit(content=f"{emotes.secure} {ctx.author.mention} - 인증이 완료되셨어요. 곧 역할이 자동으로 지급되실 거에요.")
                    await ctx.author.add_roles(role)
                    await asyncio.sleep(3)
                    await m.delete()
                else:
                    await m.edit(content=f"{emotes.profile} {ctx.author.mention} - 코드가 잘못되었어요. `7`을 `1`로 잘못 적지 않도록, 영어 `O`와 숫자 `0`을 헷갈리지 않도록 주의해주세요.\n잠시 후 인증을 다시 시도해주세요.")
                    await asyncio.sleep(3)
                    await m.delete()
        elif role is None:
            await ctx.send(f"{emotes.setting} {ctx.author.mention} - 인증 후 지급될 역할이 지정되지 않았어요. 서버 관리자에게 문의해주세요.")
        else:
            await ctx.send

def setup(bot):
    bot.add_cog(auth(bot))
