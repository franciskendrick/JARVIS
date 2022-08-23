from utils import Colors
from utils import format_time
from utils import get_restday_message
from utils import get_schedule_embed
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

        # Errors
        with open(f"{resources_path}/errors.json") as json_file:
            self.errors = json.load(json_file)

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

    @commands.command()
    async def fsched(self, ctx):
        for day in self.days["synchronous"]:
            embed = get_schedule_embed(day)
            await ctx.send(embed=embed)

    @commands.command()
    async def next(self, ctx):
        tz_manila = pytz.timezone("Asia/Manila")
        now = datetime.datetime.now(tz_manila)

        # Get current day and time
        current_day = now.strftime("%A")
        current_time = self.get_roundedtime(now.strftime("%H:%M:%S"))

        # Give next class
        if current_day in self.days["synchronous"]:
            message, time = self.get_nextclass_message(current_time)
            if (message, time) != (None, None):  # class hasn't ended, hence, there's a message
                embed = self.get_nextclass_embed(message, current_day, time)
                await ctx.send(embed=embed)
            else:  # class has ended, hence, congratulate the student
                message = random.choice(self.responses["class_finished"])
                message = message.replace("__user__", f"<@{ctx.author.id}>")
                await ctx.send(message)
        else:
            message = get_restday_message(ctx, current_day, "no_input")
            await ctx.send(message)

    # Next functions
    def get_nextclass_embed(self, message, day, time):
        # Get embed
        embed = discord.Embed(
            title=message, color=discord.Color.from_rgb(*Colors.pink))

        # Get subject and link
        subject = self.synchronous_data["schedule"][day][time]
        link = self.synchronous_data["links"][subject]

        # Times
        start_time, end_time = time.split(" - ")
        start_time = format_time(start_time)
        end_time = format_time(end_time)
        time_limit = f"{start_time} - {end_time}"

        # Add Field
        embed.add_field(
            name=f"__{subject}__ {time_limit}:",
            value=link,
            inline=False)

        # Return
        return embed

    def get_nextclass_message(self, current_time):
        for sched in self.synchronous_data["schedule"].values():
            for time in sched.keys():
                # Get start time and end time
                start_time, end_time = time.split(" - ")
                start_time = self.get_roundedtime(start_time)
                end_time = self.get_roundedtime(end_time)

                # Check if the current time has passed the start time
                passed_starttime = True
                starttime_difference = start_time - current_time
                if not int(str(starttime_difference).count("-")):  # not passed start time
                    passed_starttime = False
                    starttime_difference = self.convert_timestr_to_datetime(
                        str(starttime_difference))

                # Check if the current time has passed the end time
                passed_endtime = True
                endtime_difference = end_time - current_time
                if not int(str(endtime_difference).count("-")):  # not passed end time
                    passed_endtime = False
                    endtime_difference = self.convert_timestr_to_datetime(
                        str(endtime_difference))

                # Get messages
                if not passed_starttime and (  # class is starting
                        starttime_difference.hour <= 0) and (
                        starttime_difference.minute <= 0):
                    message = "Class is starting!"

                    return message, time
                elif passed_starttime and not passed_endtime and (  # class already started
                        endtime_difference.hour >= 0) and (
                        endtime_difference.minute > 0):
                    message = self.get_classaldreadystarted_message(
                        current_time, start_time)

                    return message, time
                elif not passed_starttime:  # class hasn't started
                    message = self.get_classhasntstarted_messsage(
                        starttime_difference)

                    return message, time

    def get_hoursleft(self, time_pivot):
        hour = time_pivot.hour
        if hour > 1:  # plural
            hour = f"{hour} hrs"
        elif hour == 1:  # singular
            hour = f"{hour} hr"
        else:  # none
            hour = None
        
        return hour

    def get_minutesleft(self, time_pivot):
        min = time_pivot.minute
        if min > 1:  # plural
            min = f"{min} mins"
        elif min == 1:  # singular
            min = f"{min} min"
        else:
            min = None

        return min

    def get_classhasntstarted_messsage(self, starttime_difference):
        # Get how much time left
        hour = self.get_hoursleft(starttime_difference)
        min = self.get_minutesleft(starttime_difference)

        # Time left string
        if hour != None and min != None:  # with both hour and minutes
            message = f"__{hour} and {min} left__ utill class starts!"
        elif hour != None and min == None:  # with hour, but no minutes
            message = f"__{hour} left__ utill class starts!"
        elif hour == None and min != None:  # no hour, but with minutes
            message = f"__{min} left__ utill class starts!"
        else:  # no hour and no minutes
            message = "Hurry, class is alredy starting!"

        # Return
        return message

    def get_classaldreadystarted_message(self, current_time, start_time):
        # Get how much time has elapsed
        time_elapsed = self.convert_timestr_to_datetime(
            str(current_time - start_time))

        # Get how much time left
        hour = self.get_hoursleft(time_elapsed)
        min = self.get_minutesleft(time_elapsed)

        # Time Left String
        if hour != None and min != None:  # with both hour and minutes
            message = f"Class started {hour} and {min} ago!"
        elif hour != None and min == None:  # with hour, but no minutes
            message = f"Class started {hour} ago!"
        elif hour == None and min != None:  # no hour, but with minutes
            message = f"Class started {min} ago!"

        # Return
        return message


    def get_roundedtime(self, time):
        # Get date
        date = datetime.date.today()

        # Get time
        split_time = time.split(":")
        time = f"{split_time[0]}:{split_time[1]}:00"
        time = self.convert_timestr_to_datetime(time)

        # Return
        return datetime.datetime.combine(date, time)

    def convert_timestr_to_datetime(self, time):
        time = [int(t) for t in time.split(":")]
        return datetime.time(*time)


# Setup
def setup(bot):
    bot.add_cog(School(bot))
