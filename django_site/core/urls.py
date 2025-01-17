from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, register_converter, include
from django.views.generic import RedirectView

from . import converters
from .sitemaps import SeriesSitemap, EpisodeSitemap, StaticViewSitemap
from .views import *

register_converter(converters.AnimeSlug, 'anime_slug')
register_converter(converters.SearchTerm, 'search_term')
register_converter(converters.TagsString, 'tags_string')

sitemaps = {
    'series': SeriesSitemap,
    'episode': EpisodeSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('anime/', List.as_view(), name='anime-list'),
    path('anime/search/', search_anime, name='search'),
    path('anime/<anime_slug:anime_name>/', Series.as_view(), name='anime-nm'),
    path('anime/<anime_slug:anime_name>/<int:ep>/', Episode.as_view(), name='ep-nm'),

    path('about/', About.as_view(), name='core-about'),
    path('announcements/', Announcements.as_view(), name='core-announcements'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='core-privacy-policy'),
    path('terms-of-service/', TermsOfService.as_view(), name='core-terms-of-service'),
    path('edit-comment/<uuid:pk>', EditComment.as_view(), name='edit-cmt'),
    path('delete-comment/<uuid:pk>', DeleteComment.as_view(), name='del-cmt'),

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('', include('users.urls')),
    path('', include('api.urls')),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

