class AnimeSlug:
    regex = '[a-z0-9-]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class SearchTerm:
    regex = '[a-z0-9-!?,.\'"():]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class TagsString:
    regex = '[a-z-+]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
