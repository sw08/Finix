import discord
from discord.ext import commands
from Tools.var import embedcolor, mainprefix
import ast
from Tools.func import is_owner, sendEmbed, log, getnow, getdata, writedata, warn
import pickle
import json
from os.path import isfile, isdir
from os import remove, makedirs, popen

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Owner(commands.Cog, name='관리자'):
    '''
    이 봇의 주인만 쓸 수 있는 카테고리입니다.
    '''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='실행', aliases=['컴파일', 'eval', 'ㄱ'], help='소스코드를 실행합니다', usage='[소스 코드]')
    @is_owner()
    async def eval(self, ctx, *, cmd):
        embed = discord.Embed(title='실행', description='', color=embedcolor)
        embed.add_field(name='**INPUT**', value=f'```py\n{cmd}```', inline=False)
        embed.set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'self': self,
                'app': self.bot,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__,
                'bot': self.bot,
                'discord': discord
                }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
        except Exception as a:
            result = a
        if result == '':
            result = 'None'
        embed.add_field(name="**OUTPUT**", value=f'```py\n{result}```', inline=False)
        embed.add_field(name='**TYPE**', value='```py\n' + str(type(result)).split("'")[1] + '```')    
        await ctx.send(embed=embed)
    
    @commands.command(name='밴', aliases=['차단', 'ban', 'ㅂ'], help='봇에게서 차단하는 명령어입니다.', usage='[유저] [이유]')
    @is_owner()
    async def _ban(self, ctx, user: discord.Member, *, reason):
        if isfile('banned.bin'):
            with open("banned.bin", "rb") as f: # 파일 읽기 (만약 파일이 있을 경우)
                ban = pickle.load(f) # 데이터를 불러오기
        else:
            with open("banned.bin", "wb+") as f: # 파일을 만들기
                ban = list()
                pickle.dump(ban, f)
        if user.id in ban:
            await sendEmbed(ctx=ctx, title='밴', content='이미 차단당한 유저입니다.')
            return
        ban.append(user.id)
        with open('banned.bin', 'wb') as f:
            pickle.dump(ban, f)
        await sendEmbed(ctx=ctx, title='밴', content=f'{user.mention}님이 {reason} 사유로 차단당하셨습니다.\n이의는 관리자 DM으로 제출해 주십시오.')
        try:
            user = await user.create_dm()
            await user.send(embed=discord.Embed(title='밴', description=f'당신은 {reason}이라는 이유로 피닉스로부터 차단당하셨습니다.\n이의는 관리자 DM으로 제출해 주십시오', color=embedcolor))
        except:
            pass
        await (self.bot.get_channel(807035238475628574)).send(f'{user.mention}님 - 밴\n사유: ```{reason}```')
        try: await (self.bot.get_guild(807033213003759626)).ban(user, reason=reason)
        except: pass
        await log(embed=discord.Embed(title='밴', description=f'{user.mention}님이 {reason}이라는 이유로 피닉스로부터 차단당하셨습니다.\n처리자: {ctx.author.mention}\n{(str(ctx.message.created_at))[:-7]}', color=embedcolor), bot=self.bot)
    
    @commands.command(name='언밴', aliases=['차단해제', 'unban', 'ㅇㅂ'], help='봇에게서 차단을 해제하는 명령어입니다.', usage='[유저] [이유]')
    @is_owner()
    async def _unban(self, ctx, user: discord.Member, *, reason):
        if isfile('banned.bin'):
            with open("banned.bin", "rb") as f: # 파일 읽기 (만약 파일이 있을 경우)
                ban = pickle.load(f) # 데이터를 불러오기
        else:
            with open("banned.bin", "wb+") as f: # 파일을 만들기
                ban = list()
                pickle.dump(ban, f)
        if user.id not in ban:
            await sendEmbed(ctx=ctx, title='밴', content='차단당하지 않은 유저입니다.')
            return
        del ban[ban.index(user.id)]
        with open('banned.bin', 'wb') as f:
            pickle.dump(ban, f)
        await sendEmbed(ctx=ctx, title='밴', content=f'{user.mention}님은 {reason} 사유로 차단해제 되셨습니다.')
        try:
            user = await user.create_dm()
            await user.send(embed=discord.Embed(title='밴', description=f'당신은 {reason}이라는 이유로 피닉스로부터 차단해제 되셨습니다.', color=embedcolor))
        except:
            pass
        try: await (self.bot.get_guild(807033213003759626)).unban(user, reason=reason)
        except: pass
        await log(embed=discord.Embed(title='밴', description=f'{user.mention}님이 {reason}이라는 이유로 피닉스로부터 차단해제 되셨습니다.\n처리자: {ctx.author.mention}\n{(str(ctx.message.created_at))[:-7]}', color=embedcolor), bot=self.bot)
    
    @commands.command(name='공지보내기', aliases=['공지발행', 'post', 'ㅂㅎ'], help='공지를 발행합니다.', usage='[공지 내용]')
    @is_owner()
    async def _post(self, ctx, *, content):
        if not isdir('posts'):
            makedirs('posts')
        if not isfile('posts/count.bin'):
            with open('posts/count.bin', 'wb') as f:
                pickle.dump(0, f)
            count = 0
        else:
            with open('posts/count.bin', 'rb') as f:
                count = pickle.load(f)
        with open(f'posts/{count}.json', 'w') as f:
            json.dump({'content': content,
                       'date': getnow('%Y년 %m월 %d일 %H시 %M분'),
                       'writer': str(ctx.author.id)}, f)
        with open(f'posts/count.bin', 'wb') as f:
            pickle.dump(count+1, f)
        await sendEmbed(ctx=ctx, title='공지발행', content='공지 발행완료')
    
    @commands.command(name='관리자송금', aliases=['강제송금', 'addpoint', 'ㄱㅅ'], help='포인트 수정 명령어입니다.', usage='[유저] [돈]')
    @is_owner()
    async def _addpoint(self, ctx, user:discord.Member, addpoint:int):
        point = int(getdata(id=user.id, item='point'))
        point += addpoint
        writedata(id=user.id, item='point', value=str(point))
        await sendEmbed(ctx=ctx, title='관리자송금', content=f'{addpoint}원이 {user.mention}님께 보내졌습니다.')
        await log(embed=discord.Embed(title='관리자송금', description=f'{user.mention}님의 돈에 `{addpoint}`가 추가되었습니다.\n처리자: {ctx.author.mention}\n{(str(ctx.message.created_at))[:-7]}', color=embedcolor), bot=self.bot)
    
    @commands.command(name='답변', aliases=['ㅁㅇㄷㅂ', '문의답변', 'answer'], help='DM으로 온 문의에 답변하는 명령어입니다.', usage='[답변할 내용]')
    @is_owner()
    async def _answer(self, ctx, *, answer=None):
        if ctx.channel.category_id != 812625850565525525:
            return await warn(ctx=ctx, content='문의채널이 아닙니다')
        if answer is not None: return await (await (self.bot.get_user(int(ctx.channel.name))).create_dm()).send(f'{ctx.author.mention}: ```{answer.content}```')
        answer = ''
        await sendEmbed(ctx=ctx, title='답변 시작', content='답변 내용을 입력해 주세요')
        channel = await (self.bot.get_user(int(ctx.channel.name))).create_dm()
        while True:
            answer = await self.bot.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
            if answer.content in ['문의종료', '종료', '끝', '문의끝', '완료']:
                await channel.send('문의가 종료되었습니다.')
                return await ctx.send('문의 끝')
            await channel.send(f'{ctx.author.mention}: ```{answer.content}```')
            await answer.add_reaction('<a:CheckGIF2:808647121061675049>')
    
    @commands.command(name='깃풀', aliases=['git pull', '깃허브 풀', 'ㄱㅍ'])
    @is_owner()
    async def _git(self, ctx):
        if not isfile('restarting.py'):
            with open('restarting.py', 'w') as f:
                f.write('import os, time\ntime.sleep(3)\nos.system("python bot.py")')
        popen('python restarting.py')
        result = popen('git pull').read()
        await sendEmbed(ctx=ctx, content=f'완료.\n```{result}```')
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Owner(bot))