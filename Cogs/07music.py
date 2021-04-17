from discord.ext import commands
import discord
from Tools.func import can_use, sendEmbed, warn, errorlog
from Tools.var import mainprefix
import asyncio
import youtube_dl
from os.path import isfile, isdir
from os import remove, rename, makedirs

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
    
    @commands.group('음악', aliases=['ㅇㅇ', 'music', '노래'], help='음악 관련 기능을 실행합니다', usage='<재생/완전정지/일시정지>', invoke_without_command=True)
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    @can_use()
    async def music(self, ctx):
        await sendEmbed(ctx=ctx, title='음악 명령어', content=f'`{mainprefix}음악 (재생/완전정지/일시정지)`')
    
    @music.command(name='재생', aliases=['play', 'ㅈㅅ'])
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    @can_use()
    async def _play(self, ctx, *, url):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                msg = await sendEmbed(ctx=ctx, title='음악 재생', content='이미 노래가 재생중이에요. 건너뛸까요?')
                await msg.add_reaction('<:Check:808647119275294762>')
                await msg.add_reaction('<:No:808647119048540170>')
                try:
                    reaction, _user =  await self.bot.wait_for('reaction_add', timeout=30, check=lambda reaction, user: user.id == ctx.author.id and reaction.message == msg)
                except asyncio.TimeoutError:
                    await sendEmbed(ctx=ctx, title='음악', content='취소되었습니다.')
                    return
                if reaction.emoji == '<:No:808647119048540170>': return
                ctx.voice_client.stop()
        try: await ctx.author.voice.channel.connect()
        except: pass
        if not isdir('Music'): makedirs('Music')
        if isfile(f'Music/{ctx.guild.id}_first.m4a'): remove(f'Music/{ctx.guild.id}_first.m4a')
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
            #'download_archive': f'Music/{ctx.author.id}.mp3'
        }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            info = ydl.extract_info(url, download=False) # 유튜브에 저장된 파일명을 받아옵니다.
            filename = ydl.prepare_filename(info)
            rename('.'.join(filename.split('.')[:-1]) + '.m4a', f'Music/{ctx.guild.id}_first.m4a')
        except Exception as error:
            await warn(ctx=ctx, content='재생을 위해 다운로드 중 에러가 발생했어요.')
            raise error
        ctx.voice_client.play(discord.FFmpegPCMAudio(f'Music/{ctx.guild.id}_first.m4a'))
        
    @commands.group('재생목록', invoke_without_command=True)
    @can_use()
    async def playlist(self, ctx):
        await sendEmbed(ctx=ctx, title='재생목록', content=f'{mainprefix}재생목록 (추가/제거/리셋)')
    
    @

def setup(bot):
    bot.add_cog(Music(bot))