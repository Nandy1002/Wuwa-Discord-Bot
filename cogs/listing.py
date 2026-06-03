import discord
from discord.ext import commands
from typing import Optional

from cogs.echoset import EchoSetPaginator
from cogs.weapon import WeaponPaginator
from cogs.character import CharacterPaginator

class ListingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name='list')
    async def list_group(self, ctx):
        """Group of commands to list various data."""
        pass

    @list_group.command(name='echoset', description='Show a paginated list of all echo sets.')
    async def list_echoset(self, ctx):
        """Show a paginated list of all echo sets."""
        echosets = list(self.bot.data_manager.echosets.values())
        if not echosets:
            await ctx.send("No echo sets available.")
            return
            
        view = EchoSetPaginator(echosets, ctx)
        embed, file = await view.generate_page()
        
        await ctx.send(embed=embed, file=file, view=view)

    @list_group.command(name='weapon', description='Show a paginated list of all weapons.')
    async def list_weapon(self, ctx, weapon_type: Optional[str] = None, rarity: Optional[str] = None):
        """Show a paginated list of all weapons. Optionally filter by type and rarity."""
        all_weapons = list(self.bot.data_manager.weapons.values())
            
        if not all_weapons:
            await ctx.send("No weapons found.")
            return
            
        view = WeaponPaginator(all_weapons, ctx, weapon_type=weapon_type, rarity=rarity)
        embed, file = await view.generate_page()
        
        if file:
            await ctx.send(embed=embed, file=file, view=view)
        else:
            await ctx.send(embed=embed, view=view)

    @list_group.command(name='character', description='Show a paginated list of all characters.')
    async def list_character(self, ctx, attribute: Optional[str] = None, weapon_type: Optional[str] = None, rarity: Optional[str] = None):
        """Show a paginated list of all characters. Optionally filter by attribute, weapon type, and rarity."""
        all_chars = list(self.bot.data_manager.characters.values())
            
        if not all_chars:
            await ctx.send("No characters found.")
            return
            
        view = CharacterPaginator(all_chars, ctx, attribute=attribute, weapon_type=weapon_type, rarity=rarity)
        embed, file = await view.generate_page()
        
        if file:
            await ctx.send(embed=embed, file=file, view=view)
        else:
            await ctx.send(embed=embed, view=view)
