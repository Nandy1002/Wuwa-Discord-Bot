import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from core.data_manager import DataManager
from core.help import CustomHelpCommand
from cogs.character import CharacterCog
from cogs.misc import MiscCog
from cogs.echoset import EchoSetCog
from cogs.weapon import WeaponCog
from cogs.listing import ListingCog


class ShorekeeperBot(commands.Bot):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, command_prefix='!!', intents=None):
        if hasattr(self, 'initialized') and self.initialized:
            return

        load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        self.guild_id = os.getenv('DISCORD_GUILD_ID')
        if not token:
            raise RuntimeError('DISCORD_TOKEN not found in environment variables.')

        self.token = token
        self.data_manager = DataManager(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.data_manager.load()

        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents, help_command=CustomHelpCommand())
        self.initialized = True

    async def setup_hook(self):
        await self.add_cog(CharacterCog(self))
        await self.add_cog(MiscCog(self))
        await self.add_cog(EchoSetCog(self))
        await self.add_cog(WeaponCog(self))
        await self.add_cog(ListingCog(self))
        try:
            await self.tree.sync()
            print('Synced global application commands.')
        except Exception as exc:
            print(f'Failed to sync app commands: {exc}')

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def run_bot(self):
        super().run(self.token)
