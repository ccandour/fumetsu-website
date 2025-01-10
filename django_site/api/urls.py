from django.urls import path

from . import views

urlpatterns = [
    path('get-series/', views.getSeries, name='get-series'),
    path('get-episodes/<str:series_id>/', views.getSeriesEpisodes, name='get-episodes'),
    path('get-posts/', views.getPosts, name='get-posts'),
    path('add-series/', views.addSeries, name='add-series'),
    path('add-episode/', views.addEpisode, name='add-episode'),
    path('add-announcement/', views.addAnnouncement, name='add-announcement'),
]
