import discord
from discord.ext import commands
from Tools.func import writedata, getdata, sendEmbed, warn
from random import randint
import json
from os.path import isdir, isfile
from os import makedirs
import pickle

class Level(commands.Cog, name='레벨링'):
    '''
    레벨링 기능입니다
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
        
    @commands.Cog.listener()
    async def on_command_completion(self, message):
        if message.author.bot: return
        with open('level/guilds.json', 'r') as f:
            data = json.load(f)
        try:
            if data[str(message.guild.id)] == 'off':
                return
        except KeyError:
            pass
        if randint(1, 5) < 4: return
        if not isfile(f'level/{message.guild.id}/{message.author.id}.bin'):
            with open(f'level/{message.guild.id}/{message.author.id}.bin', 'w') as f:
                pickle.dump(0, f)
        with open(f'level/{message.guild.id}/{message.author.id}.bin') as f:
            xp = pickle.load(f)
        level = xp // 50
        xp += randint(1, 4)
        with open(f'level/{message.guild.id}/{message.author.id}.bin', 'w') as f:
            pickle.dump(xp, f)
        if xp // 50 > level:
            await sendEmbed(ctx=await self.bot.get_context(message), title='레벨 업!', content=f'{message.author.mention}님이 {int(level)+1}레벨이 되었습니다!')
    
    @commands.command(name='레벨링', aliases=['레벨', 'level', 'ㄹㅂ'], help='레벨링 기능을 켜거나 끌 수 있습니다.', usage='[ON/OFF]')
    @commands.cooldown(1.0, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def _leveling(self, ctx, mode):
        if mode.lower() not in ['on', 'off']:
            return await warn(ctx=ctx, content='ON 또는 OFF로 설정해 주세요.')
        if not isdir('level'): makedirs('level')
        if isfile('level/guilds.json'):
            with open('level/guilds.json', 'r') as f:
                data = json.load(f)
        else:
            data = {}
        data[str(ctx.guild.id)] = mode.lower()
        with open('level/guilds.json', 'w') as f:
            json.dump(data, f)
        await sendEmbed(ctx=ctx, title='레벨링 모드 설정', content=f'레벨링 모드가 {mode.upper()}로 변경되었습니다.')
    
    @commands.command(name='xp조정', aliases=['managexp', 'xpㅈㅈ', 'xp수정'])
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def _manageXp(self, ctx, member:discord.Member, amount: int):
        if not isdir('level'):
            makedirs('level')
        if isfile('level/guilds.json'):
            with open('level/guilds.json', 'r') as f:
                data = json.load(f)
        else:
            data = {}
        if data[str(ctx.author.id)] == 'off':
            return await warn(ctx=ctx, content='레벨링 관련 기능들이 꺼져 있습니다')
        if not isfile(f'level/{ctx.guild.id}/{member.id}.bin'):
            with open(f'level/{ctx.guild.id}/{member.id}.bin', 'w') as f:
                pickle.dump(0, f)
        with open(f'level/{ctx.guild.id}/{member.id}.bin') as f:
            xp = pickle.load(f)
        if xp + amount < 0:
            return await warn(ctx=ctx, content='XP는 0 이상이어야 합니다.')
        with open(f'level/{ctx.guild.id}/{member.id}.bin', 'w') as f:
            pickle.dump(xp+amount, f)
        await sendEmbed(ctx=ctx, title='xp 조절', content=f'{member.mention}님의 xp가 {xp}만큼 조절되었습니다.')

def setup(bot):
    bot.add_cog(Level(bot))