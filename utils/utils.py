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