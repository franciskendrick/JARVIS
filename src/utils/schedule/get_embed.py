from ..colors import Colors
from ..get_env import get_synchronous_schedule
from ..get_env import get_asynchronous_schedule
from .write_embed import write_syncsched
from .write_embed import write_asyncsched

# Schedules
sync_full_schedule = get_synchronous_schedule()
async_full_schedule = get_asynchronous_schedule()

# Embed colors
embed_colors = {
    "Monday": Colors.red,
    "Wednesday": Colors.yellow,
    "Friday": Colors.green
}


def get_schedule_embed(day, learning_type):
    # Get color
    color = embed_colors[day]

    # Write to embed
    if learning_type == "synchronous":
        embed = write_syncsched(day, color)
    elif learning_type == "asynchronous":
        embed = write_asyncsched(day, color)

    # Return embed
    return embed
