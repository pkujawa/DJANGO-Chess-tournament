
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='home'),
    path('filter/', views.FilterView.as_view(), name='filter-tournaments'),
    path('api/', views.MainPageList.as_view(), name='ongoing-tournaments'),
    path('api/tournaments/', views.TournamentList.as_view(), name='tournament-list'),
    path('api/tournaments/<int:pk>/', views.TournamentDetail.as_view(), name='tournament-detail'),
    path('api/tournaments/<int:pk>/games', views.GameList.as_view(), name='game-list'),
    path('api/players', views.PlayerList.as_view(), name='player-list'),
    path('api/game/<int:pk>', views.GameDetail.as_view(), name='game-detail'),
    path('api/addSuperuser', views.AddSuperuser.as_view(), name='add-superuser'),

]
