import discord
from discord.ext import commands
from Tools.func import can_use, sendEmbed, warn
from EZPaginator import Paginator as page

class Develop(commands.Cog, name='개발'):
    '''
    개발자를 위한 카테고리입니다
    '''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='이모지', aliases=['raw', '이모티콘', 'ㅇㅁㅈ'], help='이모지의 raw 값을 보여줍니다.', usage='[이모지]')
    @can_use()
    async def _emoji(self, ctx, *, emoji: discord.Emoji):
        await sendEmbed(ctx=ctx, title='이모지', content=f'`{emoji}`: {emoji}')

def setup(bot):
    bot.add_cog(Develop(bot))