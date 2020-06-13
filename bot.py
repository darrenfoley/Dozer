from os import listdir

import discord
from discord.ext import commands


class Bot:

    def __init__(self, config):
        self._config = config
        self._client = commands.Bot(command_prefix=config['discord']['prefix'])
        self._register_events()
        self._register_commands()
        self._load_cogs()

    def run(self):
        self._client.run(self._config['discord']['token'])

    def _register_events(self):
        async def on_ready():
            print('Bot is ready')
            activity = discord.Game('fetch')
            await self._client.change_presence(activity=activity)

        self._client.add_listener(on_ready)

    def _register_commands(self):

        @self._client.command(name='load')
        @commands.is_owner()
        async def _load(ctx, cog):
            """Load the specified cog"""
            self._client.load_extension(f'cogs.{cog}')
            await ctx.send(f'{cog} loaded')

        @self._client.command(name='unload')
        @commands.is_owner()
        async def _unload(ctx, cog):
            """Unload the specified cog"""
            self._client.unload_extension(f'cogs.{cog}')
            await ctx.send(f'{cog} unloaded')

        @self._client.command(name='reload')
        @commands.is_owner()
        async def _reload(ctx, cog):
            """Reload the specified cog"""
            self._client.reload_extension(f'cogs.{cog}')
            await ctx.send(f'{cog} reloaded')

        @self._client.command(name='reload_all')
        @commands.is_owner()
        async def _reload_all(ctx):
            """Reload all cogs"""
            self._load_cogs(reload=True)
            await ctx.send('All cogs reloaded')

    def _load_cogs(self, *, reload=False):
        for file in listdir('./cogs'):
            if file.endswith('.py'):
                func = self._client.reload_extension if reload else self._client.load_extension
                func(f'cogs.{file[:-3]}')
