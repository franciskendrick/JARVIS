import os


def get_links():
    LINKS_DATA = os.environ["LINKS_DATA"]
    links = {}
    for value in LINKS_DATA.split(", "):
        subject, link = value.split(" = ")
        links[subject] = link

    return links
