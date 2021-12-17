from re import search
import re
from tokenize import triple_quoted
import discord
from discord import channel
from discord import message, FFmpegAudio
from discord.client import Client
from discord.ext import commands
from discord.ext.commands.core import after_invoke, check, has_permissions
from io import BytesIO
import uuid
import os
import asyncio
from discord.flags import Intents
from gtts import gTTS
import random
from validators.url import url
import youtube_dl
import validators
from discord import embeds
import time
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents().all()

TOKEN = "OTA4OTU1MDc1NDgzOTUxMTA0.YY9QYQ.NtTctO2zR84AJCDxQMVlJaq56mg"
client = commands.Bot(command_prefix="*",intents = intents)
stop = 0
vc = None
is_loop = False
queue_list = []
is_skipping = False
men_user = None
now_del = 0
limits = None


def time_format(seconds: int):
    if seconds is not None:
        seconds = int(seconds)
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if d > 0:
            return '{:02d}D {:02d}H {:02d}m {:02d}s'.format(d, h, m, s)
        elif h > 0:
            return '{:02d}H {:02d}m {:02d}s'.format(h, m, s)
        elif m > 0:
            return '{:02d}m {:02d}s'.format(m, s)
        elif s > 0:
            return '{:02d}s'.format(s)
    return '-'
@client.event
async def on_ready():
    print("READY")


@client.command()
async def call(ctx):
    global stop
    stop = 0
    msg = ctx.message.content
    for u in ctx.message.mentions:
        x = u.mention 
        while stop == 0:

            await ctx.send("Come" + x)
            await asyncio.sleep(3)

@client.command()
async def stoptag(ctx):
    global stop
    stop = 1
    await ctx.send("**__OK STOP__**")


@client.command(pass_context=True)
@commands.has_guild_permissions(mute_members=True)
async def mute(ctx):
    for u in ctx.message.mentions:

        await ctx.send("You have been muted!" + u.mention)
        await u.edit(mute = True)

@mute.error
async def mute_error(ctx,error):
    print(error)
    print(type(error))
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to mute!".format(ctx.message.author.mention)
        await ctx.send(text)


@client.command(pass_context=True)
@commands.has_guild_permissions(mute_members=True)
async def unmute(ctx):
    for u in ctx.message.mentions:

        await ctx.send("You have been release!" + u.mention)
        await u.edit(mute = False)


@unmute.error
async def mute_error(ctx,error):
    print(error)
    print(type(error))
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to unmute!".format(ctx.message.author.mention)
        await ctx.send(text)


@client.command()
async def join(ctx):
    global vc
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice chat!")
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await channel.connect()
        await ctx.send("Hello I'm in your VC")
    else:
        vc = await ctx.voice_client.move_to(channel)

@client.command()
async def leave(ctx):
    global vc
    if (ctx.voice_client):
        await ctx.voice_client.disconnect()
        await ctx.send("Bye ")
    else:
        await ctx.send("I'm not in any of your voice channel!")


@client.command()
async def ahh(ctx):
    global vc
    voice_channel = ctx.author.voice.channel
    try:
        vc = await voice_channel.connect()
    except Exception as e:
        print(e)
    print(12)
    text = ctx.message.clean_content[4:]
    filename = text + ".wav"
    filename = "temp.mp3"
    print(123)
    tts = gTTS(text=text, lang="th")
    tts.save(filename)
    print(1234)
    await ctx.send("LINK STARTTTTTT")
    player = vc.play(discord.FFmpegPCMAudio(source=filename))
    #player = vc.FFmpegPCMAudio(filename, after=lambda: print('done'))
    #player.start()
    while vc.is_playing():
        await asyncio.sleep(.1)
    tts = gTTS(text=text, lang="th")
    tts.save(filename)
    player = vc.play(discord.FFmpegPCMAudio(source=filename))
    await vc.disconnect()


@client.command()
async def thanos(ctx):
    voice_channel = ctx.author.voice.channel
    global vc
    vc = await voice_channel.connect()
    player = vc.play(discord.FFmpegPCMAudio(source = "sound_effect/Thanos.mp3"))
    while vc.is_playing():
        await asyncio.sleep(0.1)
    await vc.disconnect()
    thanos_list = ctx.author.voice.channel.members
    thanos_list = random.choices(thanos_list,k=int(len(thanos_list)/2))
    for unlucky in thanos_list:
        await unlucky.move_to(client.get_channel(909353253303615488))


#Old version of play command(Download)
"""
@client.command()
async def play(ctx,url:str):
    chk_file = os.path.isfile("music.mp3")
    try:
        if chk_file:
            os.remove("music.mp3")
    except:
        await ctx.send("Song is currently playing")
    voice_channel = ctx.author.voice.channel
    global vc
    vc = await voice_channel.connect()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "music.mp3")
    player = vc.play(discord.FFmpegPCMAudio(source = "music.mp3"))
    while vc.is_playing():
        await asyncio.sleep(0.1)
"""

@client.command()
async def stop(ctx):
    global vc
    vc.stop()
    await ctx.send("STOPPED" + ctx.author.mention)
    await vc.disconnect()


