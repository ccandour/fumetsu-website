from rest_framework import serializers
from fumetsu.models import AnimeSeries, AnimeEpisode, AnimePost, Player


class SeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimeSeries
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = 'id', 'key_map', 'key_map', 'website', 'link'

class EpisodeSerializer(serializers.ModelSerializer):
    key_map = SeriesSerializer()
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = AnimeEpisode
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    key_map = EpisodeSerializer()

    class Meta:
        model = AnimePost
        fields = '__all__'
