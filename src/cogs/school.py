from operator import sub
from utils import Colors
from discord.ext import commands
import discord
import json
import os
import datetime
import random
import pytz

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

        # Embed colors
        self.colors = {
            "Monday": Colors.red,
            "Tuesday": Colors.red,
            "Wednesday": Colors.yellow,
            "Thursday": Colors.yellow,
            "Friday": Colors.green,
            "Saturday": Colors.green
        }

        # Aliases
        with open(f"{resources_path}/aliases.json") as json_file:
            self.aliases = json.load(json_file)

        # School
        with open(f"{resources_path}/school.json") as json_file:
            school = json.load(json_file)
            self.synchronous_data = school["synchronous"]

        # Responses
        with open(f"{resources_path}/responses.json") as json_file:
            self.responses = json.load(json_file)

    # Commands
    @commands.command()
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

        # Check for errors
        if day == None:  # error
            pass
        else:  # give schedule
            if day in self.days["synchronous"]:
                embed = self.get_schedule_embed(day)
                await ctx.send(embed=embed)
            else:
                input_type = "with_input" if with_input else "no_input"
                message = self.get_resetday_message(ctx, day, input_type)
                await ctx.send(message)

    @commands.command()
    async def fsched(self, ctx):
        pass

    @commands.command()
    async def next(self, ctx):
        pass

    # Functions
    def get_schedule_embed(self, day):
        color = self.colors[day]
        embed = discord.Embed(
            title=f"{day}:",
            color=discord.Color.from_rgb(*color))

        # Write to embed
        sched = self.synchronous_data["schedule"][day]
        for time in sched:
            # Get subjects and links
            subject = sched[time]
            link = self.synchronous_data["links"][subject]
            
            # Get time
            start_time, end_time = time.split(" - ")
            start_time = self.get_standard_time(start_time)
            end_time = self.get_standard_time(end_time)

            time = f"{start_time} - {end_time}"

            # Add field
            embed.add_field(
                name=f"__{subject}__ {time}:",
                value=link,
                inline=False
            )

        # Return embed
        return embed

    def get_resetday_message(self, ctx, day, input_type):
        # Get message
        message = random.choice(self.responses["rest"][input_type])
        message = message.replace("__user__", f"<@{ctx.author.id}>")
        message = message.replace("__day__", day)

        # Return message
        return message

    def get_standard_time(self, time):
        # Convert time into a datetime object
        time = datetime.datetime.strptime(time, "%H:%M:%S")

        # Get standard time
        time = time.time()
        standard_time = time.strftime("%I:%M")

        # Get meridian
        meridian = "PM" if time.hour >= 12 else "AM"

        # Return
        return f"{standard_time} {meridian}"


# Setup
def setup(bot):
    bot.add_cog(School(bot))
