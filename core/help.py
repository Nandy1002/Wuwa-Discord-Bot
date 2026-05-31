import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Shows help about the bot, a command, or a category'
        })

    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title='Bot Commands',
            description='Here is a list of all available commands. Use `!!help <command>` for more information.',
            color=discord.Color.blurple()
        )
        
        embed.set_image(url="https://cdn.discordapp.com/attachments/1292845515893112875/1510652472811716718/sk_intro.gif?ex=6a1d9840&is=6a1c46c0&hm=75f44022db9d57a6443fef63691ba86a24a4b41cbc7211b90c9f0e896e105a1c&")

        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, 'qualified_name', 'No Category')
                # Format commands nicely
                commands_text = ''
                for cmd in filtered:
                    commands_text += f'`{cmd.name}` - {cmd.short_doc or "No description"}\n'
                
                if commands_text:
                    embed.add_field(name=cog_name, value=commands_text, inline=False)
        
        # Add a footer
        embed.set_footer(text=f'Type {self.context.clean_prefix}help <command> for more info on a command.')
        
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f'{cog.qualified_name} Commands',
            description=cog.description or 'No description provided.',
            color=discord.Color.blurple()
        )

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or 'No description', inline=False)

        embed.set_footer(text=f'Type {self.context.clean_prefix}help <command> for more info on a command.')
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=self.get_command_signature(command),
            description=command.help or 'No description provided.',
            color=discord.Color.blurple()
        )
        
        if command.aliases:
            embed.add_field(name='Aliases', value=', '.join(command.aliases), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(
            title=self.get_command_signature(group),
            description=group.help or 'No description provided.',
            color=discord.Color.blurple()
        )

        if group.aliases:
            embed.add_field(name='Aliases', value=', '.join(group.aliases), inline=False)

        filtered = await self.filter_commands(group.commands, sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or 'No description', inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
