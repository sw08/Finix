import discord
from discord.ext import commands
from Tools.var import embedcolor, mainprefix, prefix
from Tools.func import can_use, sendEmbed
from datetime import datetime

class Support(commands.Cog, name='지원'):
    '''
    봇의 지원에 관한 명령어들의 카테고리입니다
    '''
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='봇정보', aliases=['botinfo', '봇'], help='봇의 관한 정보들을 확인합니다')
    @can_use()
    async def _botinfo(self, ctx):
        embed = discord.Embed(title='봇정보', color=embedcolor)
        embed.add_field(name='이름', value=f'{self.bot.user}, {self.bot.user.id}', inline=False)
        embed.add_field(name='현재 연결상태', value=f'{round(self.bot.latency*1000)}ms', inline=False)
        embed.add_field(name='서버/유저 수', value=f'{len(self.bot.guilds)}서버, 이용자 {len(self.bot.users)}명')
        embed.add_field(name='개발자', value=f'{await self.bot.fetch_user(745848200195473490)}, id 745848200195473490', inline=False)
        embed.add_field(name='버전', value='1.0.0', inline=False)
        embed.add_field(name='개발 언어 및 라이브러리', value='파이썬, discord.py', inline=False)
        embed.add_field(name='크레딧', value='Team Orora, huntingbear21#4317, 3.141592#7499, sonix18#5414 등 많은 분들')
        embed.set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(name='도움', aliases=['도움말', 'help'], usage='<명령어>', help='명령어들의 도움말을 보여줍니다')
    @can_use()
    async def _help(self, ctx, *, arg=None):
        command = self.bot.get_command(str(arg))
        if command is not None:
            embed = discord.Embed(title='도움말', description=f'```{command.help}```', color=embedcolor)
            embed.add_field(name='사용법', value=f'{arg} {command.usage}', inline=False)
            if command.aliases != []:
                embed.add_field(name='또 다른 형태', value=', '.join(command.aliases))
            else:
                embed.add_field(name='또 다른 형태', value=' ', inline=False)
            embed.add_field(name='카테고리', value=command.cog.qualified_name)
            embed.set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            helps = []
            cogs = [i for i in self.bot.cogs]
            for i in range(len(cogs)):
                cogs[i] = self.bot.get_cog(cogs[i])
            embed = discord.Embed(title=f'1/{len(cogs)+1}페이지', description='[]는 필수적인 값을, <>는 필수적이지 않은 값들을 의미합니다. 괄호들은 빼고 입력해 주세요!', color=embedcolor)
            embed.add_field(name='접두사', value=f'피닉스의 접두사는 `{"`, `".join(prefix)}`입니다')
            for i in cogs:
                embed.add_field(name=i.qualified_name, value=f'```{i.description}```', inline=False)
            helps.append(embed)
            for i in range(len(cogs)):
                embed = discord.Embed(title=f'{i+2}/{len(cogs)+1} 페이지', color=embedcolor)
                for i in cogs[i].get_commands():
                    if i.usage is None:
                        usage = ' '
                    else:
                        usage = i.usage
                    if i.help is None:
                        embed.add_field(name=f'**{i.name}**', value=f'```{mainprefix}{i.name} {usage}```', inline=False)
                    else:
                        embed.add_field(name=f'**{i.name}**', value=f'```{mainprefix}{i.name} {usage}\n{i.help}```', inline=False)
                helps.append(embed)
            for i in range(len(helps)):
                helps[i] = helps[i].set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
            n = 0
            msg = await ctx.send(embed=helps[n])
            emojis = ['⏮️', '◀️', '▶️', '⏭️', '⏹️']
            for i in emojis:
                await msg.add_reaction(i)
            n1 = 1
            check = lambda reaction, user: reaction.message == msg and user == ctx.author and reaction.emoji in emojis
            while True:
                try:
                    if n1 == 1: reaction, _ = await self.bot.wait_for('reaction_add', check=check, timeout=30)
                    else: await self.bot.wait_for('reaction_remove', check=check, timeout=30)
                except TimeoutError:
                    try:
                        await msg.clear_reaction()
                    except:
                        await msg.delete()
                    break
                if emojis.index(reaction.emoji) == 0:
                    n = 0
                    await msg.edit(embed=helps[0])
                elif emojis.index(reaction.emoji) == 3:
                    await msg.edit(embed=helps[len(helps)-1])
                    n = len(helps)-1
                elif emojis.index(reaction.emoji) == 1:
                    if n > 0:
                        await msg.edit(embed=helps[n-1])
                        n -= 1
                elif emojis.index(reaction.emoji) == 2:
                    if n < len(helps)-1:
                        await msg.edit(embed=helps[n+1])
                        n += 1
                else:
                    try:
                        await msg.clear_reactions()
                    except:
                        await msg.delete()
                    break
                n1 = 1 - n1
    
    @commands.command(name='핑', aliases=['응답속도', 'ping'], help='봇의 현재 연결속도를 알려줍니다')
    @can_use()
    async def _ping(self, ctx):
        ping = round(self.bot.latency*1000)
        first = datetime.now()
        msg = await sendEmbed(ctx=ctx, title='핑', content=f'api 핑: `{ping}`ms')
        second = datetime.now()
        delta = second - first
        delta = round(delta.microseconds/1000)
        await msg.edit(embed=discord.Embed(title='핑', description=f'api 핑: `{ping}`ms\n메시지 핑: `{delta}`ms', color=embedcolor).set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url))        

def setup(bot):
    bot.add_cog(Support(bot))