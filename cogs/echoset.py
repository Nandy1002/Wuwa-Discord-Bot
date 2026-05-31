import os
from datetime import datetime

import discord
from discord.ext import commands

from core.utils import resolve_asset_path
from core.image_gen import generate_echoset_table_image


class EchoSetPaginator(discord.ui.View):
    def __init__(self, echosets, ctx):
        super().__init__(timeout=120)
        self.echosets = echosets
        self.ctx = ctx
        self.per_page = 10
        self.total_pages = max(1, (len(echosets) + self.per_page - 1) // self.per_page)
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_pages - 1

    async def generate_page(self):
        start_idx = self.current_page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.echosets))
        
        page_echosets = self.echosets[start_idx:end_idx]
        
        image_buffer = generate_echoset_table_image(
            page_echosets, 
            self.current_page + 1, 
            self.total_pages, 
            resolve_asset_path
        )
        
        file = discord.File(fp=image_buffer, filename="table.png")
        
        embed = discord.Embed(
            title="Echo Sets List",
            color=discord.Color.blurple()
        )
        embed.set_image(url="attachment://table.png")
        
        try:
            avatar_url = self.ctx.author.display_avatar.url
        except Exception:
            avatar_url = None
        embed.set_footer(text=f'Requested by {self.ctx.author.display_name}', icon_url=avatar_url)
        
        return embed, file

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary, custom_id='prev_btn')
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
            
        self.current_page -= 1
        self.update_buttons()
        embed, file = await self.generate_page()
        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary, custom_id='next_btn')
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
            
        self.current_page += 1
        self.update_buttons()
        embed, file = await self.generate_page()
        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)


class EchoSetCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='echoset', description='Show details about an echo set by ID or Name.')
    async def echoset(self, ctx, *, query: str = None):
        """Show details about an echo set by ID or Name."""
        if not query:
            await ctx.send(f'Please use `!!echoset <id_or_name>`. Or use `!!list echoset` to browse them all.')
            return

        query_lower = query.strip().lower()
        echosets = self.bot.data_manager.echosets
        
        # Search by key (ID) or name
        echoset_obj = None
        if query_lower in echosets:
            echoset_obj = echosets[query_lower]
        else:
            query_norm = query_lower.replace('_', ' ')
            # Exact or partial name match
            partial_matches = []
            for es in echosets.values():
                if es.name:
                    name_norm = es.name.lower().replace('_', ' ')
                    if name_norm == query_norm:
                        echoset_obj = es
                        break
                    elif query_norm in name_norm:
                        partial_matches.append(es)
            
            if not echoset_obj and partial_matches:
                echoset_obj = partial_matches[0]
        
        if not echoset_obj:
            await ctx.send(f'Echo set not found. Use `!!list echoset` to see all available sets.')
            return

        embed = discord.Embed(
            title=f"{echoset_obj.name or echoset_obj.key.title()} (ID: {echoset_obj.key})",
            description=echoset_obj.description or '',
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        )

        files = []
        if echoset_obj.icon:
            icon_path = resolve_asset_path(echoset_obj.icon)
            if icon_path:
                filename = 'echoset_icon' + os.path.splitext(icon_path)[1]
                files.append(discord.File(icon_path, filename=filename))
                embed.set_thumbnail(url=f'attachment://{filename}')
            else:
                embed.set_thumbnail(url=echoset_obj.icon)

        if echoset_obj.set_bonus:
            embed.add_field(
                name='Set Bonus',
                value=echoset_obj.format_set_bonus(),
                inline=False
            )
            
        if getattr(echoset_obj, 'pieces', None):
            embed.add_field(
                name='Echoes in Set',
                value=echoset_obj.format_pieces(),
                inline=False
            )

        try:
            avatar_url = ctx.author.display_avatar.url
        except Exception:
            avatar_url = None
        embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=avatar_url)

        message_content = f'Here is the information for {echoset_obj.name or echoset_obj.key.title()}, {ctx.author.mention}.'
        if files:
            await ctx.send(content=message_content, embed=embed, files=files)
        else:
            await ctx.send(content=message_content, embed=embed)


