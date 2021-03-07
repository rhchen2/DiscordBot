import os
import requests
from bs4 import BeautifulSoup

HOW_TO_USE = "Help for MangaUpdates:\n\t$manga help: see this menu\n\t$manga updates: get a list of the current chapters for the registered mangas\n\t$manga remove <title>: removes a manga from the tracking list\n\t$manga list: gets the currently registered manga\n\t$manga register <link>: registers a new manga to follow; right now only mangakakalot.com is supported"

UNSUPPORTED_COMMAND = "Command '{0}' is unsupported, please see help menu with '$manga help'"

manga = dict()

def save_manga():
    f = open("manga.txt", "w+")
    f.write(str(manga))
    f.close()

def read_manga():
    if not os.path.exists("manga.txt"):
        return
    f = open("manga.txt", "r").read()
    manga = eval(f)


def get_manga_title(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    list_items = soup.find_all("title")
    title = list_items[0].get_text()
    return title[:title.index(' Manga')]

def get_chapter_link(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    list_items = soup.find_all("li")
    item = list_items[0]
    link = item.find_all("a")[0]
    return "{0}: {1}\n".format(link['title'], link['href'])

def get_mangas():
    ret = "Registered Manga List:\n"
    for key in manga:
        ret += "\t" + key + "\n"
    return ret

def register_manga(url):
    title = get_manga_title(url)
    if len(title) < 1:
        return "No title found for {0}".format(url)
    manga[title] = url
    save_manga()
    return "Manga '{0}' Registered".format(title)

def get_updates():
    ret = ""
    for key in manga:
        ret += get_chapter_link(manga[key])
    return ret

def remove_manga(title):
    for key in manga:
        if title.lower() == key.lower():
            del manga[key]
            return "Removed {0} from MangaUpdates".format(key)
    return "Failed to find {0} in Registered List\n{1}".format(title, get_mangas())


def manga_main(message):
    read_manga()
    tokens = message.split(' ')
    if len(tokens) < 2 or tokens[1].lower() == 'help':
        return HOW_TO_USE
    elif len(tokens) == 3 and tokens[1].lower() == 'register':
        return register_manga(tokens[2])
    elif len(tokens) == 2 and tokens[1].lower() == 'updates':
        return get_updates()
    elif len(tokens) > 2 and tokens[1].lower() == 'remove':
        return remove_manga(" ".join(tokens[2:]))
    elif len(tokens) == 2 and tokens[1].lower() == 'list':
        return get_mangas()
    else:
        return UNSUPPORTED_COMMAND.format(message)
