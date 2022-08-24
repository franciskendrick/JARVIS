from utils import Colors
from discord.ext import commands
import discord


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, command_name=None):
        if command_name == None:  # send the full help message
            # Embed
            embed = discord.Embed(
                title="**Help Command**",
                color=discord.Color.from_rgb(*Colors.light_brown))
            
            # Set author
            embed.set_author(
                name=ctx.me, 
                icon_url=ctx.me.avatar_url)

            # Add description
            embed.description = "Use `~help [command]` to see more information about a command." 

            # Add field
            commands_text = ""
            for (name, command) in self.bot.all_commands.items():
                if name != "help":
                    commands_text += f"`~{name}`: {command.description}"
                    commands_text += "\n"
            else:
                embed.add_field(
                    name=":gear: __Commands:__",
                    value=commands_text)

            # Send
            await ctx.send(embed=embed)
        else:  # send the infomation about the command given
            command = self.bot.all_commands.get(command_name)

            # Embed
            embed = discord.Embed(
                title=f"**Command __{command_name}__**",
                color=discord.Color.from_rgb(*Colors.light_brown))

            # Set author
            embed.set_author(
                name=ctx.me, 
                icon_url=ctx.me.avatar_url)

            # Add how to use the command
            usage = command.usage
            embed.add_field(
                name="How to use:",
                value=f"`~{command_name}{(' ' + usage) if usage else ''}`")

            # Add command's description
            description = command.description
            embed.add_field(
                name="Description:", 
                value=description,
                inline=False)

            # Add command's parameters
            parameters = command.help
            embed.add_field(
                name="Parameter/s:",
                value=parameters)

            # Send
            await ctx.send(embed=embed)


# Setup
def setup(bot):
    bot.add_cog(Help(bot))
