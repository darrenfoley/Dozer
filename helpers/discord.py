from os import listdir

import discord


async def send_as_embed(send_func, message):
    colour = 0xffcd42
    embed = discord.Embed(description=message, colour=colour)
    await send_func(embed=embed)


def load_cogs(*, client, reload=False):
    for file in listdir('./cogs'):
        if file.endswith('.py'):
            func = client.reload_extension if reload else client.load_extension
            func(f'cogs.{file[:-3]}')
