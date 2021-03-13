from qrcode import make
from discord.ext import commands
import discord
from Tools.func import sendEmbed, can_use, warn, writedata
from Tools.var import embedcolor, mainprefix, prefix
from os import listdir, remove
from os.path import isfile
from datetime import datetime
from asyncio import TimeoutError
from PIL import Image
from barcode import get
from barcode.writer import ImageWriter

class Main(commands.Cog, name='잡다한것'):
    """
    잡다한 명령어들이 들어 있는 카테고리입니다.
    """
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='파일생성', aliases=['makefile', '파일', 'ㅍㅇ'], help='텍스트를 파일로 만듭니다', usage='<파일제목> [파일내용]')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _makefile(self, ctx, title='file.txt', *, content):
        with open(title, 'w') as f:
            f.write(content)
        dm = await ctx.author.create_dm()
        await dm.send(file=discord.File(title))
        remove(title)
        try: await ctx.message.delete()
        except: pass
        await sendEmbed(ctx=ctx, title='완료', content='DM으로 파일이 전송되었습니다.\n\n만약 전송되지 않았다면 DM을 차단하지 않았는지 확인해 보세요.')
    
    @commands.command(name='색깔보기', aliases=['색보기', 'ㅅ', 'color'], help='RGB로 입력한 색상을 보여줍니다', usage='[R] [G] [B]')
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    @can_use()
    async def _seecolor(self, ctx, R: int, G: int, B: int):
        if R > 255 or G > 255 or B > 255:
            await warn(ctx=ctx, content='RGB에 해당하는 십진수 값을 올바르게 넣어 주세요')
            return
        img = Image.new("RGB", (256,256), (R, G, B))
        img.save('color.png')
        await ctx.send(file=discord.File('color.png'))
        remove('color.png')
    
    @commands.command(name='소개설정', aliases=['ㅅㄱㅅㅈ', '소개말설정', 'introduce'], help='소개말을 설정합니다. 소개발을 비워 둘시 지워집니다.', usage='<소개말>')
    @commands.cooldown(1.0, 4, commands.BucketType.user)
    @can_use()
    async def _introduce(self, ctx, *, content=''):
        writedata(id=ctx.author.id, item='introduce', value=content)
        await sendEmbed(ctx=ctx, title='소개말설정', content=f'{ctx.author.name}님의 소개말이 `{content}`로 변경되었습니다.')
    
    @commands.command(name='이모지', aliases=['raw', '이모티콘', 'ㅇㅁㅈ'], help='이모지의 raw 값을 보여줍니다.', usage='[이모지]')
    @can_use()
    async def _emoji(self, ctx, *, emoji: discord.Emoji):
        await sendEmbed(ctx=ctx, title='이모지', content=f'`{emoji}`: {emoji}')
    
    @commands.command(name='QR코드', aliases=['qrcode', '큐알코드', 'ㅋㅇㅋㄷ'], help='QR코드를 만들어 줍니다.', usage='[내용]')
    @can_use()
    @commands.max_concurrency(1.0, commands.BucketType.user)
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    async def _qrcode(self, ctx, *, content):
        make(content).save('qrcode.png')
        await ctx.send(file=discord.File('qrcode.png'))
        remove('qrcode.png')
    
    @commands.command(name='바코드', aliases=['barcode', 'ㅂㅋㄷ', '막대코드'], help='바코드를 만들어줍니다', usage='[바코드 타입] [내용]')
    @can_use()
    @commands.max_concurrency(1.0, commands.BucketType.user)
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    async def _barcode(self, ctx, type_code, *, content):
        try:
            types = ['ean8', 'ean13', 'ean14', 'code128', 'code39', 'pzn', 'issn', 'isbn13', 'isbn10', 'jan', 'upca']
            if type_code.lower() not in types: await warn(ctx=ctx, content=f'바코드의 타입을 찾을 수 없습니다.\n타입 목록:\n```{", ".join([i.upper() for i in types])}```')
            img = get(type_code.lower(), content, writer=ImageWriter())
            file = img.save(type_code)
            await ctx.send(file=discord.File(file))
            remove(file)
        except Exception as error:
            if str(error).endswith('ISBN must start with 978 or 979.'): return await warn(ctx=ctx, content='이 타입은 코드가 978이나 979로 시작해야 합니다')
            elif str(error).endswith('can only contain numbers.'): return await warn(ctx=ctx, content='이 타입은 코드에 숫자만 들어갈 수 있습니다.')
            elif str(error).endswith('Command raised an exception: NumberOfDigitsError:'): return await warn(ctx=ctx, content='내용의 글자 수가 올바르지 않습니다')
            else: return await warn(ctx=ctx, content='저런! 에러가 발생했습니다.')
    
    @commands.command(name='첫메시지', aliases=['firstmessage', 'ㅊㅁㅅㅈ', '처음메시지'], help='채널의 첫 메시지를 보여줍니다.', usage='<채널 멘션>')
    @can_use()
    @commands.cooldown(1.0, 2.5, commands.BucketType.user)
    async def _channelInfo(self, ctx, channel:discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        message = (await channel.history().flatten())[0]
        await sendEmbed(ctx=ctx, title=f'{channel.name} 채널의 첫 메시지', content=f'[여기를 클릭하세요](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id})')

def setup(bot):
    bot.add_cog(Main(bot))