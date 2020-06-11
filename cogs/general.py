import re
from asyncio import Lock

import discord
from discord.ext import commands
from webcolors import name_to_hex

from helpers.randomlists import EightBall


class General(commands.Cog):

    def __init__(self, client):

        self._client = client
        self._colour_lock = Lock()

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        await ctx.send(f'{ctx.message.author.mention}, {EightBall.random()}')

    @commands.command(name='colour', aliases=['color'])
    async def _colour(self, ctx, *, colour):
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
            async with self._colour_lock:
                # find any existing colour roles and clean them up
                # print(f'{colour} in lock')
                user = ctx.message.author
                user_roles = user.roles
                already_has_role = False  # user already has the role they want
                # print(f'roles before cleanup: [{ctx.guild.roles}]')
                for r in user_roles:
                    if r.name == colour_ci:
                        already_has_role = True
                        continue
                    match = hex_colour_pattern.match(r.name)
                    if match is not None:
                        # Delete role if no one else is using it, else just remove the role from the user
                        # print(f'role has {len(r.members)} members')
                        num_members = len(r.members)
                        if len(r.members) == 1:
                            # print(f'start deleting role {r.name}')
                            await r.delete(reason='unused colour role')
                            # print(f'end deleting role {r.name}')
                        else:
                            # print(f'start removing role {r.name} from user')
                            await user.remove_roles(r,
                                                    f'user requested new colour role. Role still in use by {num_members - 1} others')
                            # print(f'end removing role {r.name} from user')

                    # print(f'roles after cleanup: [{ctx.guild.roles}]')
                    # # Remove role from user
                    # print(f'start removing role {r.name} from user')
                    # await user.remove_roles(r)
                    # print(f'end removing role {r.name} from user')
                    # # Delete role if no one else is using it
                    # print(f'role now has {len(r.members)} members')
                    # if len(r.members) == 0:
                    #   print(f'start deleting role {r.name}')
                    #   await r.delete()
                    #   print(f'end deleting role {r.name}')

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
                # print(f'{colour} leaving lock')

    @commands.command(name='unusedroles')
    @commands.is_owner()
    async def _unusedroles(self, ctx):
        unused = [f'{role.name}_{role.id}' for role in ctx.guild.roles if len(role.members) == 0]
        msg = 'none' if len(unused) == 0 else str(unused)
        await ctx.send(msg)


def setup(client):
    client.add_cog(General(client))
