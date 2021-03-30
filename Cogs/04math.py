import discord
from discord.ext import commands
from Tools.func import can_use, sendEmbed, warn
from Tools.var import mainprefix
from math import sqrt
import json

class Math(commands.Cog, name='수학'):
    '''
    수학 기능들을 모아놓은 카테고리입니다.
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='이차방정식', aliases=['2차방정식', 'quadraticEquation', '2ㅊㅂㅈㅅ'], help='이차방정식을 풀어줍니다, ax₂ + bx + c = 0', usage='[a] [b] [c]')
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
    async def _calculate(self, ctx, n1:float, operator:str, n2:float):
        if not operator in ['*', '/', '+', '-']: return await warn(ctx=ctx, content='연산자를 제대로 입력해 주세요')
        try:
            result = eval(f'{n1}{operator}{n2}')
        except ZeroDivisionError:
            return await warn(ctx=ctx, content='0으로는 나눌 수 없습니다.')
        await sendEmbed(ctx=ctx, title='결과', content=f'{n1} {operator} {n2} = {result}')
    
    @commands.command(name='일차방정식', aliases=['1차방정식', '1ㅊㅂㅈㅅ', 'linearEquation'], help='일차방정식을 풀어줍니다. ax + b = 0', usage='[a] [b]')
    @commands.cooldown(1.0, 7, commands.BucketType.user)
    @can_use()
    async def _linearEquation(self, ctx, n1:float, n2:float):
        await sendEmbed(ctx=ctx, title='결과', content=f'해: {-1 * n2 / n1}')
    
    @commands.command(name='조립제법', aliases=['ㅈㄹㅈㅂ', 'assemblyMethod', '조립 제법'], help='조립제법을 실행합니다. 계수들은 |로 구분해 넣어주십시오', usage='[일차방정식의 해] [다차방정식의 계수들]')
    @commands.cooldown(1.0, 7, commands.BucketType.user)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=True)
    @can_use()
    async def _assemblyMethod(self, ctx, Hae:float, *, Gyesu):
        try: Gyesu = [float(i.replace('|', '').replace(' ', '')) for i in Gyesu.split('|')]
        except ValueError: return await warn(ctx=ctx, content='계수들을 제대로 입력해 주세요')
        result = []
        result.append(Gyesu[0])
        for i in range(len(Gyesu)-1):
            try: result.append(Gyesu[i+1] + (result[i] * Hae))
            except IndexError: break
        content = []
        for i in range(len(result)-2):
            content.append(f'**{len(result) - i - 2}**차항의 계수는 `{result[i]}`')
        content.append(f'**상수항**은 `{result[-2]}`')
        content.append(f'**나머지**는 `{result[-1]}`입니다')
        await sendEmbed(ctx=ctx, title='조립제법 결과', content=', '.join(content) + '입니다')
    
    @commands.group('분수계산', aliases=['ㅂㅅㄱㅅ', '분수', 'fraction'], enabled=False, help='분수 관련 계산을 합니다', usage='<통분/약분/곱셈/나눗셈/덧셈/뺄셈>')
    @can_use()
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=True)
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    async def _fraction(self, ctx):
        await sendEmbed(ctx=ctx, title='분수 관련 명령어들', content=f'`{mainprefix}분수계산 <통분/약분/곱셈/나눗셈/덧셈/뺄셈>`')

def setup(bot):
    bot.add_cog(Math(bot))