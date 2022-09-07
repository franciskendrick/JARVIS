from utils import get_fullhelp_embed, get_commandinfo_embed  # help module/s
from disnake.ext import commands
import disnake
import random
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "resources"
        )
    )


async def autocomplete_commands(inter: disnake.AppCmdInter, user_input: str):
    commands = get_commands(inter)
    return [cmd for cmd in commands if user_input.lower() in cmd.lower()][:25]


def get_commands(inter: disnake.AppCmdInter):
    commands = []
    for cmd in inter.bot.all_slash_commands.values():
        commands.append(cmd.name)

    return commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Errors
        with open(f"{resources_path}/errors.json") as json_file:
            self.errors = json.load(json_file)

    # Normal command/s
    @commands.command(
        name="help",
        usage="<command_name>",
        description="Show all the commands.",
        help="`<command_name>`: The name of the command you want more information about."
    )
    async def help(self, ctx, command_name=None):
        await self.handle_help(ctx, command_name)

    # Slash command/s
    @commands.slash_command(
        name="help", 
        description="Show all the commands.")
    async def _help(
        self,
        inter: disnake.AppCmdInter,
        command_name = commands.Param(
            default=None, 
            name="command_name", 
            autocomplete=autocomplete_commands)
    ):
        """
        Show all the commands.

        Parameters
        ----------
        command_name: The name of the command you want more information about.
        """

        await self.handle_help(inter, command_name)

    # Handle command/s
    async def handle_help(self, ctx, command_name):
        commands = get_commands(ctx)
        if command_name in commands:  # give help message
            if command_name == None:  # send the full help message
                embed = get_fullhelp_embed(ctx, self.bot)
            else:  # send the infomation about the command given
                embed = get_commandinfo_embed(ctx, self.bot, command_name)

            # Send
            await ctx.send(embed=embed)
        else:  # give error
            message = random.choice(self.errors["CommandNotFound"])
            message = message.replace("__user__", f"<@{ctx.author.id}>")
            await ctx.send(message)


# Setup
def setup(bot):
    bot.add_cog(Help(bot))
