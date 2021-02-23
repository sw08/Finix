import discord
from discord.ext import commands
from Tools.func import can_use, sendEmbed, warn
from math import sqrt

class Math(commands.Cog, name='수학'):
    '''
    수학 기능들을 모아놓은 카테고리입니다.
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='근의공식', aliases=['이차방정식', 'quadEquation', 'ㅇㅊ'], help='이차방정식을 풀어줍니다, ax₂ + bx + c = 0', usage='[a] [b] [c]')
    @commands.cooldown(1.0, 7, commands.BucketType.user)
    @can_use()
    async def _quadEquation(self, ctx, a:float, b:float, c:float):
        if b*b < 4*a*c:
            await sendEmbed(ctx=ctx, title='결과', content='해가 없습니다.')
            return
        result = [str(((-1*b) + sqrt(b*b-4*a*c)) / 2*a), str(((-1*b) - sqrt(b*b-4*a*c)) / 2*a)]
        if result[0] == result[1]:
            del result[1]
        await sendEmbed(ctx=ctx, title='결과', content=f'해: `{"`, `".join(result)}`')
    
    @commands.command(name='피보나치', aliases=['FibonacciNumber', '피보나치수열', 'ㅍㅂㄴㅊ'], help='피보나치 수열을 구합니다.', usage='[수열의 개수]')
    @commands.cooldown(1.0, 10, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=True) 
    @can_use()
    async def _fibonacci(self, ctx, amount: int):
        if amount < 1: return await warn(ctx=ctx, content='1 이상의 정수를 입력해 두세요')
        numbers = [0, 1]
        for _ in range(amount-2):
            numbers.append(numbers[-2] + numbers[-1])
        for i in range(len(numbers)):
            numbers[i] = str(numbers[i])
        if amount == 1:
            del numbers[1]
        await sendEmbed(ctx=ctx, title='결과', content=f'`{"`, `".join(numbers)}`')
    
    @commands.command(name='사칙연산', aliases=['산수', 'ㅅㅊㅇㅅ', 'calculate'], help='간단한 사칙연산을 해 줍니다. 곱하기는 *, 나누기는 /로 처리합니다', usage='[수] [연산자] [수]')
    @can_use()
    async def _calculate(self, ctx, n1:int, operator:float, n2:float):
        if not str in ['*', '/', '+', '-']: return await warn(ctx=ctx, content='연산자를 제대로 입력해 주세요')
        result = eval(f'{n1}{operator}{n2}')
        await sendEmbed(ctx=ctx, title='결과', content=f'{n1} {operator} {n2} = {result}')
    
    @commands.command(name='파이', aliases=['pi', 'ㅍㅇ', '원주율'], help='지금까지 피닉스가 구한 원주율을 보여줍니다')
    @can_use()
    async def _pi(self, ctx):
        with open('pi.json') as f:
            data = json.load(f)
        await sendEmbed(ctx=ctx, title='지금까지 피닉스가 구한 원주율', content=f'`{int(data["quater_pi"])*4}`s')

def setup(bot):
    bot.add_cog(Math(bot))