from ..colors import Colors
from ..get_env import get_clublinks
import disnake
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", "resources"
        )
    )

# Club links
clublinks = get_clublinks()

# JSON
with open(f"{resources_path}/aliases.json") as json_file:
    all_aliases = json.load(json_file)


def get_clublinks_embed(given_clubname):
    # Get embed
    embed = disnake.Embed(
        title="Club Link/s:",
        color=disnake.Color.from_rgb(*Colors.blue))

    # Write embed
    if given_clubname == None:  # write all club names
        for club, link in clublinks.items():
            # Add field
            embed.add_field(
                name=f"__{club}:__",
                value=link,
                inline=False)
    else:  # write given club name
        # Get aliases
        for name in clublinks.keys():
            aliases = []

            # Get aliases
            splitted_name = name.split(" - ")
            if len(splitted_name) > 0:  # multiple names
                for _name in splitted_name:
                    for j in range(len(_name)):
                        aliases.append(_name[0:j+2].lower())

                aliases.append(name.lower())
            else:  # one name (normal)
                for i in range(len(name)):
                    aliases.append(name[0:i+2].lower())

            # Format aliases
            aliases = list(set(aliases))

            # Get abbriviation aliases
            try:
                abbr_aliases = all_aliases["club_name"][name]
            except KeyError:
                abbr_aliases = []

            # Get club name
            if given_clubname.lower() in aliases or given_clubname.lower() in abbr_aliases:
                club_name = name
                break

        # Add field
        embed.add_field(
            name=f"__{club_name}:__",
            value=clublinks[club_name],
            inline=False)

    # Return
    return embed
