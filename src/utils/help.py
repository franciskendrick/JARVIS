from .colors import Colors
import discord


def get_fullhelp_embed(ctx, bot):
    embed = discord.Embed(
        title="**Help Command**",
        color=discord.Color.from_rgb(*Colors.light_brown))
    
    # Set author
    embed.set_author(
        name=ctx.me, 
        icon_url=ctx.me.avatar_url)

    # Add description
    embed.description = "Use `~help [command]` to see more information about a command." 

    # Add commands list
    commands_text = ""
    for (name, command) in bot.all_commands.items():
        if name != "help":
            commands_text += f"`~{name}`: {command.description}"
            commands_text += "\n"
    else:
        embed.add_field(
            name=":gear: __Commands:__",
            value=commands_text)

    # Return
    return embed


def get_commandinfo_embed(ctx, bot, command_name):
    command = bot.all_commands.get(command_name)
    embed = discord.Embed(
        title=f"**Command __{command_name}__**",
        color=discord.Color.from_rgb(*Colors.light_brown))

    # Set author
    embed.set_author(
        name=ctx.me, 
        icon_url=ctx.me.avatar_url)

    # Add how to use the command
    usage = command.usage
    embed.add_field(
        name="How to use:",
        value=f"`~{command_name}{(' ' + usage) if usage else ''}`")

    # Add command's description
    description = command.description
    embed.add_field(
        name="Description:", 
        value=description,
        inline=False)

    # Add command's parameters
    parameters = command.help
    embed.add_field(
        name="Parameter/s:",
        value=parameters)

    # Return
    return embed
