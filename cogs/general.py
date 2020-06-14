import re

import discord
from discord.ext import commands
from webcolors import name_to_hex

from helpers.randomlists import EightBall


class General(commands.Cog):

    def __init__(self, client):
        self._client = client

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        await ctx.send(f'{ctx.message.author.mention}, {EightBall.random()}')

    @commands.command(name='colour', aliases=['color'])
    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    async def _colour(self, ctx, *, colour):
        """Set name colour with CSS3 colours or hex (e.g. 0x00aaff)

        CSS3 colours: https://www.w3.org/TR/css-color-3/#svg-color
        Hex colour picker: https://www.google.com/search?q=hex+colour+picker
        """

        colour_ci = colour.upper()

        # Check if valid hex colour
        invalid_colour = False
        hex_colour_pattern = re.compile("^0X[0-9A-F]{6}$")
        match = hex_colour_pattern.match(colour_ci)
        if match is None:
            try:
                c = name_to_hex(colour)
                colour = f'0x{c[1:]}'
                colour_ci = colour.upper()
            except ValueError:
                invalid_colour = True
        elif colour_ci == '0X000000':
            invalid_colour = True

        if invalid_colour:
            await ctx.send(
                f'Invalid colour [{colour}] specified. Must be either a valid CSS3 colour or a hex colour (e.g. 0x00bfff). 0x000000 is not valid.')
        else:
            # find any existing colour roles and clean them up
            user = ctx.message.author
            user_roles = user.roles
            already_has_role = False  # user already has the role they want
            for r in user_roles:
                if r.name == colour_ci:
                    already_has_role = True
                    continue
                match = hex_colour_pattern.match(r.name)
                if match is not None:
                    # Delete role if no one else is using it, else just remove the role from the user
                    num_members = len(r.members)
                    if num_members == 1:
                        await r.delete(reason='unused colour role')
                    else:
                        await user.remove_roles(r,
                                                reason=f'user requested new colour role. Role still in use by {num_members - 1} others')

            if already_has_role:
                return

            # check if role already exists
            all_roles = ctx.guild.roles
            role = next((x for x in all_roles if x.name == colour_ci), None)
            if role is None:
                # it does not exist. create it
                colour_int = int(colour_ci, 16)
                colour_obj = discord.Colour(colour_int)
                role = await ctx.guild.create_role(name=colour_ci, colour=colour_obj)

            await user.add_roles(role)

    @commands.command(name='fetch')
    async def _fetch(self, ctx):
        """Play fetch with me plz"""
        await ctx.send(f'Okay, {ctx.message.author.mention}! 🐶')

        activity = discord.Game(f'fetch with {ctx.message.author.display_name}')
        await self._client.change_presence(activity=activity)

    @commands.command(name='unusedroles')
    @commands.is_owner()
    async def _unusedroles(self, ctx):
        """List roles which have no members"""
        unused = [f'{role.name}_{role.id}' for role in ctx.guild.roles if len(role.members) == 0]
        msg = 'none' if len(unused) == 0 else str(unused)
        await ctx.send(msg)


def setup(client):
    client.add_cog(General(client))
