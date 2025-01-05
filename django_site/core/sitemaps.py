from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import AnimeSeries, AnimeEpisode


class SeriesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return AnimeSeries.objects.all()

    def lastmod(self, obj):
        latest_episode = obj.animeepisode_set.order_by('-date_posted').first()
        return latest_episode.date_posted if latest_episode else None

class EpisodeSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return AnimeEpisode.objects.all()

    def lastmod(self, obj):
        return obj.date_posted

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["home", "anime-list", "core-about", "core-announcements", "core-privacy-policy", "core-terms-of-service"]

    def location(self, item):
        return reverse(item)
