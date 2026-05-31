import time

import discord
from discord.ext import commands
from core.utils import get_mention_text


class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='ping', description='Check the bot latency.')
    async def ping(self, ctx):
        """Answers with pong and latency details."""
        start = time.perf_counter()
        message = await ctx.send('Pinging...')
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        embed = discord.Embed(title='Pong!', color=discord.Color.blurple())
        embed.add_field(name='Mensajes', value=f'{elapsed_ms}ms', inline=True)
        embed.add_field(name='Shard', value=f'{int(self.bot.latency * 1000)}ms', inline=True)
        embed.set_footer(text='Latency details')

        await message.edit(content=None, embed=embed)

    @commands.hybrid_command(name='hello', description='Send a friendly greeting.')
    async def hello(self, ctx):
        """Greets the user with a friendly help message."""
        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_image(url="https://cdn.discordapp.com/attachments/1292845515893112875/1510652472811716718/sk_intro.gif?ex=6a1d9840&is=6a1c46c0&hm=75f44022db9d57a6443fef63691ba86a24a4b41cbc7211b90c9f0e896e105a1c&")
        await ctx.send(f'Hello {get_mention_text(ctx.author)}, how can I help you?', embed=embed)
