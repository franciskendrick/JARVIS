from utils import round_time
from utils import get_restday_message
from utils import get_schedule_embed
from utils.schedule import get_day
from utils.schedule import get_learningtype
from utils import get_nextclass_title
from utils import get_nextclass_embed
from disnake.ext import commands
import disnake
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
            "online": ["Monday", "Wednesday", "Friday"],
            "face-to-face": ["Tuesday", "Thursday"]
        }

        # Responses
        with open(f"{resources_path}/responses.json") as json_file:
            self.responses = json.load(json_file)

        # Errors
        with open(f"{resources_path}/errors.json") as json_file:
            self.errors = json.load(json_file)

    # Normal command/s
    @commands.command(
        name="sched", 
        usage="<day> <learning_type>",
        description="Shows your schedule for today or for your given day.",
        help="""
            `<day>`: The day of the schedule you want to see. *(`sunday` / `monday` / `tuesday` / `wednesday` / `thursday` / `friday` / `saturday`)*
            `<learning_type>`: The learning type of the schedule you want to see. *(`synchronous` / `asynchronous` / `all`)*
        """
    )
    async def sched(self, ctx, day=None, learning_type=None):
        await self.handle_sched(ctx, day, learning_type)

    @commands.command(
        name="fsched",
        description="Shows your full schedule.",
        help="`<learning_type>`: The learning type of the full schedule you want to see. *(`synchronous` / `asynchronous` / `all`)*"
    )
    async def fsched(self, ctx, learning_type="synchronous"):
        await self.handle_fsched(ctx, learning_type)

    @commands.command(
        name="next",
        description="Shows the next class you will be attending.")
    async def _next(self, ctx):
        await self.handle_next(ctx)

    # Slash command/s
    @commands.slash_command(name="sched")
    async def _sched(
        self,
        inter: disnake.AppCmdInter,
        day: str = commands.Param(
            default=None, 
            choices=[
                "sunday", 
                "monday", 
                "tuesday", 
                "wednesday", 
                "thursday", 
                "friday", 
                "saturday"
            ]
        ),
        learning_type: str = commands.Param(
            default=None,
            choices=[
                "synchronous",
                "asynchronous",
                "all"
            ]
        )
    ):
        """
        Shows your schedule for today or for your given day.

        Parameters
        ----------
        day: The day of the schedule you want to see.
        learning_type: The learning type of the schedule you want to see.
        """

        await self.handle_sched(inter, day, learning_type)

    @commands.slash_command(name="fsched")
    async def _fsched(
        self, 
        inter: disnake.AppCmdInter,
        learning_type: str = commands.Param(
            default="synchronous",
            choices=[
                "synchronous",
                "asynchronous",
                "all"
            ]
        )
    ):
        """
        Shows your full schedule.

        Parameters
        ----------
        learning_type: The learning type of the full schedule you want to see.
        """

        await self.handle_fsched(inter, learning_type)

    @commands.slash_command(name="next")
    async def s_next(self, inter: disnake.AppCmdInter):
        """
        Shows the next class you will be attending.
        """
        
        await self.handle_next(inter)

    # Handle command/s
    async def handle_sched(self, ctx, given_day, given_learningtype):
        # Get variables
        day, with_input = get_day(given_day)
        learning_type = get_learningtype(given_learningtype)

        # Give schedule
        if day != None and learning_type != None:  # get schedule
            if day in self.days["online"]:  # give schedule
                if learning_type == "all":  # give all schedules
                    for new_learningtype in ["synchronous", "asynchronous"]:
                        embed = get_schedule_embed(day, new_learningtype)
                        await ctx.send(embed=embed)
                else:  # give a/synchronous schedule
                    embed = get_schedule_embed(day, learning_type)
                    await ctx.send(embed=embed)
            else:  # give rest day message
                input_type = "with_input" if with_input else "no_input"
                message = get_restday_message(ctx, day, input_type)
                await ctx.send(message)
        else:  # give error
            message = random.choice(self.errors["WrongArgumentGiven"])
            message = message.replace("__user__", f"<@{ctx.author.id}>")
            await ctx.send(message)

    async def handle_fsched(self, ctx, given_learningtype):
        for day in self.days["online"]:
            if given_learningtype == "all":  # give all schedules
                for learning_type in ["synchronous", "asynchronous"]:
                    embed = get_schedule_embed(day, learning_type)
                    await ctx.send(embed=embed)
            else:  # give a/synchronous schedule
                embed = get_schedule_embed(day, given_learningtype)
                await ctx.send(embed=embed)

    async def handle_next(self, ctx):
        tz_manila = pytz.timezone("Asia/Manila")
        now = datetime.datetime.now(tz_manila)

        # Get current day and time
        current_day = now.strftime("%A")
        current_time = round_time(now.strftime("%H:%M:%S"))

        # Give next class
        if current_day in self.days["online"]:
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
def setup(bot):
    bot.add_cog(School(bot))
