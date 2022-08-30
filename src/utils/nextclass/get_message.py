from ..colors import Colors
from ..get_env import get_synchronous_schedule
from ..get_env import get_links
from ..format_time import formattime_to_twelevehour
from ..format_time import convert_timestr_to_datetime
from ..format_time import round_time
from .get_title import get_classstarted_title
from .get_title import get_classnotstarted_title
import disnake
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", "resources"
        )
    )

# Schedule and Links
full_schedule = get_synchronous_schedule()
links = get_links()


def get_nextclass_title(current_time):
    for schedule in full_schedule.values():
        for time in schedule.keys():
            # Get start time and end time
            start_time, end_time = time.split(" - ")
            start_time = round_time(start_time)
            end_time = round_time(end_time)

            # Check if the current time has passed the start time
            passed_starttime = True
            starttime_difference = start_time - current_time
            if not int(str(starttime_difference).count("-")):  # not passed start time
                passed_starttime = False
                starttime_difference = convert_timestr_to_datetime(
                    str(starttime_difference))

            # Check if the current time has passed the end time
            passed_endtime = True
            endtime_difference = end_time - current_time
            if not int(str(endtime_difference).count("-")):  # not passed end time
                passed_endtime = False
                endtime_difference = convert_timestr_to_datetime(
                    str(endtime_difference))

            # Get title
            if not passed_starttime and (  # class is starting
                    starttime_difference.hour <= 0) and (
                    starttime_difference.minute <= 0):
                title = "Class is starting!"
                return title, time
            elif passed_starttime and not passed_endtime and (  # class already started
                    endtime_difference.hour >= 0) and (
                    endtime_difference.minute > 0):
                title = get_classstarted_title(current_time, start_time)
                return title, time
            elif not passed_starttime:  # class hasn't started
                title = get_classnotstarted_title(starttime_difference)
                return title, time

    return (None, None)


def get_nextclass_embed(title, day, time):
    # Get embed
    embed = disnake.Embed(
        title=title, color=disnake.Color.from_rgb(*Colors.pink))

    # Get subject and link
    subject = full_schedule[day][time]
    link = links[subject]

    # Times
    start_time, end_time = time.split(" - ")
    start_time = formattime_to_twelevehour(start_time)
    end_time = formattime_to_twelevehour(end_time)
    time_limit = f"{start_time} - {end_time}"

    # Add Field
    embed.add_field(
        name=f"__{subject}__ {time_limit}:",
        value=link,
        inline=False)

    # Return
    return embed
