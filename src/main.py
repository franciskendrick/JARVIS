from keep_alive import keep_alive
from disnake.ext import commands
import disnake
import asyncio
import os


async def load_cogs(bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):  # a python file
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main(bot, TOKEN):
    async with bot:
        await load_cogs(bot)
        keep_alive()
        await bot.start(TOKEN)


if __name__ == "__main__":
    bot = commands.Bot(
        command_prefix="~", 
        help_command=None,
        intents=disnake.Intents.all())

    TOKEN = os.environ["TOKEN"]

    asyncio.run(main(bot, TOKEN))
