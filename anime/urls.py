from django.urls import path, register_converter

import fumetsu
from . import converters
from .views import List, Series, Episode, redirect_legacy_anime, search_anime

register_converter(converters.AnimeSlug, 'anime_slug')
register_converter(converters.AnimeUrlConverter, 'legacy_anime_slug')
register_converter(converters.SearchTerm, 'search_term')
register_converter(converters.TagsString, 'tags_string')

urlpatterns = [
    path('anime/', List.as_view(), name='anime-list'),
    path('anime/search/', search_anime, name='search'),
    path('anime/<anime_slug:anime_name>/', Series.as_view(), name='anime-nm'),
    path('anime/<legacy_anime_slug:anime_name>/', redirect_legacy_anime, name='legacy-anime-nm'),
    path('anime/<anime_slug:anime_name>/<int:ep>/', Episode.as_view(), name='ep-nm'),
    path('anime/<legacy_anime_slug:anime_name>/<int:ep>/', redirect_legacy_anime, name='legacy-ep-nm'),
]
