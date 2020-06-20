import json

import giphy_client
from discord.ext import commands
from giphy_client.rest import ApiException

from helpers.randomlists import Insult
from helpers.discord import send_as_embed


class Giphy(commands.Cog):

    def __init__(self, client):

        self._client = client
        # I guess this path is relative to main.py ..?
        with open('./config.json') as f:
            self._config = json.load(f)

    @commands.command(name='meme')
    async def _meme(self, ctx, *, query):
        """Get the perfect GIF using GIPHY's special sauce algorithm

        Uses GIPHY's translate endpoint: https://developers.giphy.com/docs/api/endpoint#translate
        """

        api_instance = giphy_client.DefaultApi()
        api_key = self._config['giphy']['api-key']

        try:
            api_response = api_instance.gifs_translate_get(api_key, query)
            if api_response.data.url is not None and len(api_response.data.url) != 0:
                # embed = discord.Embed()
                # embed.set_image(url=api_response.data.embed_url)
                msg = f'{ctx.message.author.mention} here\'s your {query} meme, you {Insult.random()}: {api_response.data.url}'
                await ctx.send(msg)
            else:
                msg = f'#rule34fail {ctx.message.author.mention}'
                await send_as_embed(ctx.send, msg)
        except ApiException as e:
            print(f'Exception when calling DefaultApi->gifs_translate_get with query [{query}]: {e}\n')
            msg = 'something went wrong'
            await send_as_embed(ctx.send, msg)

    @commands.command(name="randommeme")
    async def _random_meme(self, ctx, *, query=None):
        """Get a random GIF. query is optional

        Uses GIPHY's random endpoint: https://developers.giphy.com/docs/api/endpoint#random
        """

        api_instance = giphy_client.DefaultApi()
        api_key = self._config['giphy']['api-key']

        try:
            api_response = api_instance.gifs_random_get(api_key, tag=query)
            if api_response.data.url is not None and len(api_response.data.url) != 0:
                msg = f'{ctx.message.author.mention} here\'s your random{" "+ query if query is not None else ""} meme, you {Insult.random()}: {api_response.data.url}'
                await ctx.send(msg)
            else:
                print(f'No URL in response when calling DefaultApi->gifs_random_get')
                msg = f'I done goofed {ctx.message.author.mention}... try again'
                await send_as_embed(ctx.send, msg)
        except ApiException as e:
            print(f'Exception when calling DefaultApi->gifs_random_get: {e}\n')
            msg = 'something went wrong'
            await send_as_embed(ctx.send, msg)


def setup(client):
    client.add_cog(Giphy(client))
