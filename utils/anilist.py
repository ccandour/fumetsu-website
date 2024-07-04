from pyanilist import AniList, MediaType

def get_series_by_name(name: str):
    return AniList().search(name, type=MediaType.ANIME)
