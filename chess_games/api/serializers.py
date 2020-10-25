from django.contrib.auth.models import User
from rest_framework import serializers
from chess_games.models import Tournament, Player, Game


class TournamentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'date', 'number_of_players', 'user')


class PlayerSerializer(serializers.ModelSerializer):
    tournament_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('name', 'tournament_name', 'tournament')

    def get_tournament_name(self, obj):
        return obj.tournament.name


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('tournament', 'white', 'black')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'is_superuser', 'username', 'email')
