import asyncio # pip install asyncio
import discord
import youtube_dl # pip install youtube_dl
from discord.ext import commands

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Sounds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['start','connect'])
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You\'re not in a voice channel, I cannot connect.')

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(aliases=['stop','disconnect'])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        ctx.voice_client.stop()
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
            vc.play(source)

        player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        await ctx.send(f'Now playing: {player.title}')

    @commands.command(aliases=['sb'])
    async def soundboard(self, ctx, *, query):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query)) # This works for the majority of sound files (Most Importantly: WAV, MP3, and MP4)
        vc = ctx.voice_client
        vc.play(source)
        await ctx.send(f'Now playing: {query[:-4]}')

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send('Music Paused')

    @commands.command(aliases=['unpause'])
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send('Music Resumed')

def setup(client):
    client.add_cog(Sounds(client))
