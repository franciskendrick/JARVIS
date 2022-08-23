from .colors import Colors
from .format_time import format_time
import discord
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "resources"
        )
    )

# School JSON
with open(f"{resources_path}/school.json") as json_file:
    school = json.load(json_file)
    synchronous_data = school["synchronous"]

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
    embed = discord.Embed(
        title=f"{day}:",
        color=discord.Color.from_rgb(*color))

    # Write to embed
    sched = synchronous_data["schedule"][day]
    for time in sched:
        # Get subjects and links
        subject = sched[time]
        link = synchronous_data["links"][subject]
        
        # Get time
        start_time, end_time = time.split(" - ")
        start_time = format_time(start_time)
        end_time = format_time(end_time)

        time = f"{start_time} - {end_time}"

        # Add field
        embed.add_field(
            name=f"__{subject}__ {time}:",
            value=link,
            inline=False)

    # Return embed
    return embed