from utils import get_fullhelp_embed
from utils import get_commandinfo_embed
from disnake.ext import commands
import disnake as discord


async def autocomplete_commands(inter: discord.AppCmdInter, user_input: str):
    commands = []
    for cmd in inter.bot.all_slash_commands.values():
        commands.append(cmd.name)

    return [cmd for cmd in commands if user_input.lower() in cmd.lower()][:25]
    

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        inter: discord.AppCmdInter,
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
        if command_name == None:  # send the full help message
            embed = get_fullhelp_embed(ctx, self.bot)
        else:  # send the infomation about the command given
            embed = get_commandinfo_embed(ctx, self.bot, command_name)

        # Send
        await ctx.send(embed=embed)


# Setup
async def setup(bot):
    await bot.add_cog(Help(bot))
