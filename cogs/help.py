import re

import discord
from discord.ext import commands

from helpers.discord import send_as_embed


class MyHelpCommand(commands.HelpCommand):
    _colour = 0xffcd42

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Help', colour=self._colour)

        for cog, _commands in mapping.items():
            value = ''
            filtered_commands = await self.filter_commands(_commands)
            for command in filtered_commands:
                value += f'{command.name}  -  {command.short_doc}\n'
            if len(value) > 0:
                embed.add_field(name=cog.qualified_name, value=value, inline=False)

        # Be well behaved
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_command_help(self, command):
        if not await command.can_run(self.context):
            # TODO: IS there a more direct way to trigger this?
            # Need to make sure to print the command with alias provided by user so we don't leak information
            matches = re.match(r'\.help\s+([a-zA-Z].*)', self.context.message.content)
            command_string = matches[1]
            error = await self.command_not_found(command_string)
            await self.send_error_message(error)
            return

        signature = self.get_command_signature(command)
        embed = discord.Embed(title=signature, description=command.help, colour=self._colour)
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_error_message(self, error):
        destination = self.get_destination()
        await send_as_embed(destination.send, error)

    async def command_not_found(self, command_string):
        return f'What\'s a "{command_string}"?'


class Help(commands.Cog):
    def __init__(self, client):
        self._client = client
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand()
        client.help_command.cog = self

    def cog_unload(self):
        self._client.help_command = self._original_help_command


def setup(client):
    client.add_cog(Help(client))
