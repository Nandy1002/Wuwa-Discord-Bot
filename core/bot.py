import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from core.data_manager import DataManager
from cogs.build import BuildCog
from cogs.misc import MiscCog


class ShorekeeperBot(commands.Bot):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, command_prefix='!', intents=None):
        if hasattr(self, 'initialized') and self.initialized:
            return

        print('[Bot] Initializing ShorekeeperBot...', flush=True)
        load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        self.guild_id = os.getenv('DISCORD_GUILD_ID')
        
        print(f'[Bot] Token loaded: {bool(token)}', flush=True)
        print(f'[Bot] Guild ID loaded: {bool(self.guild_id)}', flush=True)
        
        if not token:
            raise RuntimeError('DISCORD_TOKEN not found in environment variables.')

        self.token = token
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        print(f'[Bot] Loading data from: {data_path}', flush=True)
        self.data_manager = DataManager(data_path)
        self.data_manager.load()
        print('[Bot] Data loaded successfully', flush=True)

        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents)
        self.initialized = True
        print('[Bot] Initialization complete', flush=True)

    async def setup_hook(self):
        await self.add_cog(BuildCog(self))
        await self.add_cog(MiscCog(self))
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
        # For GitHub Actions: add timeout if in CI environment
        if os.getenv('CI') == 'true':
            async def shutdown_after_connection():
                await asyncio.sleep(5)  # Wait 5 seconds to confirm connection
                await self.close()
            
            self.loop.create_task(shutdown_after_connection())
        
        super().run(self.token)
