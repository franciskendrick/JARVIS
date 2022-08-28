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

    @commands.command(
        name="help",
        usage="<command>",
        description="Show all the commands.",
        help="`<command>`: The name of the command you want more information about."
    )
    async def help(self, ctx, command_name=None):
        if command_name == None:  # send the full help message
            embed = get_fullhelp_embed(ctx, self.bot)
        else:  # send the infomation about the command given
            embed = get_commandinfo_embed(ctx, self.bot, command_name)

        # Send
        await ctx.send(embed=embed)

    @commands.slash_command(name="help")
    async def _help(
        self,
        inter: discord.AppCmdInter,
        command_name = commands.Param(
            default=None, 
            name="command", 
            autocomplete=autocomplete_commands)
    ):
        if command_name == None:  # send the full help message
            embed = get_fullhelp_embed(inter, self.bot)
        else:  # send the infomation about the command given
            embed = get_commandinfo_embed(inter, self.bot, command_name)

        # Send
        await inter.send(embed=embed)


# Setup
async def setup(bot):
    await bot.add_cog(Help(bot))