@client.command(brief = "play the youtube video", aliases=['play','sing','paly'])
async def p(ctx): #,video_link:str
    global is_loop
    global vc
    global queue_list
    global is_skipping

    video_link = ctx.message.clean_content.split(" ")
    video_link.pop(0)
    video_link = " ".join(video_link)
    chk_file = os.path.isfile("music.mp3")
    try:
        if chk_file:
            os.remove("music.mp3")
    except:
        await ctx.send("Song is currently playing")
    
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  
    }
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    if(validators.url(video_link)):
        print("YESYESYES")
        with ydl:
            result = ydl.extract_info(
                video_link,
                download=False 
            )
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
            URL = info['formats'][0]['url']
    else:
        print("NONONO")
        print(video_link)
        #video_link = '"' + video_link + '"'
        #print(video_link)
        with ydl:
            result = ydl.extract_info(
                f"ytsearch:{video_link}",
                download=False 
            )
            result= result['entries'][0]
        #await ctx.send("added " + result["title"] + " to queue_list")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{video_link}", download=False)
            URL = info['entries'][0]['formats'][0]['url']
    queue_list.append([result,URL, result["id"]])
    embed=discord.Embed(title="Added song to queue_list ", url=str("https://youtu.be/"+ result["id"]), color=0x00bfff)
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/818876983567319110.gif?size=96")
    embed.add_field(name="queue_list number", value=str(len(queue_list)), inline=True)
    embed.add_field(name="duration", value=time_format(result["duration"]), inline=True)
    embed.add_field(name="Requested by", value=ctx.author.mention, inline=False)
    embed.set_footer(text="Acknowledged.",icon_url="https://cdn.discordapp.com/emojis/734349790803918848.gif?size=96")
    await ctx.send(embed=embed)
    await ctx.message.delete()
    if vc==None or not (vc.is_playing() or vc.is_paused()):
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
        while len(queue_list) > 0:
            current_song = queue_list.pop(0)
            embed=discord.Embed(title=str("Now playing " + current_song[0]["title"]), url=str("https://youtu.be/"+ current_song[0]["id"]), description=("Duration: " +time_format(current_song[0]["duration"]) ), color=0x00b3ff)
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/739616791084400701.gif?size=96")
            embed.set_footer(text="Enjoy your music ☺☺♪",icon_url="https://cdn.discordapp.com/emojis/837319797128953878.png?size=96")
            await ctx.send(embed=embed)
            current_URL = current_song[1]
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            while True:
                player = vc.play(discord.FFmpegPCMAudio(current_URL, **FFMPEG_OPTIONS))
                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(0.1)
                if is_loop ==False:
                    break
        await vc.disconnect()



@client.command()
async def pause(ctx):
    global vc
    vc.pause()


@client.command()
async def resume(ctx):
    global vc
    vc.resume()

@client.command()
async def loop(ctx):
    global is_loop
    is_loop = not is_loop
    if is_loop:
        await ctx.send("loop🔁")
    else:
        await ctx.send("Loop🔁 off")

@client.command(brief = "VIP", aliases=['pnow','pn'])
async def qn(ctx):
    global queue_list
    video_link = ctx.message.clean_content.split(" ")
    video_link.pop(0)
    video_link = " ".join(video_link)
    chk_file = os.path.isfile("music.mp3")
    try:
        if chk_file:
            os.remove("music.mp3")
    except:
        await ctx.send("Song is currently playing")
    
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  
    }
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    if(validators.url(video_link)):
        with ydl:
            result = ydl.extract_info(
                video_link,
                download=False 
            )
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
            URL = info['formats'][0]['url']
    else:
        #video_link = '"' + video_link + '"'
        with ydl:
            result = ydl.extract_info(
                f"ytsearch:{video_link}",
                download=False 
            )
            result= result['entries'][0]
        #await ctx.send("added " + result["title"] + " to queue_list")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{video_link}", download=False)
            URL = info['entries'][0]['formats'][0]['url']
    queue_list.insert(0,[result,URL, result["id"]])
    embed=discord.Embed(title="Added song to queue_list ", url=str("https://youtu.be/"+ result["id"]), color=0x00bfff)
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/818876983567319110.gif?size=96")
    embed.add_field(name="queue_list number", value=str(len(queue_list)), inline=True)
    embed.add_field(name="duration", value=time_format(result["duration"]), inline=True)
    embed.set_footer(text="Acknowledged.",icon_url="https://cdn.discordapp.com/emojis/734349790803918848.gif?size=96")
    await ctx.send(embed=embed)



@client.command(aliases=['q'])
async def queue(ctx):
    global queue_list
    tq = ""
    x = 1
    for i in queue_list:
        tq += str(x)+".  "+ i[0]["title"]+"\n\n"
        x+=1
    embed=discord.Embed(title="queue_list list ", description= tq, color=0x00bfff)
    embed.set_footer(text="Enjoy your day.",icon_url="https://cdn.discordapp.com/emojis/755794386650005596.gif?size=96")
    await ctx.send(embed=embed)


@client.command()
async def skip(ctx):
    global vc
    vc.stop()
    ctx.send("Skipped!")
    await ctx.message.delete()

def check_mention(m):
    global men_user
    global now_del
    global limits
    if m.author in men_user:
        now_del += 1
        if now_del <= limits:
            return 1
    return 0

@client.command()
async def clean(ctx, limit: int):
    global men_user
    global limits
    limits = limit
    men_user = ctx.message.mentions
    deleted = await ctx.channel.purge(limit = 100,check=check_mention)


@client.command()
async def roll(ctx):
    img_url = ["https://media.discordapp.net/attachments/250226310926827520/913783446441197628/unknown.png","https://media.discordapp.net/attachments/250226310926827520/913784154112548874/unknown.png","https://cdn.discordapp.com/attachments/250226310926827520/913784196529520660/unknown.png","https://media.discordapp.net/attachments/250226310926827520/913784239156264970/unknown.png","https://cdn.discordapp.com/attachments/250226310926827520/913784279497060393/unknown.png","https://cdn.discordapp.com/attachments/250226310926827520/913784332911530084/unknown.png"]
    result = (random.randint(1,6))
    embed=discord.Embed(title="Roll Result", color=0x00ccff)
    embed.set_thumbnail(url=img_url[result-1])
    embed.add_field(name="result", value=result, inline=False)
    await ctx.send(embed=embed)
client.run(TOKEN)
#