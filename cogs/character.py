import os
from datetime import datetime

import discord
from discord.ext import commands

from core.utils import format_list, format_teams, resolve_asset_path, get_mention_text
from core.image_generator import generate_materials_image
from core.image_gen import generate_character_table_image


class CharacterPaginator(discord.ui.View):
    def __init__(self, all_characters, ctx, attribute=None, weapon_type=None, rarity=None):
        super().__init__(timeout=120)
        self.all_characters = all_characters
        self.ctx = ctx
        self.per_page = 10
        self.current_page = 0
        
        if rarity and rarity.lower() in ['4', '5']:
            rarity = rarity.lower() + '-star'
            
        self.selected_attribute = attribute.title() if attribute else "All"
        self.selected_weapon = weapon_type.title() if weapon_type else "All"
        self.selected_rarity = rarity.title() if rarity else "All"
        
        if self.selected_rarity != "All" and "star" in self.selected_rarity.lower():
            parts = self.selected_rarity.split('-')
            if len(parts) == 2:
                self.selected_rarity = f"{parts[0]}-Star"
        
        self.update_state()

    def update_state(self):
        self.filtered_characters = [
            c for c in self.all_characters
            if (self.selected_attribute == "All" or (c.element and c.element.lower() == self.selected_attribute.lower()))
            and (self.selected_weapon == "All" or (c.weapon_type and c.weapon_type.lower() == self.selected_weapon.lower()))
            and (self.selected_rarity == "All" or (c.rarity and str(c.rarity) in self.selected_rarity))
        ]
        
        self.total_pages = max(1, (len(self.filtered_characters) + self.per_page - 1) // self.per_page)
        
        if self.current_page >= self.total_pages:
            self.current_page = self.total_pages - 1
            
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_pages - 1

    async def generate_page(self):
        if not self.filtered_characters:
            embed = discord.Embed(
                title="Characters List",
                description="No characters found matching the selected filters.",
                color=discord.Color.red()
            )
            return embed, None

        start_idx = self.current_page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.filtered_characters))
        
        page_chars = self.filtered_characters[start_idx:end_idx]
        
        image_buffer = generate_character_table_image(
            page_chars, 
            self.current_page + 1, 
            self.total_pages, 
            resolve_asset_path
        )
        
        file = discord.File(fp=image_buffer, filename="character_table.png")
        
        embed = discord.Embed(
            title="Characters List",
            color=discord.Color.gold()
        )
        embed.set_image(url="attachment://character_table.png")
        
        try:
            avatar_url = self.ctx.author.display_avatar.url
        except Exception:
            avatar_url = None
        embed.set_footer(text=f'Requested by {self.ctx.author.display_name}', icon_url=avatar_url)
        
        return embed, file

    @discord.ui.select(
        placeholder="Filter by Attribute",
        options=[
            discord.SelectOption(label="All Attributes", value="All"),
            discord.SelectOption(label="Fusion", value="Fusion"),
            discord.SelectOption(label="Glacio", value="Glacio"),
            discord.SelectOption(label="Aero", value="Aero"),
            discord.SelectOption(label="Electro", value="Electro"),
            discord.SelectOption(label="Spectro", value="Spectro"),
            discord.SelectOption(label="Havoc", value="Havoc"),
        ],
        row=0
    )
    async def attribute_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
            return
            
        self.selected_attribute = select.values[0]
        self.current_page = 0
        self.update_state()
        
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)

    @discord.ui.select(
        placeholder="Filter by Weapon",
        options=[
            discord.SelectOption(label="All Weapons", value="All"),
            discord.SelectOption(label="Broadblade", value="Broadblade"),
            discord.SelectOption(label="Gauntlets", value="Gauntlets"),
            discord.SelectOption(label="Pistols", value="Pistols"),
            discord.SelectOption(label="Rectifier", value="Rectifier"),
            discord.SelectOption(label="Sword", value="Sword"),
        ],
        row=1
    )
    async def weapon_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
            return
            
        self.selected_weapon = select.values[0]
        self.current_page = 0
        self.update_state()
        
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)

    @discord.ui.select(
        placeholder="Filter by Rarity",
        options=[
            discord.SelectOption(label="All Rarities", value="All"),
            discord.SelectOption(label="5-Star", value="5-Star"),
            discord.SelectOption(label="4-Star", value="4-Star"),
        ],
        row=2
    )
    async def rarity_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
            return
            
        self.selected_rarity = select.values[0]
        self.current_page = 0
        self.update_state()
        
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary, custom_id='prev_btn', row=3)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
            
        self.current_page -= 1
        self.update_state()
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary, custom_id='next_btn', row=3)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
            
        self.current_page += 1
        self.update_state()
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)

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

        # Check for numeric ID match
        if not character_obj and key.isdigit():
            numeric_id = int(key)
            for c in self.bot.data_manager.characters.values():
                if getattr(c, 'numeric_id', None) == numeric_id:
                    character_obj = c
                    break

        # Fuzzy matching fallback
        if not character_obj:
            import difflib
            candidates = {k: k for k in self.bot.data_manager.characters.keys()}
            for k, c in self.bot.data_manager.characters.items():
                candidates[c.name.lower()] = k
            
            matches = difflib.get_close_matches(key, list(candidates.keys()), n=1, cutoff=0.4)
            if matches:
                matched_key = candidates[matches[0]]
                character_obj = self.bot.data_manager.get_character(matched_key)

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
