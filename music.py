import asyncio
import youtube_dl
import discord
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio

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
FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 '
                          '-reconnect_delay_max 5',
        'options': '-vn'
        }
song_queue = {}


class Song():

    def __init__(self, prompt):
        self.prompt = prompt

    async def define_as(self, ctx, prompt: str):
        # https://qa.wujigu.com/qa/?qa=1057550/python-3-x-playing-music-with-a-bot-from-youtube-without-downloading-the-file
        try:
            ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
            info = ytdl.extract_info(prompt, download=False)
        except youtube_dl.utils.ExtractorError:
            return await ctx.send(f"Error: requested format not available :(")

        if 'entries' in info:
            info = info['entries'][0]

        self.title = info['title']
        self.artist = info['channel']
        self.bot_url = info['url']
        self.human_url = f"https://youtube.com/watch?q={info['display_id']}"
        self.audio_source = discord.FFmpegPCMAudio(self.bot_url, 
                        **FFMPEG_OPTIONS)
        return self


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['p', 'pl'])
    async def play(self, ctx, *args):
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
        await chanson.define_as(ctx, prompt)

        await self._enqueue(ctx.guild, chanson)

        # If not already playing music, then play the first song to get started,
        # then call play_next() once finished
        try:
            ctx.voice_client.play(chanson.audio_source, after=lambda e:
                    asyncio.run_coroutine_threadsafe(self._play_next(ctx), 
                        self.bot.loop))
            await ctx.send(f'Playing "{chanson.title}" by {chanson.artist}')
        except discord.errors.ClientException:
            await ctx.send(f'Enqueued "{chanson.title}" by {chanson.artist}')

    @commands.command(pass_context=True, aliases=['np'])
    async def now_playing(self, ctx):
        if not ctx.voice_client or not song_queue[ctx.guild.id]:
            await ctx.send(f'Not playing anything at the moment')
        else:
            chanson = song_queue[ctx.guild.id][0]
            await ctx.send(f'Now playing "{chanson.title}" by {chanson.artist}')

    @commands.command(pass_context=True, aliases=['q'])
    async def queue(self, ctx):
        if (ctx.guild.id not in song_queue.keys() 
                        or len(song_queue[ctx.guild.id]) == 0):
            return await ctx.send("Nothing in queue")
        embed = discord.Embed(title="Current queue", color=0xb2558d)
        index = 0
        for song in song_queue[ctx.guild.id]:
            index += 1
            embed.add_field(
                    name = f"{index}. {song.title}",
                    value = song.artist + "\n" + song.human_url,
                    inline = False)
        return await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['rm'])
    async def remove(self, ctx, *args):
        if not song_queue.get(ctx.guild.id):
            return await ctx.send("Wasn't playing anything")
          
        prompt = " ".join(args)
        if not prompt:
            return await ctx.send("I need a song name to look up!")
        for song in song_queue[ctx.guild.id]:
            if (prompt.lower() in song.title.lower()
                            or prompt.lower() in song.artist.lower()):
                if song_queue[ctx.guild.id].index(song) == 0:
                    return await self.skip(ctx)
                song_queue[ctx.guild.id].remove(song)
                return await ctx.send(f'Removed "{song.title}" by '
                                      f'{song.artist}')
        return await ctx.send(f"No match found :(") 

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        if not ctx.voice_client or not song_queue[ctx.guild.id]:
            await ctx.send(f'Nothing to skip')
        if ctx.author.voice is None:
            return await ctx.send("You are not in a voice channel!")

        skipped_song = song_queue[ctx.guild.id][0]
        # Stopping the voice client's current song causes whatever would've run
        # "after" (i.e., play_next()) to run now
        ctx.voice_client.stop()
        await ctx.send(f'Skipped "{skipped_song.title}" by {skipped_song.artist}')
        if not song_queue[ctx.guild.id]:
            return await ctx.send(f'End of queue')

    @commands.command(pass_context=True, 
            aliases=['disconnect', 'dc', 'leave', 'quit', 'exit'])
    async def stop(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send(f"Disconnected")
        else:
            await ctx.send(f"Wasn't connected in the first place lol")
        song_queue[ctx.guild.id] = []

    async def _enqueue(self, guild, chanson: Song):
        '''
        song_queue = {
                guild1_id: [Song song1, Song song2]
                guild2_id: [Song song3, Song song4]
                }
        '''
        if not song_queue.get(guild.id):
            song_queue[guild.id] = []
        song_queue[guild.id].append(chanson)

    async def _play_next(self, ctx):
        # We only pop the song when finished with it, so that _now_playing() can
        # access any currently playing song
        song_queue[ctx.guild.id].pop(0)
        if not song_queue[ctx.guild.id]:
            return await ctx.send(f'End of queue')
        chanson = song_queue[ctx.guild.id][0]
        await ctx.send(f'Playing "{chanson.title}" by {chanson.artist}')
        ctx.voice_client.play(chanson.audio_source, after=lambda e:
                asyncio.run_coroutine_threadsafe(self._play_next(ctx), 
                    self.bot.loop))


def setup(bot):
    bot.add_cog(Music(bot))
