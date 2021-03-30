import discord
from discord.ext import commands
from Tools.var import embedcolor, mainprefix, prefix, version
from Tools.func import can_use, sendEmbed, warn, getmail
from datetime import datetime
from os import makedirs
from os.path import isfile, isdir
from EZPaginator import Paginator
import json
import pickle

class Support(commands.Cog, name='지원'):
    '''
    봇의 지원에 관한 명령어들의 카테고리입니다
    '''
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='봇정보', aliases=['botinfo', '봇 정보', 'ㅂㅈㅂ'], help='봇의 관한 정보들을 확인합니다')
    @can_use()
    async def _botinfo(self, ctx):
        embed = discord.Embed(title='봇정보', color=embedcolor)
        embed.add_field(name='이름', value=f'{self.bot.user}, {self.bot.user.id}', inline=False)
        embed.add_field(name='현재 연결상태', value=f'{round(self.bot.latency*1000)}ms', inline=False)
        embed.add_field(name='서버/유저 수', value=f'{len(self.bot.guilds)}서버, 이용자 {len(self.bot.users)}명')
        embed.add_field(name='개발자', value=f'{await self.bot.fetch_user(745848200195473490)}, id 745848200195473490', inline=False)
        embed.add_field(name='버전', value=version + ' 릴리즈', inline=False)
        embed.add_field(name='개발 언어 및 라이브러리', value='파이썬, discord.py', inline=False)
        embed.add_field(name='크레딧', value='심심러, Team Orora, huntingbear21, 3.141592 등 많은 분들', inline=False)
        embed.add_field(name='링크', value=f'[서포트 서버 초대](http://support.thinkingbot.kro.kr)\n[ThinkingBot 권한없이 초대](http://invite.thinkingbot.kro.kr)\n[ThinkingBot 최소권한 초대](http://invite2.thinkingbot.kro.kr)\n[ThinkingBot 깃허브](http://github.thinkingbot.kro.kr)')
        embed.set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='도움', aliases=['도움말', 'help', 'ㄷㅇ'], usage='<명령어>', help='명령어들의 도움말을 보여줍니다')
    @can_use()
    async def _help(self, ctx, *, arg=None):
        command = self.bot.get_command(str(arg))
        if (command is not None) or str(type(command)) == 'discord.ext.commands.core.Group':
            embed = discord.Embed(title='도움말', description=f'```{command.help}```', color=embedcolor)
            if command.usage is None: usage = ''
            else: usage = command.usage
            embed.add_field(name='사용법', value=f'{mainprefix}{arg} {usage}', inline=False)
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
            for i in cogs:
                if i.get_commands() == []: del cogs[cogs.index(i)]
            embed = discord.Embed(title=f'1/{len(cogs)+1}페이지 - 카테고리 목록', description='[]는 필수적인 값을, <>는 필수적이지 않은 값들을 의미합니다. 괄호들은 빼고 입력해 주세요!', color=embedcolor)
            embed.add_field(name='접두사', value=f'{self.bot.user.name}의 접두사는 `{"`, `".join(prefix)}`입니다')
            for i in cogs:
                embed.add_field(name=f'**{i.qualified_name}**', value=f'`{i.description}`', inline=False)
            helps.append(embed)
            for i in range(len(cogs)):
                embed = discord.Embed(title=f'{i+2}/{len(cogs)+1} 페이지 - {cogs[i].qualified_name}', description=f'**`{cogs[i].description}`**', color=embedcolor)
                commandList = cogs[i].get_commands()
                '''
                for i in commandList:
                    if type(i) == commands.core.Group:
                        for j in i.commands:
                            CMD = j
                            CMD.name = i.name + CMD.name
                            commandList.append(CMD)
                        del commandList[commandList.index(i)]'''
                for i in commandList:
                    if i.enabled == False: pass
                    if i.usage is None:
                        usage = ''
                    else:
                        usage = ' ' + i.usage
                    if i.help is None:
                        embed.add_field(name=f'\n**{i.name}**', value=f'`{mainprefix}{i.name}{usage}`\n', inline=False)
                    else:
                        embed.add_field(name=f'\n**{i.name}**', value=f'`{mainprefix}{i.name}{usage}`\n{i.help}\n', inline=False)
                helps.append(embed)
            for i in range(len(helps)):
                helps[i] = helps[i].set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url)
            page = Paginator(bot=self.bot, message=await ctx.send(embed=helps[0]), embeds=helps, only=ctx.author, use_extend=True, extended_emojis=['<:leftend:809567692692258847>', '<:left:809567681652981781>', '<:right:809567682164424738>', '<:rightend:809567696307617863>'])
            await page.start()
    
    @commands.command(name='핑', aliases=['응답속도', 'ping', 'ㅍ'], help='봇의 현재 연결속도를 알려줍니다')
    @can_use()
    async def _ping(self, ctx):
        ping = round(self.bot.latency*1000)
        first = datetime.now()
        msg = await sendEmbed(ctx=ctx, title='핑', content=f'api 핑: `{ping}`ms')
        second = datetime.now()
        delta = second - first
        delta = round(delta.microseconds/1000)
        await msg.edit(embed=discord.Embed(title='핑', description=f'api 핑: `{ping}`ms\n메시지 핑: `{delta}`ms', color=embedcolor).set_footer(text=f'{ctx.author} | {mainprefix}도움', icon_url=ctx.author.avatar_url))        
    
    @commands.command(name='공지', aliases=['공지읽기', 'readpost', 'ㄱㅈ'], help='공지를 보여줍니다')
    @can_use()
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    async def _readpost(self, ctx):
        if not isdir('posts'):
            makedirs('posts')
        if not isfile('posts/count.bin'):
            with open('posts/count.bin', 'wb') as f:
                pickle.dump(0, f)
        with open('posts/count.bin', 'rb') as f:
            count = pickle.load(f)
        if count == 0:
            await warn(ctx=ctx, content='공지가 없습니다')
            return
        embeds = []
        for i in range(count):
            with open(f'posts/{i}.json') as f:
                data = json.loads(f.read())
                date = data['date']
                content = data['content']
                writer = await self.bot.fetch_user(int(data['writer']))
            embeds.append(discord.Embed(title=f'공지 - {1+i}개/{count}개', description=f'{content}\n\n------------------\n[서포트 서버 들어오기](http://support.thinkingbot.kro.kr)\n[ThinkingBot 권한없이 초대](http://invite.thinkingbot.kro.kr)\n[ThinkingBot 최소권한 초대](http://invite2.thinkingbot.kro.kr)\n[ThinkingBot 깃허브](http://github.thinkingbot.kro.kr)', color=embedcolor).set_footer(icon_url=writer.avatar_url, text=f'{writer} - {date}'))
        embeds.reverse()
        page = Paginator(bot=self.bot, message=await ctx.send(embed=embeds[0]), embeds=embeds, only=ctx.author, use_extend=True, extended_emojis=['<:leftend:809567692692258847>', '<:left:809567681652981781>', '<:right:809567682164424738>', '<:rightend:809567696307617863>'])
        await page.start()
    
    @commands.command(name='초대', aliases=['ㅊㄷ', 'invite', '링크'], help='봇과 서포트 서버, 그리고 이 서버의 초대를 보여줍니다.')
    @can_use()
    async def _invite(self, ctx):
        try:
            invite = '[현재 서버 초대](' + (await ctx.guild.channels[0].create_invite()).url + ')'
        except:
            invite = ''
        await sendEmbed(ctx=ctx, title='초대', content=f'[서포트 서버 초대](http://support.thinkingbot.kro.kr)\n[ThinkingBot 권한없이 초대](http://invite.thinkingbot.kro.kr)\n[ThinkingBot 최소권한 초대](http://invite.thinkingbot.kro.kr)\n{invite}')
    
    @commands.command(name='메일함', aliases=['메일', 'mails', 'ㅁㅇ'], help='자신에게 온 메일들을 봅니다')
    @can_use()
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    async def _mails(self, ctx):
        mails = getmail(id=ctx.author.id)
        mails.reverse() 
        main_embed = discord.Embed(title='메일함', color=embedcolor)
        for i in mails:
            if len(i['title']) > 20: title = i['title'][:20]
            else: title = i['title']
            main_embed.add_field(name=title, value='`' + i['time'].strftime("%y.%m.%d %H:%M") + '`')
        embeds = [main_embed]
        for i in mails:
            embeds.append(discord.Embed(title=i['title'], description=i['content'], color=embedcolor).set_footer(text=i['time'].strftime("%y.%m.%d %H:%M")))
        page = Paginator(bot=self.bot, message=await ctx.send(embed=embeds[0]), embeds=embeds, only=ctx.author, auto_delete=True)
        await page.start()

def setup(bot):
    bot.add_cog(Support(bot))