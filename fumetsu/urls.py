from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='fumetsu-home'),
    path('about/', about.as_view(), name='fumetsu-about'),
    path('KGePvbaey4XYheR/', Cre_ani.as_view(), name='Cre-ani'),
    # path('iBrBlGKNxHKQAKS/', Cre_series.as_view(), name='Cre-ser'),
    path('BTb5YkFuHyF5RtP/', Cre_info.as_view(), name='Cre-info'),
    # path('vRU8au2ZreoUd4y/', Ed_an.as_view(), name='ed-an'),
    path('announcements/', Announcements.as_view(), name='fumetsu-announcements'),
    path('privacy-policy/', Privacy_policy.as_view(), name='fumetsu-privacy-policy'),
    path('terms-of-service/', Terms_of_service.as_view(), name='fumetsu-terms-of-service'),
    path('info/<int:pkk>', Info_d.as_view(), name='fumetsu-infod'),
    path('google5299714afc51785a.html', google_auth.as_view(), name='google_auth'),
    path('link_error/', Link_error.as_view(), name='lnk-err')
]

