import os


def get_clublinks():
    LINKS_DATA = os.environ["CLUB_LINKS_DATA"]
    links = {}
    for value in LINKS_DATA.split(", "):
        club, link = value.split(" = ")
        links[club] = link

    return links
