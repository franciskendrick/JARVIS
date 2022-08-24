from utils import Colors
from discord.ext import commands
import discord

commands_description = {
    "~sched": "Returns your schedule for today.",
    "~fsched": "Returns your full schedule.",
    "~next": "Returns the next class you will be attending."
}


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
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
        for command, description in commands_description.items():
            commands_text += f"`{command}`: {description}"
            commands_text += "\n"
        else:
            embed.add_field(
                name=":gear: __Commands:__",
                value=commands_text)

        # Send
        await ctx.send(embed=embed)


# Setup
def setup(bot):
    bot.add_cog(Help(bot))
