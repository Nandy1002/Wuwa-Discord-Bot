import os
from datetime import datetime

import discord
from discord.ext import commands

from core.utils import format_list, format_teams, resolve_asset_path, get_mention_text
from core.image_generator import generate_materials_image


class CharacterCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='character', description='Show a character build guide.')
    async def character_cmd(self, ctx, *, character: str = None):
        """Show a character guide."""
        if not character:
            available = ', '.join(sorted(self.bot.data_manager.get_all_character_names()))
            await ctx.send(f'Please use `/character <character>`. Available characters: {available}')
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

        # Send a fast processing message
        processing_msg = await ctx.send(f"⏳ I am processing the image for **{character_obj.name.capitalize()}**... please wait!")

        files = []
        
        # Generate the dynamic materials image
        try:
            import asyncio
            # Offload generation to thread so it doesn't block
            img_bytes = await asyncio.to_thread(generate_materials_image, character_obj, self.bot.data_manager)
            files.append(discord.File(fp=img_bytes, filename="materials.png"))
            embed.set_image(url="attachment://materials.png")
        except Exception as e:
            print(f"Image generation failed: {e}")
            # Fallback to standard banner if it fails
            character_image_path = resolve_asset_path(character_obj.image_file)
            if character_image_path:
                filename = 'character_image' + os.path.splitext(character_image_path)[1]
                files.append(discord.File(character_image_path, filename=filename))
                embed.set_image(url=f'attachment://{filename}')
            elif character_obj.banner:
                embed.set_image(url=character_obj.banner)


        if character_obj.thumbnail:
            embed.set_thumbnail(url=character_obj.thumbnail)

        best_set_key = character_obj.best_set
        alt_set_key = character_obj.alt_set
        
        best_set = self.bot.data_manager.echosets.get(best_set_key) if best_set_key else None
        alt_set = self.bot.data_manager.echosets.get(alt_set_key) if alt_set_key else None

        if best_set_key:
            embed.add_field(
                name=f'Best Set — {best_set.name if best_set else (best_set_key or "N/A")}',
                value=best_set.format_pieces() if best_set else 'N/A',
                inline=False
            )
        
        if alt_set_key:
            embed.add_field(
                name=f'Alternate Set — {alt_set.name if alt_set else (alt_set_key or "N/A")}',
                value=alt_set.format_pieces() if alt_set else 'N/A',
                inline=False
            )
            
        if character_obj.substats:
            embed.add_field(
                name='Substats Priority',
                value=format_list(character_obj.substats) or 'N/A',
                inline=False
            )
            
        if character_obj.weapons:
            embed.add_field(
                name='Weapons',
                value=f'**Best:**\n{format_list(character_obj.weapon_list())}\n\n**F2P:**\n{format_list(character_obj.f2p_list())}',
                inline=False
            )
            
        if character_obj.forte_priority:
            embed.add_field(
                name='Forte Priority',
                value=format_list(character_obj.forte_priority) or 'N/A',
                inline=False
            )
            
        if character_obj.teams:
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

        message_content = f'Here is the character information and farming materials for **{character_obj.name.capitalize()}**, {get_mention_text(ctx.author)}!'
        
        try:
            if files:
                await processing_msg.edit(content=message_content, embed=embed, attachments=files)
            else:
                await processing_msg.edit(content=message_content, embed=embed)
        except Exception as e:
            # Fallback in case editing fails (e.g. some discord.py older version constraints)
            await processing_msg.delete()
            if files:
                await ctx.send(content=message_content, embed=embed, files=files)
            else:
                await ctx.send(content=message_content, embed=embed)
