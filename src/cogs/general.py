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


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Errors
        with open(f"{resources_path}/errors.json") as json_file:
            self.errors = json.load(json_file)

    @commands.Cog.listener()
    async def on_ready(self):
        print("{0.user} has logged in.".format(self.bot))
        await self.bot.change_presence(status=disnake.Status.do_not_disturb)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        messages_list = None
        if isinstance(error, commands.CommandNotFound):
            messages_list = self.errors["CommandNotFound"]

        if messages_list != None:  # didn't recognize the error
            # Get message from messages list
            message = random.choice(messages_list)

            # Replace message's key words
            message = message.replace("__user__", f"<@{ctx.author.id}>")

            # Send
            await ctx.send(message)


def setup(bot):
    bot.add_cog(General(bot))