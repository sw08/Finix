from asyncio import sleep
import discord
from discord.ext import commands
from Tools.func import writedata, getdata, sendEmbed
from random import randint
from Tools.var import embedcolor, version, mainprefix

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
    
    async def presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            messages = [f'{len(self.bot.guilds)}개의 서버에서 활동', f'{len(self.bot.users)}명의 유저들과 활동', f'{mainprefix}도움', f'피닉스 {version}', 'DM으로 문의하세요']
            for i in messages:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(i))
                await sleep(3)
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=(await self.presence()))
    
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