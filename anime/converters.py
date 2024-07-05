from django.shortcuts import redirect

from fumetsu.models import Url_redirects


class AnimeUrlConverter:
    regex = '[\w]+'

    def to_python(self, value):
        return value


    def to_url(self, value):
        return value
