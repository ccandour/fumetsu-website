from django.urls import path
from . import views 
from .views import List, Anime_content, Anime_episode


urlpatterns = [
	path('anime/', List.as_view(), name='fumetsu-list'),
    path('anime/<slug:anime_name>/', Anime_content.as_view(), name='anime-nm'),
    path('anime/<slug:anime_name>/<int:ep>/', Anime_episode.as_view(), name='ep-nm')
]
