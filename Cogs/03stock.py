import discord
from discord.ext import commands, tasks
from pickle import load, dump
from random import randint
from datetime import datetime, timedelta
from Tools.func import can_use, sendEmbed, getdata, writedata, warn
from os.path import isfile, isdir
from os import makedirs, listdir

class Stock(commands.Cog, name='주식'):
    '''
    재미있는 주식 기능을 모아 놓은 카테고리입니다
    '''
    
    def __init__(self, bot):
        self.bot = bot
        self.time = datetime.utcnow()
        self.change_price.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not isdir('stocks'): makedirs('stocks')
        if not isdir('stocks/users'): makedirs('stocks/users')
        if not isfile('stocks/stocks.bin'):
            prices = {
                '삼송증권': {
                    'price': 5000,
                    'change': 0},
                '알지전자': {
                    'price': 5000,
                    'change': 0},
                '현내보험': {
                    'price': 5000,
                    'change': 0},
                '동영화학': {
                    'price': 5000,
                    'change': 0},
                '한와금융': {
                    'price': 5000,
                    'change': 0},
                '로데관광': {
                    'price': 5000,
                    'change': 0},
                '동안출판': {
                    'price': 5000,
                    'change': 0},
                '하태식품': {
                    'price': 5000,
                    'change': 0},
                '소울우유': {
                    'price': 5000,
                    'change': 0},
                '남영유업': {
                    'price': 5000,
                    'change': 0},
                '대환통운': {
                    'price': 5000,
                    'change': 0}
            }
            with open('stocks/stocks.bin', 'wb') as f:
                dump(prices, f)
        print('stock-ok')
    
    @tasks.loop(seconds=150)
    async def change_price(self):
        self.time = datetime.utcnow()
        with open('stocks/stocks.bin', 'rb') as f:
            prices = load(f)
        for i in prices:
            if prices[i]['price'] > 1000:
                prices[i]['change'] = randint(-75, 75)
            else:
                prices[i]['change'] = randint(0, 150)
            prices[i]['price'] += prices[i]['change']
        with open('stocks/stocks.bin', 'wb') as f:
            dump(prices, f)
    
    @tasks.loop(hours=24*7)
    async def give_stock_profit(self):
        for i in listdir('stocks/users'):
            user_id = int(i.replace('.bin', ''))
            with open(i, 'rb') as f:
                data = load(f)
            with open('stocks/stocks.bin', 'rb') as f:
                stock_price = load(f)
            for i in data:
                count = 0
                for j in data[i]:
                    count += j['count']
                writedata(id=user_id, item='point', value=str(int(getdata(id=user_id, item='point')) + round(stock_price[i]['price'] * 0.01 * count)))

    def addzero(self, n):
        if len(str(n)) == 1:
            return '0' + str(n)
        return n
    
    @commands.group('주식', aliases=['stock', 'ㅈㅅ'], help='주식 관련 명령어를 실행합니다.', usage='<도표/매수/매도/계좌>', invoke_without_command=True)
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def stocks(self, ctx):
        await sendEmbed(ctx=ctx, title='주식 도움말', content='`ㅍ주식 (도표, 매수, 매도, 계좌)`')
    
    @stocks.command(name='도표', aliases=['chart', 'ㄷㅍ', '차트'], help='주식들의 차트를 보여줍니다')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _chart_stock(self, ctx):
        with open('stocks/stocks.bin', 'rb') as f:
            data = load(f)
        stocks = list()
        for i in data:
            if data[i]['change'] > 0:
                stocks.append(f'+ {data[i]["price"]}(▲ {self.addzero(abs(data[i]["change"]))}) : {i}')
            elif data[i]['change'] < 0:
                stocks.append(f'- {data[i]["price"]}(▼ {self.addzero(abs(data[i]["change"]))}) : {i}')
            else:
                stocks.append(f'= {data[i]["price"]}(■ 00) : {i}')
        stocks = "\n".join(stocks)
        time = (self.time + timedelta(seconds=150) - datetime.utcnow()).seconds
        await sendEmbed(ctx=ctx, title='차트', content=f'```diff\n{stocks}```\n`바뀔때까지 남은 시간: {time}초`')
    
    @stocks.command(name='매수', aliases=['구매', 'ㅁㅅ', 'buy'], help='주식을 삽니다', usage='[회사] [개수]')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _buy_stock(self, ctx, name, count='모두'):
        stock_names = {
            '삼송': '삼송증권',
            '알지': '알지전자',
            '현내': '현내보험',
            '동영': '동영화학',
            '한와': '한와금융',
            '로데': '로데관광',
            '동안': '동안출판',
            '하태': '하태식품',
            '소울': '소울우유',
            '남영': '남영유업',
            '대환': '대환통운'
        }
        if not (name in list(stock_names.keys()) or name in list(stock_names.values())):
            return await warn(ctx=ctx, content='주식을 찾을 수 없습니다.')
        if name in list(stock_names.keys()):
            name = stock_names[name]
        if isfile(f'stocks/users/{ctx.author.id}.bin'):
            with open(f'stocks/users/{ctx.author.id}.bin', 'rb') as f:
                data = load(f)
        else:
            data = {}
        with open('stocks/stocks.bin', 'rb') as f:
            stocks = load(f)
        if count in ['모두', 'ㅇㅇ', '올인', '최대']:
            count = int(getdata(id=ctx.author.id, item='point')) // stocks[name]['price']
            if count == 0:
                return await warn(ctx=ctx, content='돈이 부족합니다')
        else:
            count = int(count)
            if count < 1: return await warn(ctx=ctx, content='살 주식의 개수를 1개 이상으로 입력해 주세요')
        if count * stocks[name]['price'] > int(getdata(id=ctx.author.id, item='point')): return await warn(ctx=ctx, content='돈이 부족합니다')
        if name in data:
            data[name].append({'count': count,
                               'price': stocks[name]['price']})
        else:
            data[name] = [{'count': count,
                           'price': stocks[name]['price']}]
        deliting = []
        for i in data:
            if len(data[i]) == 0: deliting.append(i)
        for i in deliting:
            del data[i]
        with open(f'stocks/users/{ctx.author.id}.bin', 'wb') as f:
            dump(data, f)
        writedata(id=ctx.author.id, item='point', value=str(int(getdata(id=ctx.author.id, item='point')) - count * stocks[name]['price']))
        await sendEmbed(ctx=ctx, title='매수', content=f'{name}의 주식을 `{count}`주 매수했습니다.')
    
    @stocks.command(name='매도', aliases=['ㅁㄷ', '판매', 'sell'], help='주식을 팝니다', usage='[회사] [개수]')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _sell_stock(self, ctx, name, count='모두'):
        stock_names = {
            '삼송': '삼송증권',
            '알지': '알지전자',
            '현내': '현내보험',
            '동영': '동영화학',
            '한와': '한와금융',
            '로데': '로데관광',
            '동안': '동안출판',
            '하태': '하태식품',
            '소울': '소울우유',
            '남영': '남영유업',
            '대환': '대환통운'
        }
        if not (name in list(stock_names.keys()) or name in list(stock_names.values())):
            return await warn(ctx=ctx, content='주식을 찾을 수 없습니다.')
        if name in list(stock_names.keys()):
            name = stock_names[name]
        if isfile(f'stocks/users/{ctx.author.id}.bin'):
            with open(f'stocks/users/{ctx.author.id}.bin', 'rb') as f:
                data = load(f)
        else:
            return await warn(ctx=ctx, content=f'{ctx.author.mention}님은 주식을 갖고 있지 않습니다.')
        if not name in data:
            return await warn(ctx=ctx, content=f'{ctx.author.mention}님은 주식을 갖고 있지 않습니다.')
        with open('stocks/stocks.bin', 'rb') as f:
            stocks = load(f)
        if count in ['모두', 'ㅇㅇ', '올인', '최대']:
            count = 0
            for i in data[name]:
                count += i['count']
        else:
            count = int(count)
            if count < 1: return await warn(ctx=ctx, content='팔 주식의 개수를 1개 이상으로 입력해 주세요')
        user_stocks = 0
        for i in data[name]:
            user_stocks += i['count']
        if user_stocks < count: return await warn(ctx=ctx, content='팔 주식이 부족합니다.')
        addmoney = 0
        counts = 0
        while count != 0:
            if count >= data[name][0]['count']:
                addmoney += data[name][0]['count'] * stocks[name]['price']
                count -= data[name][0]['count']
                counts += data[name][0]['count']
                del data[name][0]
            else:
                data[name][0]['count'] -= count
                counts += count
                addmoney += count * stocks[name]['price']
                count = 0
        deliting = []
        for i in data:
            if len(data[i]) == 0: deliting.append(i)
        for i in deliting:
            del data[i]
        with open(f'stocks/users/{ctx.author.id}.bin', 'wb') as f:
            dump(data, f)
        writedata(id=ctx.author.id, item='point', value=str(int(getdata(id=ctx.author.id, item='point')) + addmoney))
        await sendEmbed(ctx=ctx, title='매도', content=f'{name}의 주식을 `{counts}`주 매도했습니다.')
    
    @stocks.command(name='계좌', aliases=['account', 'ㄱㅈ', '가방'], help='가지고 있는 주식을 보여줍니다.')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _account_stock(self, ctx):
        if not isfile(f'stocks/users/{ctx.author.id}.bin'): return await warn(ctx=ctx, content='가지고 있는 주식이 없습니다')
        with open(f'stocks/users/{ctx.author.id}.bin', 'rb') as f:
            data = load(f)
        if len(data) == 0: return await warn(ctx=ctx, content='가지고 있는 주식이 없습니다')
        with open(f'stocks/stocks.bin', 'rb') as f:
            stocks = load(f)
        user_stocks = {}
        for i in data:
            user_stocks[i] = 0
            for j in data[i]:
                user_stocks[i] += (stocks[i]['price'] - j['price']) * j['count']
        #user_stocks는 각 주식별 차익
        counts = []
        for i in data:
            counts.append(0)
            for j in data[i]:
                counts[-1] += j['count']
        content = []
        for i in enumerate(user_stocks):
            if user_stocks[i[1]] > 0:
                content.append(f'+ {i[1]} {counts[i[0]]}주 : ▲ {abs(user_stocks[i[1]])}')
            elif user_stocks[i[1]] == 0:
                content.append(f'= {i[1]} {counts[i[0]]}주 : ■ 0')
            else:
                content.append(f'- {i[1]} {counts[i[0]]}주 : ▼ {abs(user_stocks[i[1]])}')
        await sendEmbed(ctx=ctx, title='계좌', content='```diff\n' + '\n'.join(content) + '```')

def setup(bot):
    bot.add_cog(Stock(bot))