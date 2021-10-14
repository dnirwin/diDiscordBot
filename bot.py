import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

# @client.event
# async def on_ready():
#     print('Bot Active.')

@client.command()
async def greet(ctx):
    await ctx.send('Hello, how are you?')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('Enter Token Here')
