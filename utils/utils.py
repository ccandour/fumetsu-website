from slugify import slugify

from fumetsu.models import Anime_list


def generate_web_name(anime: Anime_list):
    title = anime.name_english if anime.name_english else anime.name_romaji
    return slugify(title)

def translate_status(status):
    if status == 'FINISHED':
        return 'Zakończone'
    elif status == 'AIRING':
        return 'Wychodzi'
    else:
        return status

def translate_tag(tag):
    if tag == 'Action':
        return 'Akcja'
    elif tag == 'Adventure':
        return 'Przygodowe'
    elif tag == 'Comedy':
        return 'Komedia'
    elif tag == 'Drama':
        return 'Dramat'
    elif tag == 'Music':
        return 'Muzyka'
    elif tag == 'Mystery':
        return 'Kryminał'
    elif tag == 'Romance':
        return 'Romans'
    elif tag == 'Psychological':
        return 'Psychologiczne'
    elif tag == 'Sports':
        return 'Sportowe'
    elif tag == 'Supernatural':
        return 'Nadnaturalne'
    else:
        return tag