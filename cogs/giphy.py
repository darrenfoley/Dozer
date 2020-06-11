import json

import giphy_client
from discord.ext import commands
from giphy_client.rest import ApiException

from helpers.randomlists import Insult


class Giphy(commands.Cog):

    def __init__(self, client):

        self._client = client
        # I guess this path is relative to main.py ..?
        with open('./config.json') as f:
            self._config = json.load(f)

    @commands.command(name='meme')
    async def _meme(self, ctx, *, query):
        api_instance = giphy_client.DefaultApi()
        api_key = self._config['giphy']['api-key']

        try:
            api_response = api_instance.gifs_translate_get(api_key, query)
            if api_response.data.url is not None and len(api_response.data.url) != 0:
                # embed = discord.Embed()
                # embed.set_image(url=api_response.data.embed_url)
                await ctx.send(
                    f'{ctx.message.author.mention} here\'s your {query} meme, you {Insult.random()}: {api_response.data.url}')
            else:
                await ctx.send(f'#rule34fail {ctx.message.author.mention}')
        except ApiException as e:
            print(f'Exception when calling DefaultApi->gifs_translate_get with query [{query}]: {e}\n')
            await ctx.send('something went wrong')

    @commands.command(name="randommeme")
    async def _random_meme(self, ctx):
        api_instance = giphy_client.DefaultApi()
        api_key = self._config['giphy']['api-key']

        try:
            api_response = api_instance.gifs_random_get(api_key)
            if api_response.data.url is not None and len(api_response.data.url) != 0:
                await ctx.send(
                    f'{ctx.message.author.mention} here\'s your random meme, you {Insult.random()}: {api_response.data.url}')
            else:
                print(f'No URL in response when calling DefaultApi->gifs_random_get')
                await ctx.send(f'I done goofed {ctx.message.author.mention}... try again')
        except ApiException as e:
            print(f'Exception when calling DefaultApi->gifs_random_get: {e}\n')
            await ctx.send('something went wrong')


def setup(client):
    client.add_cog(Giphy(client))
