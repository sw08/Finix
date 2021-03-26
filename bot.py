import discord
from discord.ext import commands, tasks
from pickle import load
from Tools.var import prefix, embedcolor, mainprefix, version
from Tools.func import warn, errorlog
from datetime import datetime
from os import listdir, chdir
import asyncio
from asyncio import sleep
import koreanbots
import logging
import sys
from datetime import datetime

with open('token.bin', 'rb') as f:
    token = load(f)

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command('help')

with open('koreanbotsToken.bin', 'rb') as f:
    koreanbotsToken = load(f)

Bots = koreanbots.Client(bot, koreanbotsToken)

if 'Finix' in listdir():
    chdir('Finix')

async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        messages = [f'{len(bot.guilds)}서버 {len(bot.users)}유저', f'{mainprefix}도움', f'피닉스 {version}', 'DM으로 문의하세요']
        for i in messages:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(i))
            await sleep(10)

@bot.event
async def on_ready():
    global logger
    bot.owner_ids = [745848200195473490, 441202161481809922]
    cogs = listdir("Cogs")
    cogs.sort()
    for filename in cogs:
        if filename.endswith(".py"):    
            bot.load_extension(f"Cogs.{filename[:-3]}")
            print(f"Cogs.{filename[:-3]}")
    logger = logging.getLogger('Finix_Log')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    print('구동 시작')
    await bot.change_presence(status=discord.Status.online, activity=(await presence()))

@bot.command(name="로드", aliases=['모듈로드', 'load', 'ㄹㄷ'])
@commands.is_owner()
async def load_commands(ctx, *, extension):
    bot.load_extension(f"Cogs.{extension}")
    await ctx.send(embed=discord.Embed(title='Load', description=f'Successfully Loaded {extension}', color=embedcolor))

@bot.command(name="언로드", aliases=['모듈언로드', 'unload', 'ㅇㄹㄷ'])
@commands.is_owner()
async def unload_commands(ctx, *, extension):
    bot.unload_extension(f"Cogs.{extension}")
    await ctx.send(embed=discord.Embed(title='Unload', description=f'Successfully Unloaded {extension}', color=embedcolor))

@bot.command(name='리로드', aliases=['모듈리로드', 'reload', 'ㄹㄹㄷ'])
@commands.is_owner()
async def reload_commands(ctx, *, extension='all'):
    if extension == 'all':
        embed = discord.Embed(title='Reloading All Category', color=embedcolor)
        msg = await ctx.send(embed=embed)
        cogs = listdir("Cogs")
        cogs.sort()
        for i in cogs:
            if i.endswith('.py'):
                try: bot.unload_extension(f'Cogs.{i[:-3]}')
                except: pass
                embed.add_field(name='Unloading', value=f'Unloading {i[:-3]}')
                await msg.edit(embed=embed)
                embed.remove_field(index=0)
                try: bot.load_extension(f'Cogs.{i[:-3]}')
                except: pass
                embed.add_field(name='Loading', value=f'Loading {i[:-3]}')
                await msg.edit(embed=embed)
                embed.remove_field(index=0)
        await msg.edit(embed=discord.Embed(title='Finished', descriptions='Reloading All Modules Finished', color=embedcolor))
    else:
        embed = discord.Embed(title=f'Reloading {extension} Category', color=embedcolor)
        msg = await ctx.send(embed=embed)
        bot.unload_extension(f'Cogs.{extension}')
        embed.add_field(name='Unloading', value=f'Unloading {extension}')
        await msg.edit(embed=embed)
        embed.remove_field(index=0)
        bot.load_extension(f'Cogs.{extension}')
        embed.add_field(name='Loading', value=f'Loading {extension}')
        await msg.edit(embed=embed)
        embed.remove_field(index=0)
        await msg.edit(embed=discord.Embed(title='Finished', description=f'Reloading {extension} Finished', color=embedcolor))

@bot.event
async def on_command(ctx):
    logger.info(f'{ctx.author} ({ctx.author.id})가 {ctx.message.content} 실행\n{ctx.message.created_at}')

@bot.event
async def on_error(event, *args, **kwargs):
    exc = sys.exc_info()
    logger.error(f'{event}에서 에러 발생: {exc}\n{datetime.now()}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
        await warn(ctx=ctx, content=f"지금 쿨타임에 있어요. `{round(error.retry_after, 2)}`초 후에 다시 시도해 주세요")
    elif isinstance(error, commands.CheckFailure):
        await warn(ctx=ctx, content='실행하실 조건이 충족되지 않았습니다')
    elif isinstance(error, commands.BadArgument):
        await warn(ctx=ctx, content='올바른 값을 넣어 주세요')
    elif isinstance(error, commands.MissingRequiredArgument):
        await warn(ctx=ctx, content='값이 필요합니다')
    elif isinstance(error, commands.MissingPermissions):
        await warn(ctx=ctx, content='권한이 없습니다')
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.DisabledCommand):
        await warn(ctx=ctx, content='현재 이 명령어는 사용이 불가능합니다')
    elif isinstance(error, commands.MaxConcurrencyReached):
        await warn(ctx=ctx, content='너무 많은 명령어가 실행 중이에요')
    elif '403 Forbidden' in str(error):
        await warn(ctx=ctx, content='저런. 봇에게 권한을 제대로 주지 않으셨군요')
    else:
        await errorlog(ctx=ctx, error=error, bot=bot)
    logger.error('에러: {ctx.author.id} ({ctx.author})\n\n{error}\n\n{datetime.now()}')

bot.run(token)