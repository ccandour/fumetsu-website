from django.urls import path, register_converter

import fumetsu
from . import converters
from .views import List, Anime_content, Anime_episode, redirect_legacy_anime

register_converter(converters.AnimeUrlConverter, 'legacy_anime_slug')

urlpatterns = [
    path('anime/', List.as_view(), name='fumetsu-list'),
    path('anime/<legacy_anime_slug:anime_name>/', redirect_legacy_anime, name='legacy-anime-nm'),
    path('anime/<slug:anime_name>/', Anime_content.as_view(), name='anime-nm'),
    path('anime/<legacy_anime_slug:anime_name>/<int:ep>/', redirect_legacy_anime, name='legacy-ep-nm'),
    path('anime/<slug:anime_name>/<int:ep>/', Anime_episode.as_view(), name='ep-nm')
]
