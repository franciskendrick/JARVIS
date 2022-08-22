from discord.ext import commands
import discord
import os
import datetime
import pytz


class School(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Days
        self.days = {
            "synchronous": ["Monday", "Wednesday", "Friday"],
            "asynchronous": ["Tuesday", "Thursday", "Saturday"],
            "rest": ["Sunday"]
        }

    @commands.command()
    async def sched(self, ctx, given_day=None):
        pass

    @commands.command()
    async def fsched(self, ctx):
        pass

    @commands.command()
    async def next(self, ctx):
        pass


# Setup
def setup(bot):
    bot.add_cog(School(bot))
