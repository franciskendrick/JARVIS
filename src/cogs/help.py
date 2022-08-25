from utils import get_fullhelp_embed
from utils import get_commandinfo_embed
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, command_name=None):
        if command_name == None:  # send the full help message
            embed = get_fullhelp_embed(ctx, self.bot)
        else:  # send the infomation about the command given
            embed = get_commandinfo_embed(ctx, self.bot, command_name)

        # Send
        await ctx.send(embed=embed)


# Setup
def setup(bot):
    bot.add_cog(Help(bot))
