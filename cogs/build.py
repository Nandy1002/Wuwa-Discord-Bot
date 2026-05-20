import os
from datetime import datetime

import discord
from discord.ext import commands

from core.utils import format_list, format_teams, resolve_asset_path


class BuildCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='build', description='Show a character build guide.')
    async def build(self, ctx, *, character: str = None):
        """Show a character build guide."""
        if not character:
            available = ', '.join(sorted(self.bot.data_manager.get_all_character_names()))
            await ctx.send(f'Please use `!build <character>`. Available characters: {available}')
            return

        key = character.strip().lower()
        character_obj = self.bot.data_manager.get_character(key)
        if not character_obj:
            available = ', '.join(sorted(self.bot.data_manager.get_all_character_names()))
            await ctx.send(f'Character not found. Available characters: {available}')
            return

        embed = discord.Embed(
            title=f'{character_obj.element} {character_obj.name} — {character_obj.element} | {character_obj.weapon_type}',
            description=character_obj.description or '',
            color=discord.Color(int(character_obj.color or 5814783)),
            timestamp=datetime.utcnow()
        )

        files = []
        character_image_path = resolve_asset_path(character_obj.image_file)
        if character_image_path:
            filename = 'character_image' + os.path.splitext(character_image_path)[1]
            files.append(discord.File(character_image_path, filename=filename))
            embed.set_image(url=f'attachment://{filename}')
        elif character_obj.banner:
            embed.set_image(url=character_obj.banner)

        if character_obj.thumbnail:
            embed.set_thumbnail(url=character_obj.thumbnail)

        best_set = character_obj.best_set
        alt_set = character_obj.alt_set

        embed.add_field(
            name=f'Best Set — {best_set.name if best_set else "N/A"}',
            value=best_set.format_pieces() if best_set else 'N/A',
            inline=False
        )
        embed.add_field(
            name=f'Alternate Set — {alt_set.name if alt_set else "N/A"}',
            value=alt_set.format_pieces() if alt_set else 'N/A',
            inline=False
        )
        embed.add_field(
            name='Substats Priority',
            value=format_list(character_obj.substats) or 'N/A',
            inline=False
        )
        embed.add_field(
            name='Weapons',
            value=f'**Best:**\n{format_list(character_obj.weapon_list())}\n\n**F2P:**\n{format_list(character_obj.f2p_list())}',
            inline=False
        )
        embed.add_field(
            name='Forte Priority',
            value=format_list(character_obj.forte_priority) or 'N/A',
            inline=False
        )
        embed.add_field(
            name='Team Compositions',
            value=format_teams(character_obj.teams) or 'N/A',
            inline=False
        )

        try:
            avatar_url = ctx.author.display_avatar.url
        except Exception:
            avatar_url = None
        embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=avatar_url)

        message_content = f'Here is your build, {ctx.author.mention}. Let me know if you want a alternate team or weapon recommendation.'
        if files:
            await ctx.send(content=message_content, embed=embed, files=files)
        else:
            await ctx.send(content=message_content, embed=embed)
