import discord
from discord.ext import commands
from lib import emotes
import sqlite3
import typing

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_data(self, ctx):
        o = sqlite3.connect("lib/riaco.sqlite")
        c = o.cursor()
        c.execute(f"SELECT * FROM guilds WHERE guild = {ctx.guild.id}")
        rows = c.fetchall()
        return rows

    @commands.command(name="추방", aliases=["킥"])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        reason = ""
        if not ctx.message.content.split(" ")[3:]:
            reason = "사유 없음."
        else:
            reason = "".join(ctx.message.content.split(" ")[3:])
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f":athletic_shoe: {ctx.author.mention} - {member}님을 서버에서 추방했어요.\n사유 : {reason}")
    
    @commands.command(name="차단", aliases=["밴"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User):
        reason = ""
        args = ctx.message.content.split(" ")
        delete_days = 0
        if not args[3:]:
            delete_days = 0
            reason = "사유 없음."
        elif args[3].isdecimal() == True and int(args[3]) <= 7:
            delete_days = int(args[3])
            reason = "".join(args[4:])
        else:
            delete_days = 0
            reason = "".join(args[3:])
        await ctx.guild.kick(user, delete_message_days=delete_days, reason=reason)
        await ctx.send(f":athletic_shoe: {ctx.author.mention} - {user}님을 서버에서 차단했어요.\n메시지 삭제 일 수 : {delete_days}일\n사유 : {reason}")
    
    @commands.command(name="뮤트", aliases=["채금", "채팅금지"])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        reason = ""
        if not ctx.message.content.split(" ")[3:]:
            reason = "사유 없음."
        else:
            reason = "".join(ctx.message.content.split(" ")[3:])
        rows = Moderation.get_data(self, ctx)
        role = ctx.guild.get_role(int(rows[0][3]))
        if role is not None and role not in member.roles:
            await member.add_roles(role, reason=reason)
            await ctx.send(f":mute: {ctx.author.mention} - {member}님의 채팅을 차단했어요.\n사유 : {reason}")
        elif role in member.roles:
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 이미 채팅이 차단된 유저에요.")
        else:
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 뮤트 시 지급하도록 지정된 역할이 없거나, 잘못되었어요.")
    
    @commands.command(name="언뮤트", aliases=["채금해제"])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        reason = ""
        if not ctx.message.content.split(" ")[3:]:
            reason = "사유 없음."
        else:
            reason = "".join(ctx.message.content.split(" ")[3:])
        rows = Moderation.get_data(self, ctx)
        role = ctx.guild.get_role(int(rows[0][3]))
        if role is not None and role in member.roles:
            await member.remove_roles(role, reason=reason)
            await ctx.send(f":loud_sound: {ctx.author.mention} - {member}님의 채팅 차단을 해제했어요.\n사유 : {reason}")
        elif role not in member.roles:
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 채팅 금지 처리된 유저가 아니에요.")
        else:
            await ctx.send(f"{emotes.fail} {ctx.author.mention} - 뮤트 시 지급하도록 지정된 역할이 없거나, 잘못되었어요.")
    
    @commands.command(name="청소", aliases=["삭제", "채팅청소"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, number: typing.Optional[int] = 0):
        await ctx.message.delete()
        if number == 0 or number > 100:
            await ctx.send(f"{emotes.console} {ctx.author.mention} - 삭제에 실패했어요. 삭제하시려면 `1 - 100` 사이의 정수를 입력해주세요.")
        else:
            deleted = await ctx.channel.purge(limit=number)
            await ctx.send(f"{emotes.trash} {ctx.author.mention} - **{len(deleted)}**개의 메시지를 삭제했어요.", delete_after=5)
def setup(bot):
    bot.add_cog(Moderation(bot))