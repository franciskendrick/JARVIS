from ..get_env import get_synchronous_schedule
from ..get_env import get_asynchronous_schedule
from ..get_env import get_classlinks
from ..format_time import formattime_to_twelevehour
import disnake

# Schedule and Links
sync_full_schedule = get_synchronous_schedule()
async_full_schedule = get_asynchronous_schedule()
links = get_classlinks()


def write_syncsched(day, color):
    # Get embed
    embed = disnake.Embed(
        title=f"__Synchronous__ - {day}:",
        color=disnake.Color.from_rgb(*color))

    # Write embed
    sched = sync_full_schedule[day]
    for time in sched:
        # Get subject and link
        subject = sched[time]
        link = links[subject]
        
        # Get time
        start_time, end_time = time.split(" - ")
        start_time = formattime_to_twelevehour(start_time)
        end_time = formattime_to_twelevehour(end_time)

        time = f"{start_time} - {end_time}"

        # Add field
        embed.add_field(
            name=f"__{subject}__ {time}:",
            value=link,
            inline=False)

    # Return
    return embed


def write_asyncsched(day, color):
    # Get embed
    embed = disnake.Embed(
        title=f"__Asynchronous__ - {day}:",
        color=disnake.Color.from_rgb(*color))

    # Write embed
    sched = async_full_schedule[day]
    for time in sched:
        # Get subject
        subject = sched[time]

        # Get time
        start_time, end_time = time.split(" - ")
        start_time = formattime_to_twelevehour(start_time)
        end_time = formattime_to_twelevehour(end_time)

        time = f"{start_time} - {end_time}"

        # Add field
        value = "*Do* `~club` *to get your club link/s.*" if subject == "Club Meeting" else "** **"
        embed.add_field(
            name=f"__{subject}__: **{time}**",
            value=value,
            inline=False)

    # Return
    return embed
