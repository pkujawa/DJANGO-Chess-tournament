from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.response import Response
from .api.serializers import TournamentSerializer, PlayerSerializer, GameSerializer, GameDetailSerializer, \
    UserSerializer
from .models import Tournament, Player, Game
import django.views.generic as generic
from .forms import FilterByDate
import datetime
import random
from django.contrib.auth.models import User


class MainPageView(generic.TemplateView):
    template_name = 'chess_games/home.html'

    def get(self, *args, **kwards):
        return render(self.request, self.template_name)


class FilterView(generic.TemplateView):
    login_required = True
    template_name = 'chess_games/filter.html'

    def get(self, request):
        form = FilterByDate()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FilterByDate(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            url = "/api/tournaments/?from=" + str(date_from)[:10] + "&to=" + str(date_to)[:10]
        return redirect(url)


class TournamentList(generics.ListCreateAPIView):
    login_required = True
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def get(self, format=None, *args, **kwargs):
        d_from = self.request.query_params.get('from', None)
        d_to = self.request.query_params.get('to', None)
        if d_from is not None and d_to is not None:
            if self.request.user.is_superuser:
                tournaments = Tournament.objects.filter(date__gte=d_from).filter(date__lte=d_to)
            else:
                tournaments = Tournament.objects.filter(user=self.request.user, date__gte=d_from).filter(date__lte=d_to)
        else:
            if self.request.user.is_superuser:
                tournaments = Tournament.objects.all()
            else:
                tournaments = Tournament.objects.filter(user=self.request.user)
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)


class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    login_required = True
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def get(self, request, pk, format=None, *args, **kwargs):
        if self.request.user.is_superuser:
            tournament = Tournament.objects.filter(pk=pk).first()
        else:
            tournament = Tournament.objects.filter(user=self.request.user, pk=pk).first()
        if not tournament:
            return redirect('tournaments:tournament-list')
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)

    def delete(self, pk, format=None, *args, **kwargs):
        tournament = Tournament.objects.get(pk=pk)
        if tournament.date > datetime.datetime.now() or self.request.user.is_superuser:
            tournament.delete()
            return Response(self.request.data, status=status.HTTP_200_OK)
        else:
            return redirect('tournaments:tournament-list')


class PlayerList(generics.ListCreateAPIView):
    login_required = True
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, format=None, *args, **kwargs):
        if self.request.user.is_superuser:
            players = Player.objects.all()
        else:
            user_tournaments = Tournament.objects.filter(user=self.request.user)
            players = Player.objects.filter(tournament__pk__in=user_tournaments)
        if players:
            serializer = PlayerSerializer(players, many=True)
        else:
            return Response()
        return Response(serializer.data)


class GameList(generics.ListAPIView):
    login_required = True
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        games = Game.objects.filter(tournament__pk=pk)
        if games.count() == 0:
            tournament = Tournament.objects.get(pk=pk)
            players = [p for p in Player.objects.filter(tournament=tournament)]
            for _ in range(0, len(players), 2):
                random.shuffle(players)
                game = Game()
                game.tournament = tournament
                game.white = players.pop()
                if len(players) > 0:
                    game.black = players.pop()
                game.save()
        return games


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    login_required = True
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer

    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if self.request.user.is_superuser:
            game = Game.objects.get(pk=pk)
        elif self.request.user == Game.objects.get(pk=pk).tournament.user:
            game = Game.objects.get(pk=self.kwargs.get('pk'))
        else:
            return redirect('tournaments:ongoing-tournaments')
        if game:
            serializer = GameSerializer(game)
        else:
            return Response()
        return Response(serializer.data)


class MainPageList(generics.ListAPIView):
    login_required = True
    queryset = Tournament.objects.filter(date__lt=datetime.datetime.now())
    serializer_class = TournamentSerializer


class AddSuperuser(generics.ListCreateAPIView):
    login_required = True
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, format=None, *args, **kwargs):
        if self.request.user.is_superuser:
            return Response()
        else:
            return redirect('tournaments:ongoing-tournaments')
