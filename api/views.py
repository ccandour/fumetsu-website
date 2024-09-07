import os

import requests
from pyanilist import AniList
from django.core.files import File
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from fumetsu.models import AnimeSeries, AnimePost, Player, Relation
from utils.utils import generate_web_name
from .serializers import SeriesSerializer, EpisodeSerializer, RelationSerializer, PostSerializer, PlayerSerializer, EpisodePOSTSerializer, \
    PostPOSTSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getSeries(request):
    series = AnimeSeries.objects.all()
    serializer = SeriesSerializer(series, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getSeriesEpisodes(request, series_id):
    episodes = AnimeSeries.objects.get(id=series_id).animeepisode_set.all()
    for episode in episodes:
        episode.players = Player.objects.filter(key_map=episode)
    serializer = EpisodeSerializer(episodes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getPosts(request):
    posts = AnimePost.objects.all()
    for post in posts:
        post.key_map.players = Player.objects.filter(key_map=post.key_map)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def addSeries(request):
    anilist_entry = AniList().get(id=request.data.get('anilist_id'))

    data = {
        'anilist_id': request.data.get('anilist_id'),
        'name_english': anilist_entry.title.english,
        'name_romaji': anilist_entry.title.romaji,
        'format': anilist_entry.format,
        'status': anilist_entry.status,
        'episode_count': anilist_entry.episodes,
        'rating': anilist_entry.average_score,
        'content': anilist_entry.description.default,
        'image': str(anilist_entry.cover_image.extra_large),
        'web_name': generate_web_name(anilist_entry.title.english)
    }

    serializer = SeriesSerializer(data=data)
    if serializer.is_valid():
        series = serializer.save()
        # Add relations
        db_series = AnimeSeries.objects.all()
        for relation in anilist_entry.relations:
            if db_series.filter(anilist_id=relation.id).exists():
                relation_data = {
                    'parent_series_id': series.anilist_id,
                    'child_series_id': relation.id,
                    'type': relation.relation_type
                }
                relation_serializer = RelationSerializer(data=relation_data)
                if relation_serializer.is_valid():
                    relation_serializer.save()

                relation_anilist_entry = AniList().get(id=relation.id)
                for related_relation in relation_anilist_entry.relations:
                    if str(related_relation.id) == series.anilist_id:
                        related_relation_data = {
                            'parent_series_id': relation.id,
                            'child_series_id': series.anilist_id,
                            'type': related_relation.relation_type
                        }
                        related_relation_serializer = RelationSerializer(data=related_relation_data)
                        if related_relation_serializer.is_valid():
                            print('workin')
                            related_relation_serializer.save()
                        print(related_relation_serializer.errors)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def addEpisode(request):
    # Extract episode data from the request
    series_anilist_id = request.data.get('series_anilist_id')
    ep_nr = request.data.get('ep_nr')
    title = request.data.get('title')

    subtitles_url = request.data.get('subtitles_url')
    subtitles_name = request.data.get('subtitles_name')
    os.makedirs('media/temp', exist_ok=True)
    res = requests.get(subtitles_url)
    try:
        with open(f'media/temp/{subtitles_name}', 'wb') as f:
            f.write(res.content)
    except:
        return Response({'error': 'Could not download subtitles'})
    subtitles = open(f'media/temp/{subtitles_name}', 'rb')

    # Create the episode
    episode_data = {
        'key_map': AnimeSeries.objects.get(anilist_id=series_anilist_id).id,
        'ep_nr': ep_nr,
        'title': title,
        'subtitles': File(subtitles, name=subtitles_name)
    }

    episode_serializer = EpisodePOSTSerializer(data=episode_data)

    if episode_serializer.is_valid():
        episode = episode_serializer.save()

        # Link the key_map of each player to the newly created episode
        players = request.data.get('players')
        for player in players:
            player['key_map'] = episode.id
            player_serializer = PlayerSerializer(data=player)
            if player_serializer.is_valid():
                player_serializer.save()

        # Create a corresponding post
        image_url = request.data.get('image_url')
        image_name = request.data.get('image_name')
        res = requests.get(image_url)
        with open(f'media/temp/{image_name}', 'wb') as f:
            f.write(res.content)
        image = open(f'media/temp/{image_name}', 'rb')
        post_data = {
            'key_map': episode.id,
            'content': request.data.get('content'),
            'image': File(image, name=image_name)
        }
        post_serializer = PostPOSTSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()

        # Close and remove temp files
        subtitles.close()
        os.remove(f'media/temp/{subtitles_name}')
        image.close()
        os.remove(f'media/temp/{image_name}')

        return Response(episode_serializer.data)
    else:
        subtitles.close()
        os.remove(f'media/temp/{subtitles_name}')
        return Response(episode_serializer.errors)