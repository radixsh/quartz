import youtube_dl
import discord
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.typing = True
intents.reactions = True
client = commands.Bot(command_prefix='>', intents=intents, help_command=None)

song_queue = {}

@commands.command(aliases=['play', 'p', 'pl', 'pla'])
async def _play(ctx, *args):
    prompt = " ".join(args)
    if not prompt:
        return await ctx.send("I need a song name to look up!")
    if ctx.author.voice is None:
        return await ctx.send("You are not in a voice channel!")
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.voice_client.move_to(ctx.author.voice.channel)

    song_title, url = get_info(prompt)

    FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
    audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
    enqueue(ctx.guild, song_title, audio_source)
    # If not already playing music, then play the first song to get started,
    # then call play_next() once finished
    if not ctx.voice_client.is_playing():
        await ctx.send(f'Playing "{song_title}"')
        ctx.voice_client.play(song_queue[ctx.guild.id][0]['source'], after=lambda e:
                asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
    else:
        await ctx.send(f'Enqueued "{song_title}"')

def get_info(prompt: str):
    YTDL_OPTIONS = {
        'format': 'bestaudio',
        'default_search': 'auto',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'source_address': '0.0.0.0'
        }
    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
    # https://qa.wujigu.com/qa/?qa=1057550/python-3-x-playing-music-with-a-bot-from-youtube-without-downloading-the-file
    info = ytdl.extract_info(prompt, download=False)
    song_title = info['entries'][0]['title']
    if 'entries' in info:
        url = info['entries'][0]['formats'][0]['url']
    elif 'formats' in info:
        url = info['formats'][0]['url']
    print(song_title)
    print(url)
    return song_title, url

def enqueue(guild, song_title, audio_source):
    '''
    song_queue = {
        guild1_id: [song1, song2],
        guild2_id: [song3, song4]}
    '''
    if not song_queue.get(guild.id):
        song_queue[guild.id] = []
    song_queue[guild.id].append({'title': song_title, 'source': audio_source})

async def play_next(ctx):
    song_queue[ctx.guild.id].pop(0)
    new_song = song_queue[ctx.guild.id][0]
    await ctx.send(f'Moving on to "{new_song["title"]}"')
    ctx.voice_client.play(new_song['source'], after=lambda e:
            asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))

@commands.command(aliases=['np'])
async def _now_playing(ctx):
    if not ctx.voice_client:
        await ctx.send(f'Not playing anything at the moment')
    else:
        await ctx.send(f'Now playing "{song_queue[ctx.guild.id][0]["title"]}"')

@commands.command(aliases=['queue', 'q'])
async def _queue(ctx):
    if len(song_queue[ctx.guild.id]) == 0:
        return await ctx.send("Nothing in queue")
    embed = discord.Embed(title="Current queue", color=0xb2558d)
    index = 0
    for song in song_queue[ctx.guild.id]:
        index += 1
        embed.add_field(
                name=f"{index}. {song['title']}",
                value=song['source'],
                inline=False)
    return await ctx.send(embed=embed)

@commands.command(aliases=['stop', 'disconnect', 'dc'])
async def _stop(ctx):
    song_queue[ctx.guild.id] = []
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send(f"Disconnected")

def setup(bot):
    bot.add_command(_play)
    bot.add_command(_now_playing)
    bot.add_command(_queue)
    bot.add_command(_stop)
