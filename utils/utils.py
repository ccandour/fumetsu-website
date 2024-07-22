from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from slugify import slugify

from anime.models import Tags
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

def tag_label_to_polish(tag):
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

def tag_label_to_english(tag):
    if tag == 'Akcja':
        return 'Action'
    elif tag == 'Przygodowe':
        return 'Adventure'
    elif tag == 'Komedia':
        return 'Comedy'
    elif tag == 'Dramat':
        return 'Drama'
    elif tag == 'Muzyka':
        return 'Music'
    elif tag == 'Kryminał':
        return 'Mystery'
    elif tag == 'Romans':
        return 'Romance'
    elif tag == 'Psychologiczne':
        return 'Psychological'
    elif tag == 'Sportowe':
        return 'Sports'
    elif tag == 'Nadnaturalne':
        return 'Supernatural'
    else:
        return tag



class AnimeSeriesJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Anime_list):
            tags = list(Tags.objects.filter(anime_anilist_id=obj.anilist_id).values_list('label_polish', flat=True))

            return {
                "name_english": (obj.name_english.replace('"', '\\"') if obj.name_english else obj.name_romaji.replace('"', '\\"')),
                "name_romaji": obj.name_romaji.replace('"', '\\"'),
                "image": obj.image,
                "tags": tags,
                "web_name": obj.web_name,
                "format": obj.format,
                "rating": obj.rating,
            }
        else:
            return super().default(obj)
