from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from fumetsu.models import AnimeSeries, AnimePost, Player
from .serializers import SeriesSerializer, EpisodeSerializer, PostSerializer


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
    serializer = SeriesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def addEpisode(request):
    serializer = EpisodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
