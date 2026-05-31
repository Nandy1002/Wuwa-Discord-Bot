import os
from datetime import datetime

import discord
from discord.ext import commands

from core.utils import resolve_asset_path
from core.image_gen import generate_weapon_table_image


class WeaponPaginator(discord.ui.View):
    def __init__(self, all_weapons, ctx, weapon_type=None, rarity=None):
        super().__init__(timeout=120)
        self.all_weapons = all_weapons
        self.ctx = ctx
        self.per_page = 10
        self.current_page = 0
        
        # Handle rarity string matching like the listing command
        if rarity and rarity.lower() in ['3', '4', '5']:
            rarity = rarity.lower() + '-star'
            
        # Capitalize appropriately or use "All"
        self.selected_type = weapon_type.title() if weapon_type else "All"
        self.selected_rarity = rarity.title() if rarity else "All"
        
        # Fix exact casing for 5-Star, etc.
        if self.selected_rarity != "All" and "star" in self.selected_rarity.lower():
            parts = self.selected_rarity.split('-')
            if len(parts) == 2:
                self.selected_rarity = f"{parts[0]}-Star"
        
        self.update_state()

    def update_state(self):
        self.filtered_weapons = [
            w for w in self.all_weapons
            if (self.selected_type == "All" or (w.type and w.type.lower() == self.selected_type.lower()))
            and (self.selected_rarity == "All" or (w.rarity and w.rarity.lower() == self.selected_rarity.lower()))
        ]
        
        self.total_pages = max(1, (len(self.filtered_weapons) + self.per_page - 1) // self.per_page)
        
        if self.current_page >= self.total_pages:
            self.current_page = self.total_pages - 1
            
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_pages - 1

    async def generate_page(self):
        if not self.filtered_weapons:
            embed = discord.Embed(
                title="Weapons List",
                description="No weapons found matching the selected filters.",
                color=discord.Color.red()
            )
            return embed, None

        start_idx = self.current_page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.filtered_weapons))
        
        page_weapons = self.filtered_weapons[start_idx:end_idx]
        
        image_buffer = generate_weapon_table_image(
            page_weapons, 
            self.current_page + 1, 
            self.total_pages, 
            resolve_asset_path
        )
        
        file = discord.File(fp=image_buffer, filename="weapon_table.png")
        
        embed = discord.Embed(
            title="Weapons List",
            color=discord.Color.gold()
        )
        embed.set_image(url="attachment://weapon_table.png")
        
        try:
            avatar_url = self.ctx.author.display_avatar.url
        except Exception:
            avatar_url = None
        embed.set_footer(text=f'Requested by {self.ctx.author.display_name}', icon_url=avatar_url)
        
        return embed, file

    @discord.ui.select(
        placeholder="Filter by Type",
        options=[
            discord.SelectOption(label="All Types", value="All"),
            discord.SelectOption(label="Broadblade", value="Broadblade"),
            discord.SelectOption(label="Gauntlets", value="Gauntlets"),
            discord.SelectOption(label="Pistols", value="Pistols"),
            discord.SelectOption(label="Rectifier", value="Rectifier"),
            discord.SelectOption(label="Sword", value="Sword"),
        ],
        row=0
    )
    async def type_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
            return
            
        self.selected_type = select.values[0]
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
            discord.SelectOption(label="3-Star", value="3-Star"),
            discord.SelectOption(label="2-Star", value="2-Star"),
            discord.SelectOption(label="1-Star", value="1-Star"),
        ],
        row=1
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

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary, custom_id='prev_btn', row=2)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
            
        self.current_page -= 1
        self.update_state()
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary, custom_id='next_btn', row=2)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
            
        self.current_page += 1
        self.update_state()
        embed, file = await self.generate_page()
        attachments = [file] if file else []
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=self)


class WeaponCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='weapon', description='Show details about a weapon by ID or Name.')
    async def weapon(self, ctx, *, query: str = None):
        """Show details about a weapon by ID or Name."""
        if not query:
            await ctx.send(f'Please use `!!weapon <id_or_name>`. Or use `!!list weapon` to browse them all.')
            return

        query_lower = query.strip().lower()
        weapons = self.bot.data_manager.weapons
        
        # Search by key (ID) or name
        weapon_obj = None
        if query_lower in weapons:
            weapon_obj = weapons[query_lower]
        else:
            query_norm = query_lower.replace('_', ' ')
            partial_matches = []
            for w in weapons.values():
                if w.name:
                    name_norm = w.name.lower().replace('_', ' ')
                    if name_norm == query_norm:
                        weapon_obj = w
                        break
                    elif query_norm in name_norm:
                        partial_matches.append(w)
            
            if not weapon_obj and partial_matches:
                weapon_obj = partial_matches[0]
        
        if not weapon_obj:
            await ctx.send(f'Weapon not found. Use `!!list weapon` to see all available weapons.')
            return

        embed = discord.Embed(
            title=f"{weapon_obj.name or weapon_obj.key.title()} (ID: {weapon_obj.key})",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )

        files = []
        if weapon_obj.icon:
            icon_path = resolve_asset_path(weapon_obj.icon)
            if icon_path:
                filename = 'weapon_icon' + os.path.splitext(icon_path)[1]
                files.append(discord.File(icon_path, filename=filename))
                embed.set_thumbnail(url=f'attachment://{filename}')
            else:
                embed.set_thumbnail(url=weapon_obj.icon)

        # Build description
        desc_lines = []
        if weapon_obj.rarity: desc_lines.append(f"**Rarity:** {weapon_obj.rarity}")
        if weapon_obj.type: desc_lines.append(f"**Type:** {weapon_obj.type}")
        if weapon_obj.base_stat: desc_lines.append(f"**Base Stat:** {weapon_obj.base_stat}")
        if weapon_obj.sub_stat: desc_lines.append(f"**Sub Stat:** {weapon_obj.sub_stat}")
        
        if desc_lines:
            embed.description = "\n".join(desc_lines)

        if weapon_obj.passive:
            embed.add_field(
                name='Passive',
                value=weapon_obj.passive,
                inline=False
            )

        try:
            avatar_url = ctx.author.display_avatar.url
        except Exception:
            avatar_url = None
        embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=avatar_url)

        message_content = f'Here is the information for {weapon_obj.name or weapon_obj.key.title()}, {ctx.author.mention}.'
        if files:
            await ctx.send(content=message_content, embed=embed, files=files)
        else:
            await ctx.send(content=message_content, embed=embed)
