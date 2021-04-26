import discord
from discord.ext import commands
from Tools.var import mainprefix, embedcolor, errorcolor
from datetime import datetime, timedelta
from os.path import isfile, isdir
from os import makedirs
from datetime import datetime
from pickle import load, dump
import logging
import json
from datetime import datetime


async def sendEmbed(*, ctx, title, content):
    embed = discord.Embed(title=title, description=content, color=embedcolor)
    embed.set_footer(
        text=f"{ctx.author} | {mainprefix}도움", icon_url=ctx.author.avatar_url
    )
    return await ctx.send(embed=embed)


async def warn(*, ctx, content):
    embed = discord.Embed(title="경고", description=content, color=errorcolor)
    embed.set_footer(
        text=f"{ctx.author} | {mainprefix}도움", icon_url=ctx.author.avatar_url
    )
    await ctx.send(embed=embed)


async def errorlog(*, ctx, error, bot):
    embed = discord.Embed(
        title="오류", description=f"`{ctx.message.content}`", color=errorcolor
    )
    embed.add_field(
        name="오류 발생자", value=f"{ctx.author} ({ctx.author.id})\n{ctx.author.mention}"
    )
    embed.add_field(
        name="오류 발생지",
        value=f"{ctx.message.guild.name} ({ctx.message.guild.id})\n{ctx.message.channel.name} ({ctx.message.channel.id})",
    )
    embed.add_field(name="오류 내용", value=f"```py\n{error}```")
    await (bot.get_channel(825221941090189372)).send(embed=embed)


async def log(embed, bot):
    await (bot.get_channel(825221941090189372)).send(embed=embed)


def getnow(format):
    utcnow = datetime.utcnow()
    time_gap = timedelta(hours=9)
    kor_time = utcnow + time_gap
    return str(kor_time.strftime(format))


def getmail(id):
    if not isdir("mail"):
        makedirs("mail")
    if not isfile(f"mail/{id}.bin"):
        return []
    with open(f"mail/{id}.bin", "rb") as f:
        return load(f)


def writemail(id, title, content):
    if not isdir("mail"):
        makedirs("mail")
    if not isfile(f"mail/{id}.bin"):
        mails = []
    else:
        with open(f"{id}.bin", "rb") as f:
            mails = load(f)
    mails.append({"title": title, "content": content, "time": datetime.now()})
    with open(f"mail/{id}.bin", "wb") as f:
        dump(mails, f)


"""
mails = [dict, dict, dict, ...]
dict = {
    "title": 제목,
    'content': 내용,
    'time': datetime.datetime.now()
}
"""


def getdata(id, item):
    if not isdir("data"):
        makedirs("data")
    if not isfile(f"data/{id}.json"):
        with open(f"data/{id}.json", "w") as f:
            json.dump(
                {
                    "point": "0",
                    "lastCheck": "",
                    "countCheck": "0",
                    "winningRandom": "0",
                    "countRandom": "0",
                    "introduce": "소개말이 없어요.",
                    "commandCount": "0",
                },
                f,
            )
    with open(f"data/{id}.json", "r") as f:
        return json.load(f)[item]


def writedata(id, item, value):
    if not isdir("data"):
        makedirs("data")
    if not isfile(f"data/{id}.json"):
        with open(f"data/{id}.json", "w") as f:
            json.dump(
                {
                    "point": "0",
                    "lastCheck": "",
                    "countCheck": "0",
                    "sumRandom": "0",
                    "countRandom": "0",
                    "introduce": "소개말이 없어요.",
                    "commandCount": "0",
                },
                f,
            )
    with open(f"data/{id}.json", "r") as f:
        data = json.load(f)
    data[item] = value
    with open(f"data/{id}.json", "w") as f:
        json.dump(data, f)


def can_use():
    async def predicate(ctx):
        if type(ctx.channel) == discord.DMChannel:
            return False
        if not isfile("banned.bin"):
            return True
        with open("banned.bin", "rb") as f:
            banned = load(f)
        return not ctx.author.id in banned

    return commands.check(predicate)
