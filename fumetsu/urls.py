from django.urls import path
from .views import *

urlpatterns = [
    path('',  Home.as_view(), name='fumetsu-home'),
    path('about/', about.as_view(), name='fumetsu-about'),
    path('KGePvbaey4XYheR/', Cre_ani.as_view(), name='Cre-ani'),
    path('iBrBlGKNxHKQAKS/', Cre_series.as_view(), name='Cre-ser'),
    path('BTb5YkFuHyF5RtP/', Cre_info.as_view(), name='Cre-info'),
    path('vRU8au2ZreoUd4y/', Ed_an.as_view(), name='ed-an'),
    path('info/', Info.as_view(), name='fumetsu-info'),
    path('info/<int:pkk>', Info_d.as_view(), name='fumetsu-infod'),
    path('google5299714afc51785a.html', google_auth.as_view(), name='google_auth'),
    path('link_error/', Link_error.as_view(), name='lnk-err')
]

