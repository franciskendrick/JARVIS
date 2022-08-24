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

        # Errors
        with open(f"{resources_path}/errors.json") as json_file:
            self.errors = json.load(json_file)

    @commands.Cog.listener()
    async def on_ready(self):
        print("{0.user} has logged in.".format(self.bot))
        await self.bot.change_presence(status=discord.Status.do_not_disturb)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            messages_list = self.errors["CommandNotFound"]

        # Get message from messages list
        message = random.choice(messages_list)

        # Replace message's key words
        message = message.replace("__user__", f"<@{ctx.author.id}>")
        message = message.replace("__creator__", f"<@{CREATOR_ID}>")

        # Send
        await ctx.send(message)


def setup(bot):
    bot.add_cog(General(bot))
