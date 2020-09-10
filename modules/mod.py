import discord
from discord.ext import commands
from lib import emotes

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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
        await ctx.send(f":athletic_shoe: {ctx.author.mention} - {member}님을 서버에서 추방했어요. 사유 : {reason}")
    
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
        await ctx.guild.kick(member, delete_message_days=delete_days, reason=reason)
        await ctx.send(f":athletic_shoe: {ctx.author.mention} - {member}님을 서버에서 차단했어요.\n메시지 삭제 일 수 : {delete_days}일\n사유 : {reason}")
    
    @commands.command(name="뮤트", aliases=["채금", "채팅금지"])
    async def mute(self, ctx, member: discord.Member):
        reason = ""
        if not ctx.message.content.split(" ")[3:]:
            reason = "사유 없음."
        else:
            reason = "".join(ctx.message.content.split(" ")[3:])
        role = ctx.guild.get_role(int(rows[0][]))

def setup(bot):
    bot.add_cog(Moderation(bot))