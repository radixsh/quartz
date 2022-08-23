import youtube_dl
import asyncio
import discord
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio

song_queue = {}

class Song():
    def __init__(self, prompt):
        self.prompt = prompt

    async def define_as(self, prompt: str):
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
        if 'entries' in info:
            info = info['entries'][0]

        self.title = info['title']
        self.artist = info['channel']
        self.bot_url = info['url']
        self.human_url = f"https://youtube.com/watch?q={info['display_id']}"
        FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
                }
        self.audio_source = discord.FFmpegPCMAudio(self.bot_url, **FFMPEG_OPTIONS)
        return self

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['play', 'p', 'pl', 'pla'])
    async def _play(self, ctx, *args):
        prompt = " ".join(args)
        if not prompt:
            return await ctx.send("I need a song name to look up!")
        if ctx.author.voice is None:
            return await ctx.send("You are not in a voice channel!")
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

        chanson = Song(prompt)
        await chanson.define_as(prompt)
        print(f'Playing/queuing "{chanson.title}" by {chanson.artist}')

        await self.enqueue(ctx.guild, chanson)

        # If not already playing music, then play the first song to get started,
        # then call play_next() once finished
        try:
            await ctx.send(f'Playing "{chanson.title}" by {chanson.artist}')
            ctx.voice_client.play(chanson.audio_source, after=lambda e:
                    asyncio.run_coroutine_threadsafe(self.play_next(ctx), 
                        self.bot.loop))
        except discord.errors.ClientException:
            await ctx.send(f'Enqueued "{chanson.title}"')

    @commands.command(pass_context=True, aliases=['now_playing', 'np'])
    async def _now_playing(self, ctx):
        if not ctx.voice_client or not song_queue[ctx.guild.id]:
            await ctx.send(f'Not playing anything at the moment')
        else:
            chanson = song_queue[ctx.guild.id][0]
            await ctx.send(f'Now playing "{chanson.title}" by {chanson.artist}')

    @commands.command(pass_context=True, aliases=['queue', 'q'])
    async def _queue(self, ctx):
        if ctx.guild.id not in song_queue.keys() or len(song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Nothing in queue")
        embed = discord.Embed(title="Current queue", color=0xb2558d)
        index = 0
        for song in song_queue[ctx.guild.id]:
            index += 1
            embed.add_field(
                    name=f"{index}. {song.title}",
                    value=song.human_url,
                    inline=False)
        return await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['stop', 'disconnect', 'dc'])
    async def _stop(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send(f"Disconnected")
        else:
            await ctx.send(f"Wasn't connected in the first place lol")
        song_queue[ctx.guild.id] = []

    async def enqueue(self, guild, chanson: Song):
        '''
        song_queue = {
                guild1_id: [Song song1, Song song2]
                guild2_id: [Song song3, Song song4]
                }
        '''
        if not song_queue.get(guild.id):
            song_queue[guild.id] = []
        song_queue[guild.id].append(chanson)

    async def play_next(self, ctx):
        # We only pop the song when finished with it, so that _now_playing() can
        # access any currently playing song
        song_queue[ctx.guild.id].pop(0)
        chanson = song_queue[ctx.guild.id][0]
        await ctx.send(f'Playing "{chanson.title}" by {chanson.artist}')
        ctx.voice_client.play(chanson.audio_source, after=lambda e:
                asyncio.run_coroutine_threadsafe(self.play_next(ctx), 
                    self.bot.loop))

def setup(bot):
    bot.add_cog(Music(bot))
