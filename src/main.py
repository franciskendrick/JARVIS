from discord.ext import commands
import discord
import os

bot = commands.Bot(
    command_prefix="~", 
    intents=discord.Intents.all(),
)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb)


if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]

    # Path
    path = os.path.dirname(__file__)

    # Load cogs
    for filename in os.listdir(f"{path}/cogs"):
        if filename.endswith(".py"):  # a python file
            bot.load_extension(f"cogs.{filename[:-3]}")

    # Run bot
    bot.run(TOKEN)
