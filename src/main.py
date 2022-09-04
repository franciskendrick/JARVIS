from keep_alive import keep_alive
from disnake.ext import commands
import disnake
import os


if __name__ == "__main__":
    bot = commands.Bot(
        command_prefix="~", 
        help_command=None,
        intents=disnake.Intents.all())
    
    TOKEN = os.environ["TOKEN"]

    # Path
    path = os.path.dirname(__file__)

    # Load cogs
    for filename in os.listdir(f"{path}/cogs"):
        if filename.endswith(".py"):  # a python file
            bot.load_extension(f"cogs.{filename[:-3]}")

    # Run bot
    keep_alive()
    bot.run(TOKEN)
