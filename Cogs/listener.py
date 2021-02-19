import discord
from discord.ext import commands
from Tools.func import writedata, getdata, sendEmbed
from random import randint
from Tools.var import embedcolor

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
    async def on_command_completion(self, ctx):
        if ctx.message.author.bot: return
        writedata(id=ctx.message.author.id, item='commandCount', value=str(1 + int(getdata(id=ctx.message.author.id, item='commandCount'))))
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title='서버 참여', color=embedcolor)
        embed.add_field(name='서버 정보', value=f'{guild.name} ({guild.id})')
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.owner.avatar_url, text=f'{guild.owner}')
        await (self.bot.get_channel(808619404240748586)).send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title='서버 퇴장', color=embedcolor)
        embed.add_field(name='서버 정보', value=f'{guild.name} ({guild.id})')
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.owner.avatar_url, text=f'{guild.owner}')
        await (self.bot.get_channel(808619404240748586)).send(embed=embed)

def setup(bot):
    bot.add_cog(Listener(bot))