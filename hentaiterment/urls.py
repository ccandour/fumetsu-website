from django.urls import path
from .views import *

urlpatterns = [
    path('hentaiterment', KH_Home.as_view(), name='kh'),
    path('hentaiterment/upld/', KH_upld.as_view(), name='kh-upload'),
    path('hentaiterment/crte/', KH_Cre_series.as_view(), name='kh-create'),
    path('hentaiterment/list/',  KH_list.as_view(), name='kh-list'),
    path('hentaiterment/<slug:hentai_name>/',  Hentai_content.as_view(), name='kh-hentai'),
    path('hentaiterment/<slug:hentai_name>/<int:ep>',  KH_Anime_episode.as_view(), name='kh-hentai-odc'),
]

