from asyncio import sleep
import discord
from discord.ext import commands, tasks
from Tools.func import writedata, getdata, sendEmbed
from random import randint
from Tools.var import embedcolor, version, mainprefix
from os.path import isdir, isfile
import os.path
from os import makedirs, remove
from threading import Thread
import json, datetime, zipfile

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._backup.start()
    
    @tasks.loop(hours=24)
    async def _backup(self):
        if isfile('backup.zip'): remove('backup.zip')
        backup_zip = zipfile.ZipFile('backup.zip', 'w')
        for i in ['data/', 'stocks/', 'rank/', 'posts/', 'level/']:
            for folder, _subfolders, files in os.walk(i):
                for file in files:
                    backup_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file)), compress_type = zipfile.ZIP_DEFLATED)
        if isfile('banned.bin'): backup_zip.write('banned.bin', compress_type=zipfile.ZIP_DEFLATED)
        backup_zip.close()
        await (self.bot.get_channel(821358881837416468)).send(file=discord.File('backup.zip'), content=datetime.datetime.now())
        os.remove('backup.zip')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.author.bot: return
        writedata(id=ctx.author.id, item='commandCount', value=str(1 + int(getdata(id=ctx.author.id, item='commandCount'))))
    
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
        if message.mentions == [self.bot.user.mention] and len(message.content) == 21: return await sendEmbed(ctx=await self.bot.get_context(message), title='피닉스 접두사', content='피닉스의 접두사는 `ㅍ`, `\'\'`, `"`입니다')
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