import discord
from discord.ext import commands
from Tools.func import writedata, getdata, sendEmbed
from random import randint

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        level = getdata(id=message.author.id, item='level')
        writedata(id=message.author.id, item='xp', value=str(randint(1, 5) + int(getdata(id=message.author.id, item='xp'))))
        if int(level) < (int(getdata(id=message.author.id, item='xp')) // 50):
            await sendEmbed(ctx=(await self.bot.get_context(message)), title='레벨 업!', content=f'{message.author.mention}님이 {int(level)+1}레벨이 되었습니다!')
            writedata(id=message.author.id, item='level', value=str(int(level)+1))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.message.author.bot: return
        writedata(id=ctx.message.author.id, item='commandCount', value=str(1 + int(getdata(id=ctx.message.author.id, item='commandCount'))))

def setup(bot):
    bot.add_cog(Listener(bot))