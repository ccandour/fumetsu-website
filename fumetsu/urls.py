from django.urls import path, register_converter, include
from django.conf import settings
from django.conf.urls.static import static

from . import converters
from .views import *

register_converter(converters.AnimeSlug, 'anime_slug')
register_converter(converters.AnimeUrlConverter, 'legacy_anime_slug')
register_converter(converters.SearchTerm, 'search_term')
register_converter(converters.TagsString, 'tags_string')

urlpatterns = [
    path('', Home.as_view(), name='fumetsu-home'),

    path('anime/', List.as_view(), name='anime-list'),
    path('anime/search/', search_anime, name='search'),
    path('anime/<anime_slug:anime_name>/', Series.as_view(), name='anime-nm'),
    path('anime/<legacy_anime_slug:anime_name>/', redirect_legacy_anime, name='legacy-anime-nm'),
    path('anime/<anime_slug:anime_name>/<int:ep>/', Episode.as_view(), name='ep-nm'),
    path('anime/<legacy_anime_slug:anime_name>/<int:ep>/', redirect_legacy_anime, name='legacy-ep-nm'),

    path('about/', About.as_view(), name='fumetsu-about'),
    path('announcements/', Announcements.as_view(), name='fumetsu-announcements'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='fumetsu-privacy-policy'),
    path('terms-of-service/', TermsOfService.as_view(), name='fumetsu-terms-of-service'),
    path('edit-comment/<uuid:pk>', EditComment.as_view(), name='edit-cmt'),
    path('delete-comment/<uuid:pk>', DeleteComment.as_view(), name='del-cmt'),

    path('', include('users.urls')),
]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

