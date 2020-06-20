import discord
from discord.ext import commands

from helpers.discord import load_cogs


class Bot:

    def __init__(self, config):
        self._config = config
        self._client = commands.Bot(command_prefix=config['discord']['prefix'])
        self._id = config['discord']['bot-id']  # TODO: Is there a better way to get this?
        self._register_events()
        load_cogs(client=self._client)

    def run(self):
        self._client.run(self._config['discord']['token'])

    def _register_events(self):
        async def on_ready():
            print('Bot is ready')
            activity = discord.Game('fetch')
            await self._client.change_presence(activity=activity)

        self._client.add_listener(on_ready)

