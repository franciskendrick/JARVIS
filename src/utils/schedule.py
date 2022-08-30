from .colors import Colors
from .get_env import get_synchronous_schedule
from .get_env import get_links
from .format_time import formattime_to_twelevehour
import disnake
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "resources"
        )
    )

# Schedule and Links
full_schedule = get_synchronous_schedule()
links = get_links()

# Embed colors
embed_colors = {
    "Monday": Colors.red,
    "Tuesday": Colors.red,
    "Wednesday": Colors.yellow,
    "Thursday": Colors.yellow,
    "Friday": Colors.green,
    "Saturday": Colors.green
}


def get_schedule_embed(day):
    color = embed_colors[day]
    embed = disnake.Embed(
        title=f"{day}:",
        color=disnake.Color.from_rgb(*color))

    # Write to embed
    sched = full_schedule[day]
    for time in sched:
        # Get subjects and links
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

    # Return embed
    return embed
