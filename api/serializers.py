from rest_framework import serializers
from fumetsu.models import AnimeSeries, AnimeEpisode, AnimePost, Player, Relation


class SeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimeSeries
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'

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

class EpisodePOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimeEpisode
        fields = '__all__'

class PostPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimePost
        fields = '__all__'