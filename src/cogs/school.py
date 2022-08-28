from utils import round_time
from utils import get_restday_message
from utils import get_schedule_embed
from utils import get_nextclass_title
from utils import get_nextclass_embed
from disnake.ext import commands
import datetime
import random
import pytz
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "resources"
        )
    )


class School(commands.Cog):
    # Initialize
    def __init__(self, bot):
        self.bot = bot

        # Days
        self.days = {
            "synchronous": ["Monday", "Wednesday", "Friday"],
            "asynchronous": ["Tuesday", "Thursday", "Saturday"]
        }

        # Aliases
        with open(f"{resources_path}/aliases.json") as json_file:
            self.aliases = json.load(json_file)

        # Responses
        with open(f"{resources_path}/responses.json") as json_file:
            self.responses = json.load(json_file)

        # Errors
        with open(f"{resources_path}/errors.json") as json_file:
            self.errors = json.load(json_file)

    # Commands
    @commands.command( 
        name="sched", 
        usage="<given_day>",
        description="Returns your schedule for today or for your given day.",
        help="`<given_day>`: The day of the schedule you want to see. (`sunday` / `monday` / `tuesday` / `wednesday` / `thursday` / `friday` / `saturday`)")
    async def sched(self, ctx, given_day=None):
        # Get day
        if given_day == None:  # no argument given
            with_input = False

            # Get current day
            timezone_manila = pytz.timezone("Asia/Manila")
            day = datetime.datetime.now(timezone_manila).strftime("%A")
        else:  # has an argument
            with_input = True

            # Get day
            day = None
            for key, aliases in self.aliases.items():
                if given_day.lower() in aliases:
                    day = key
                    break

        # Give schedule
        if day != None:  # give schedule
            if day in self.days["synchronous"]:
                embed = get_schedule_embed(day)
                await ctx.send(embed=embed)
            else:
                input_type = "with_input" if with_input else "no_input"
                message = get_restday_message(ctx, day, input_type)
                await ctx.send(message)
        else:  # give schedule
            message = random.choice(self.errors["WrongArgumentGiven"])
            message = message.replace("__user__", f"<@{ctx.author.id}>")

            await ctx.send(message)

    @commands.command(
        name="fsched",
        description="Returns your full schedule.")
    async def fsched(self, ctx):
        for day in self.days["synchronous"]:
            embed = get_schedule_embed(day)
            await ctx.send(embed=embed)

    @commands.command(
        name="next",
        description="Returns the next class you will be attending.")
    async def next(self, ctx):
        tz_manila = pytz.timezone("Asia/Manila")
        now = datetime.datetime.now(tz_manila)

        # Get current day and time
        current_day = now.strftime("%A")
        current_time = round_time(now.strftime("%H:%M:%S"))

        # Give next class
        if current_day in self.days["synchronous"]:
            title, time = get_nextclass_title(current_time)
            if (title, time) != (None, None):  # class hasn't ended, hence, there's a class next
                embed = get_nextclass_embed(title, current_day, time)
                await ctx.send(embed=embed)
            else:  # class has ended, hence, congratulate the student
                message = random.choice(self.responses["class_finished"])
                message = message.replace("__user__", f"<@{ctx.author.id}>")
                await ctx.send(message)
        else:
            message = get_restday_message(ctx, current_day, "no_input")
            await ctx.send(message)


# Setup
async def setup(bot):
    await bot.add_cog(School(bot))
