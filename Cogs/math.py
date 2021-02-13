import discord
from discord.ext import commands
from Tools.func import can_use, sendEmbed
from math import sqrt

class Math(commands.Cog, name='수학'):
    '''
    수학 기능들을 모아놓은 카테고리입니다.
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='근의공식', aliases=['이차방정식', 'quadEquation', 'ㅇㅊ'], help='이차방정식을 풀어줍니다, ax₂ + bx + c = 0', usage='[a] [b] [c]')
    @commands.cooldown(1.0, 7, commands.BucketType.user)
    @can_use()
    async def _quadEquation(self, ctx, a:float, b:float, c:float):
        if b*b < 4*a*c:
            await sendEmbed(ctx=ctx, title='결과', content='해가 없습니다.')
            return
        result = [str(((-1*b) + sqrt(b*b-4*a*c)) / 2*a), str(((-1*b) - sqrt(b*b-4*a*c)) / 2*a)]
        if result[0] == result[1]:
            del result[1]
        await sendEmbed(ctx=ctx, title='결과', content=f'해: `{"`, `".join(result)}`')

def setup(bot):
    bot.add_cog(Math(bot))