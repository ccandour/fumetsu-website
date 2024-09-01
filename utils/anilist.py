from pyanilist import AniList, MediaType


def get_series_by_name(name: str):
    return AniList().search(name, type=MediaType.ANIME)


def get_series_by_id(anilist_id):
    return AniList().get(id=anilist_id)
