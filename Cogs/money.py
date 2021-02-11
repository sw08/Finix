import discord
from discord.ext import commands
import json
from Tools.func import can_use, sendEmbed, getdata, writedata, getnow, warn
from random import randint

class Money(commands.Cog, name='경제'):
    '''
    포인트 관련 경제 카테고리입니다.
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='포인트', aliases=['point', '돈', 'ㄷ'], help='자신이 가지고 있는 돈을 보여줍니다.', usage='<유저 닉네임 또는 멘션>')
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    @can_use()
    async def _point(self, ctx, user: discord.User=None):
        if user is None: user = ctx.author
        point = int(getdata(id=user.id, item='point'))
        await sendEmbed(ctx=ctx, title='돈', content=f'`{user}`님의 돈: `{point}`원')
    
    @commands.command(name='출석', aliases=['ㅊ', '체크', 'check'], help='출석을 해 돈을 받습니다.')
    @commands.cooldown(1.0, 15, commands.BucketType.user)
    @can_use()
    async def _check(self, ctx):
        date = getnow('%Y%m%d')
        if getdata(id=ctx.author.id, item='lastCheck') == date:
            await warn(ctx=ctx, content='오늘은 이미 출석했습니다. 내일 출석해 주십시오.')
            return
        point = str(int(getdata(id=ctx.author.id, item='point')) + 50 * randint(2, 4))
        writedata(id=ctx.author.id, item='point', value=point)
        writedata(id=ctx.author.id, item='lastCheck', value=date)
        await sendEmbed(ctx=ctx, title='출석', content=f'출석 완료되었습니다.\n현재 포인트: `{point}`')

def setup(bot):
    bot.add_cog(Money(bot))