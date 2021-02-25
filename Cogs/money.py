import discord
from discord.ext import commands
import json
from Tools.func import can_use, sendEmbed, getdata, writedata, getnow, warn
from Tools.var import embedcolor, mainprefix
from random import randint
import pickle
from datetime import datetime
from os.path import isfile, isdir
from os import makedirs

class Money(commands.Cog, name='경제'):
    '''
    포인트 관련 경제 카테고리입니다.
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='정보', aliases=['info', '프로필', 'ㅍㄹㅍ'], usage='<유저>', help='유저의 정보를 보여줍니다')
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    @can_use()
    async def _info(self, ctx, user: discord.Member=None):
        if user is None: user = ctx.author
        point = getdata(id=user.id, item='point')
        checks = getdata(id=user.id, item='countCheck')
        try: percentCheck = int(getdata(id=user.id, item='winningRandom')) / int(getdata(id=user.id, item='countRandom')) * 100
        except: percentCheck = 0
        embed = discord.Embed(title=f'{user}', description=getdata(id=user.id, item='introduce'), color=embedcolor)
        embed.set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='유저 id', value=f'{user.id}')
        statuses = ['<:online:809612933633146881>', '<:DND:809612933561843712>', '<:idle:809612931775594526>', '<:offline:809612930932670505>']
        a2 = ['online', 'dnd', 'idle', 'offline']
        a = ['온라인', '방해 금지', '자리 비움', '오프라인']
        status = statuses[a2.index(str(user.status))] + ' ' + a[a2.index(str(user.status))] 
        embed.add_field(name='유저 상태', value=f'{(["데스크톱", "모바일"])[int(user.is_on_mobile())]}, {status}')
        embed.add_field(name='봇 여부', value=f'{([ "👤", "🤖"])[int(user.bot)]} 계정')
        embed.add_field(name='계정 생성일', value=f'{(user.created_at).strftime("%Y년 %m월 %d일")}', inline=False)
            embed.add_field(name='명령어 사용 횟수', value=f'`{getdata(id=user.id, item="commandCount")}`회')
            embed.add_field(name='포인트', value=f'💵 `{point}`포인트')
            embed.add_field(name='승률', value=f'`{round(percentCheck)}`%')
            embed.add_field(name='출석 횟수', value=f'`{checks}`회')
        else:
            embed.add_field(name='인증 여부', value=f'{(["<:bot:812119117711933461>", "<:verified_bot:812119144731902013>"])[int(user.public_flags.verified_bot)]}')
        await ctx.send(embed=embed)
    
    @commands.command(name='포인트', aliases=['point', '돈', 'ㄷ'], help='자신이 가지고 있는 돈을 보여줍니다.', usage='<유저 닉네임 또는 멘션>')
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    @can_use()
    async def _point(self, ctx, user: discord.User=None):
        if user is None or user.bot: user = ctx.author
        point = int(getdata(id=user.id, item='point'))
        await sendEmbed(ctx=ctx, title='💵 돈 💵', content=f'`{user}`님의 돈: `{point}`원')
    
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
        writedata(id=ctx.author.id, item='coundCheck', value=str(1+int(getdata(id=ctx.author.id, item='countCheck'))))
        writedata(id=ctx.author.id, item='lastCheck', value=date)
        await sendEmbed(ctx=ctx, title='출석', content=f'출석 완료되었습니다.\n현재 포인트: `{point}`')
        writingDate = getnow('**%H:%M:%S.%f**')
        if not isdir('rank'):
            makedirs('rank')
        if not isfile('rank/check.json'):
            with open('rank/check.json', 'w') as f:
                json.dump({
                    'date': date,
                    '1': {'id': 'none',
                          'time': 'none'},
                    '2': {'id': 'none',
                          'time': 'none'},  
                    '3': {'id': 'none',
                          'time': 'none'},
                    '4': {'id': 'none',
                          'time': 'none'},
                    '5': {'id': 'none',
                          'time': 'none'},
                    'len': '0'
                }, f)
        with open('rank/check.json', 'r') as f:
            data = json.load(f)
        if data['len'] == '5': return
        if data['date'] != date: data['len'] = '0'
        data[str(int(data['len'])+1)]['id'] = str(ctx.author.id)
        data[str(int(data['len'])+1)]['time'] = writingDate
        data['len'] = str(int(data['len']) + 1)
        data['date'] = date
        with open('rank/check.json', 'w') as f:
            json.dump(data, f)
        content = []
        for i in range(int(data['len'])):
            content.append('**' + str(i+1) + '**. `' + str(await self.bot.fetch_user(int(data[str(i+1)]['id']))) + '` : ' + data[str(i+1)]['time'])
        await sendEmbed(ctx=ctx, title='출석 랭킹', content='\n'.join(content))

    @commands.command(name='도박', aliases=['베팅', 'betting', 'ㄷㅂ'], help='포인트를 걸고 도박을 합니다.', usage='[걸 포인트]')
    @can_use()
    @commands.cooldown(1.0, 4, commands.BucketType.user)
    async def _betting(self, ctx, amount):
        point = int(getdata(id=ctx.author.id, item='point'))
        if amount in ['올인', '모두']:
            amount = point
        try:
            amount = int(amount)
        except ValueError:
            await warn(ctx=ctx, content='걸 돈을 제대로 넣어 주세요.')
            return
        if int(point) < amount:
            return await warn(ctx=ctx, content='돈이 부족합니다.')
        result = randint(-1, 1)
        writedata(id=ctx.author.id, item='countRandom', value=str(int(getdata(id=ctx.author.id, item='countRandom'))+1))
        if result == 1:
            writedata(id=ctx.author.id, item='point', value=str(point+amount))
            await sendEmbed(ctx=ctx, title='와아아', content=f'이겼습니다!\n현재 포인트: `{point+amount}`')
            writedata(id=ctx.author.id, item='winningRandom', value=str(int(getdata(id=ctx.author.id, item='winningRandom'))+1))
        elif result == 0:
            await sendEmbed(ctx=ctx, title='휴...', content='이기진 못했지만 다행히 잃지는 않았어요!')
        else:
            writedata(id=ctx.author.id, item='point', value=str(point-amount))
            await sendEmbed(ctx=ctx, title='이런!', content=f'아쉽게도 져서 💵 {amount}만큼 잃었어요...\n현재 포인트: `{point-amount}`')
    
    @commands.command(name='송금', aliases=['돈보내기', 'sendMoney', 'ㅅㄱ'], help='원하는 사람에게 돈을 보냅니다.', usage='[유저] [돈]')
    @can_use()
    @commands.cooldown(1.0, 7, commands.BucketType.user)
    async def _sendmoney(self, ctx, user:discord.User, amount:int):
        if amount < 50:
            await warn(ctx=ctx, content='50뭔 이상부터 송금할 수 있습니다')
            return
        if user.bot:
            return await warn(ctx=ctx, content='봇에게는 송금할 수 없습니다')
        writedata(id=ctx.author.id, item='point', value=str(int(getdata(id=ctx.author.id, item='point'))-amount))
        writedata(id=user.id, item='point', value=str(int(getdata(id=user.id, item='point'))+round(amount*0.95)))
        await sendEmbed(ctx=ctx, title='💵 송금 💵', content=f'`{user}`님께 💵 `{round(amount*0.95)}`만큼 송금되었습니다.\n수수료: 💵 `{amount-round(amount*0.95)}`')
    
    @commands.command(name='랭킹', aliases=['순위표', 'ㄹㅋ', 'rank'], help='랭킹을 보여줍니다', usage="<종류>")
    @commands.cooldown(1.0, 10, commands.BucketType.user)
    @can_use()
    async def _ranking(self, ctx, category=None):
        if category not in ['출석순위', None]: return
        await ctx.trigger_typing()
        if not isdir('rank'):
            makedirs('rank')
        if not isfile('rank/check.json'):
            date = getnow('%Y%m%d')
            with open('rank/check.json', 'w') as f:
                json.dump({
                    'date': date,
                    '1': {'id': 'none',
                          'time': 'none'},
                    '2': {'id': 'none',
                          'time': 'none'},  
                    '3': {'id': 'none',
                          'time': 'none'},
                    '4': {'id': 'none',
                          'time': 'none'},
                    '5': {'id': 'none',
                          'time': 'none'},
                    'len': '0'
                }, f)
        if category == '출석순위':
            content = []
            with open('rank/check.json', 'r') as f:
                data = json.load(f)
            for i in range(5):
                if data[str(i+1)]['id'] == 'none': break
                content.append('**' + str(i+1) + '**. ' + str(await self.bot.fetch_user(int(data[str(i+1)]['id']))))
            content = '\n'.join(content)
            return await sendEmbed(ctx=ctx, title='출석 순위 랭킹', content=content)

def setup(bot):
    bot.add_cog(Money(bot))