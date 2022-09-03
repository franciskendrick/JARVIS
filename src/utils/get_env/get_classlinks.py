import os


def get_classlinks():
    LINKS_DATA = os.environ["CLASS_LINKS_DATA"]
    links = {}
    for value in LINKS_DATA.split(", "):
        subject, link = value.split(" = ")
        links[subject] = link

    return links
