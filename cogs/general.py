import json
import random
import re

import discord
from discord.ext import commands
from webcolors import name_to_hex

from helpers.discord import send_as_embed
from helpers.randomlists import EightBall


class General(commands.Cog):

    def __init__(self, client):
        self._client = client
        with open('./config.json') as f:
            self._config = json.load(f)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.self_stream and after.self_stream:
            # If stream_categories is specified in config.json, send notification if channel is listed.
            # Otherwise send notification regardless
            send_notification = True
            try:
                stream_categories = self._config['discord']['guild-settings'][str(member.guild.id)]['stream-categories']
                send_notification = after.channel.category_id in stream_categories
            except KeyError:
                pass
            if send_notification:
                try:
                    notifications_channel_id = self._config['discord']['guild-settings'][str(member.guild.id)][
                        'stream-notifications-channel']
                    notifications_channel = self._client.get_channel(notifications_channel_id)
                    msg = f'{member.mention} is streaming in {after.channel}'
                    await send_as_embed(notifications_channel.send, msg)
                except KeyError:
                    pass

    @commands.command(name='8ball')
    async def _8_ball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        msg = f'{ctx.message.author.mention}, {EightBall.random()}'
        await send_as_embed(ctx.send, msg)

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
            msg = f'Invalid colour [{colour}] specified. Must be either a valid CSS3 colour or a hex colour (e.g. 0x00bfff). 0x000000 is not valid.'
            await send_as_embed(ctx.send, msg)
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

    @commands.command(name='decide')
    async def _decide(self, ctx, *options):
        """I'll decide for you!

        Options are separated by spaces. If an option includes a space, wrap it in double quotes
        """
        if len(options) > 0:
            choice = random.choice(options)
            await send_as_embed(ctx.send, choice)

    @commands.command(name='fetch')
    async def _fetch(self, ctx):
        """Play fetch with me plz"""
        msg = f'Okay, {ctx.message.author.mention}! 🐶'
        await send_as_embed(ctx.send, msg)

        activity = discord.Game(f'fetch with {ctx.message.author.display_name}')
        await self._client.change_presence(activity=activity)


def setup(client):
    client.add_cog(General(client))
