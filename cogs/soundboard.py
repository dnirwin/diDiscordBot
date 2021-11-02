import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

class Soundboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def death(self, ctx):
        if (ctx.author.voice):
            voice_channel = ctx.message.author.voice.channel
            voice = await voice_channel.connect()
            source = FFmpegPCMAudio('gmoddeath.wav')
            player = voice.play(source)
        else:
            await ctx.send('You\'re not in a voice channel, I cannot connect.')

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(Soundboard(client))
