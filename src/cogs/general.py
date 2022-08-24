from discord.ext import commands
import discord
import random
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "resources"
        )
    )
    
CREATOR_ID = os.environ['CREATOR_ID']


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    async def on_command_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(General(bot))
