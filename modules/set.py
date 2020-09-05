import discord
from discord.ext import commands
import sqlite3
import asyncio
from lib import emotes

class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="설정")
    async def settings(self, ctx, *args):
        edit_values = ['공지', '로그', '뮤트', '인증', '알림']
        if not args or args[0] not in edit_values:
            await ctx.send(f"{emotes.console} {ctx.author.mention} - 해당 설정 값은 없는 값이에요. 아래 목록에 있는 값만 변경하실 수 있어요.\n```공지, 로그, 뮤트, 인증, 알림```")
        elif args[0] == edit_values[0]:
            anchmsg = await ctx.send(f"{emotes.console} {ctx.author.mention} - 공지 채널 설정을 시작할게요. 잠시만 기다려주세요...")
            o = sqlite3.connect("lib/riaco.sqlite")
            c = o.cursor()
            c.execute(f"SELECT * FROM guilds WHERE guild = {ctx.guild.id}")
            rows = c.fetchall()
            data = rows[0]
            await anchmsg.edit(content=f"{emotes.success} {ctx.author.mention} - 데이터를 불러왔어요! 현재 공지 채널 : <#{data[1]}>\n( 올바르지 않은 채널이라고 뜰 경우 채널이 잘못되었거나, 지정되지 않은 거에요. )")
            msg = await ctx.send(f"{emotes.profile} {ctx.author.mention} - 공지 채널을 변경하시겠어요?\n{emotes.success} : 예\n{emotes.fail} : 아니오")
            await msg.add_reaction(emotes.success)
            await msg.add_reaction(emotes.fail)
            def check(reaction, user):
                return reaction.message.id == msg.id and user == ctx.author
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                await msg.delete()
                await anchmsg.delete()
            else:
                if reaction.emoji == emotes.success:
                    await anchmsg.delete()
                    await msg.edit(content=f":loudspeaker: {ctx.author.mention} - 리아코의 공지를 받아볼 채널을 멘션해주세요.")
                    def msg_check(define):
                        return define.channel == ctx.channel and define.author == ctx.author and define.channel_mentions is not None
                    try:
                        define = await self.bot.wait_for('message', timeout=60, check=msg_check)
                    except asyncio.TimeoutError:
                        await msg.delete()
                    else:
                        await define.delete()
                        channel = define.channel_mentions[0]
                        await msg.edit(content=f"{emotes.success} {ctx.author.mention} - 공지 채널이 {channel.mention} 채널로 설정되었어요. 이제 모든 공지가 해당 채널로 전송될거에요.")
                        c.execute(f"UPDATE guilds SET announce = {channel.id} WHERE guild = {ctx.guild.id}")
                        o.commit()
                        o.close()
                else:
                    await msg.edit(content=f"{emotes.fail} {ctx.author.mention} - 공지 채널 설정 변경이 취소되었어요.")