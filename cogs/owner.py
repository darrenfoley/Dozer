import discord
from discord.ext import commands

from helpers.discord import load_cogs, send_as_embed


@commands.is_owner()
class Owner(commands.Cog, command_attrs={'hidden': True, }):

    def __init__(self, client):
        self._client = client

    async def cog_check(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        raise commands.NotOwner('You do not own this bot.')  # TODO: handle errors

    @commands.command(name='load')
    async def _load(self, ctx, cog):
        """Load the specified cog"""
        self._client.load_extension(f'cogs.{cog}')
        msg = f'{cog} loaded'
        await send_as_embed(ctx.send, msg)

    @commands.command(name='unload')
    async def _unload(self, ctx, cog):
        """Unload the specified cog"""
        self._client.unload_extension(f'cogs.{cog}')
        msg = f'{cog} unloaded'
        await send_as_embed(ctx.send, msg)

    @commands.command(name='reload')
    async def _reload(self, ctx, cog):
        """Reload the specified cog"""
        self._client.reload_extension(f'cogs.{cog}')
        msg = f'{cog} reloaded'
        await send_as_embed(ctx.send, msg)

    @commands.command(name='reload_all')
    async def _reload_all(self, ctx):
        """Reload all cogs"""
        load_cogs(client=self._client, reload=True)
        msg = 'All cogs reloaded'
        await send_as_embed(ctx.send, msg)

    @commands.command(name='unusedroles')
    @commands.is_owner()
    async def _unused_roles(self, ctx):
        """List roles which have no members"""
        unused = [f'{role.name}_{role.id}' for role in ctx.guild.roles if len(role.members) == 0]
        msg = 'none' if len(unused) == 0 else str(unused)
        await send_as_embed(ctx.send, msg)


def setup(client):
    client.add_cog(Owner(client))
