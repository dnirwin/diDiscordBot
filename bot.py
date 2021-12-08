import discord
import os
import json
from discord.ext import commands

# Used to make custom descriptions of commands
class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()
    # General help (.help) command, shows all cogs and commands per respective cog
    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
    # Cog help (.help <cog name>) command, shows all commands for specificed cog
    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
    # Command help (.help <command name>), shows how a sawait self.get_destination().send('greet:')pecific command works
    # Done as if/elif/else because this was done before python 3.10
    async def send_command_help(self, command):
        if command.name == 'greet':
            await self.get_destination().send('greet: Bot will say hi to you')
        elif command.name == 'ping':
            await self.get_destination().send('ping: Bot returns your current ping')
        elif command.name == 'join':
            await self.get_destination().send('join: Bot joins your VC for Music Cog use (Also works as: start, connect)')
        elif command.name == 'leave':
            await self.get_destination().send('leave: Bot leaves your VC (Also works as: stop, disconnect)')
        elif command.name == 'play':
            await self.get_destination().send('play: Bot will play audio from a YouTube link')
        elif command.name == 'soundboard':
            await self.get_destination().send('soundboard: Bot will play audio from a file in root folder (Also works as: sb)')
        elif command.name == 'pause':
            await self.get_destination().send('pause: Bot will pause any audio')
        elif command.name == 'resume':
            await self.get_destination().send('resume: Bot will play any paused audio (Also works as: unpause)')
        else:
            await self.get_destination().send(command.name)

client = commands.Bot(command_prefix = '.', help_command = CustomHelpCommand())

@client.event
async def on_ready():
    print('Bot is online.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command, try \'.help\' for a list of commands')

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

f = open('config.json')
token = json.load(f)

client.run(token['token'])
