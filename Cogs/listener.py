import discord
from discord.ext import commands
from Tools.func import writedata, getdata, sendEmbed
from random import randint
from Tools.var import embedcolor
from os.path import isdir, isfile
from os import makedirs
from threading import Thread
import json, datetime

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.author.bot: return
        writedata(id=ctx.author.id, item='commandCount', value=str(1 + int(getdata(id=ctx.author.id, item='commandCount'))))
    
    def getpi(self):
        if isfile('pi.json'):
            with open('pi.json', 'r') as f:
                data = json.load(f)
                n = int(data['n'])
                quater_pi = float(data['quater_pi'])
        else:
            with open('pi.json', 'w') as f:
                json.dump({'n': '1',
                           'quater_pi': '0'}, f)
            quater_pi = 0
            n = 1
        while True:
            for _ in range(10000000):
                quater_pi += 1/n
                n += 2
                quater_pi -= 1/n
                n += 2
            with open('pi.json', 'w') as f:
                json.dump({'quater_pi': str(quater_pi),
                           'n': str(n)}, f)
 
    @commands.Cog.listener()
    async def on_ready(self):
        thread = Thread(target=self.getpi)
        thread.setDaemon(True)
        thread.start()
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title='서버 참여', color=embedcolor)
        embed.add_field(name='서버 정보', value=f'{guild.name} ({guild.id})')
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.owner.avatar_url, text=f'{guild.owner}')
        await (self.bot.get_channel(808619404240748586)).send(embed=embed)
        if not isdir('level'): makedirs('level')
        if isfile('level/guilds.json'):
            with open('level/guilds.json', 'r') as f:
                data = json.load(f)
        else:
            data = {}
        data[str(guild.id)] = 'on'
        with open('level/guilds.json', 'w') as f:
            json.dump(data, f)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title='서버 퇴장', color=embedcolor)
        embed.add_field(name='서버 정보', value=f'{guild.name} ({guild.id})')
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.owner.avatar_url, text=f'{guild.owner}')
        await (self.bot.get_channel(808619404240748586)).send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or type(message.channel) != discord.DMChannel: return
        category = self.bot.get_channel(812625850565525525)
        channels = [i.name for i in category.channels]
        await message.add_reaction('<a:CheckGIF2:808647121061675049>')
        if str(message.author.id) in channels:
            userChannel = category.channels[channels.index(str(message.author.id))]
        else:
            userChannel = await category.create_text_channel(name=str(message.author.id))
        await userChannel.edit(topic=str(message.author))
        await userChannel.send(f'{message.author.mention}: ```{message.content}```')

def setup(bot):
    bot.add_cog(Listener(bot))