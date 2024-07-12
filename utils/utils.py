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

class AnimeSeriesJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Anime_list):
            tags = list(Tags.objects.filter(anime_anilist_id=obj.anilist_id).values_list('label', flat=True))
            return {
                "name_english": (obj.name_english.replace('"', '\\"') if obj.name_english else obj.name_romaji.replace('"', '\\"')),
                "name_romaji": obj.name_romaji.replace('"', '\\"'),
                "cover_image": obj.cover_image,
                "tags": tags,
                "web_name": obj.web_name,
                "format": obj.format,
            }
        else:
            return super().default(obj)
