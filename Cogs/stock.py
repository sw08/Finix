import discord
from discord.ext import commands, tasks
from pickle import load, dump
from random import randint
from datetime import datetime, timedelta
from Tools.func import can_use, sendEmbed, getdata, writedata, warn
from os.path import isfile, isdir
from os import makedirs

class Stock(commands.Cog, name='주식'):
    '''
    재미있는 주식 기능을 모아 놓은 카테고리입니다
    '''
    
    def __init__(self, bot):
        self.bot = bot
        self.time = datetime.utcnow()
    
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
                '시민은행': {
                    'price': 5000,
                    'change': 0},
                '엑스케이': {
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
                    'change': 0},
                '자일운수': {
                    'price': 5000,
                    'change': 0},
                '엑스오일': {
                    'price': 5000,
                    'change': 0},
                '한직택배': {
                    'price': 5000,
                    'change': 0}
            }
            with open('stocks/stocks.bin', 'wb') as f:
                dump(prices, f)
            
        @tasks.loop(seconds=150)
        async def _change_price(self):
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
    
    @commands.command(name='도표', aliases=['chart', 'ㄷㅍ', '차트'], help='주식들의 차트를 보여줍니다')
    @can_use()
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    async def _chart(self, ctx):
        with open('stocks/stocks.bin', 'rb') as f:
            data = load(f)
        stocks = list()
        for i in data:
            if data[i]['change'] > 0:
                stocks.append(f'+ {data[i]["price"]}(▲ {abs(data[i]["change"])}) : {i}')
            elif data[i]['change'] < 0:
                stocks.append(f'- {data[i]["price"]}(▼ {abs(data[i]["change"])}) : {i}')
            else:
                stocks.append(f'= {data[i]["price"]}(■ 0) : {i}')
        stocks = "\n".join(stocks)
        time = (self.time + timedelta(seconds=150) - datetime.utcnow()).seconds
        await sendEmbed(ctx=ctx, title='차트', content=f'```diff\n{stocks}```\n\n`바뀔때까지 남은 시간: {time}초`')
    
    @commands.command(name='매수', aliases=['구매', 'ㅁㅅ', 'buy'], help='주식을 삽니다', usage='[주식 이름] [개수]')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _buy_stock(self, ctx, name, count:int=None):
        stock_names = {
            '삼송': '삼송증권',
            '알지': '알지전자',
            '현내': '현내보험',
            '시민': '시민은행',
            '엑스': '엑스케이',
            '동영': '동영화학',
            '한와': '한와금융',
            '로데': '로데관광',
            '동안': '동안출판',
            '하태': '하태식품',
            '소울': '소울우유',
            '남영': '남영유업',
            '대환': '대환통운',
            '자일': '자일운수',
            '엑스': '엑스오일',
            '한직': '한직택배'
        }
        if not (name in list(stock_names.keys()) or name in list(stock_names.values())):
            await warn(ctx=ctx, content='')       
        if count is None:
            count = int(getdata(id=ctx.author.id, item='point')) 
            if isfile(f'stocks/users/{ctx.author.id}.bin'):
                with open(f'stocks/users/{ctx.author.id}.bin', 'rb') as f:
                    data = load(f)
            else:
                data = {}
        

def setup(bot):
    bot.add_cog(Stock(bot))