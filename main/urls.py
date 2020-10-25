from django.contrib import admin
from django.urls import path, include
from .views import home
from accounts.views import login_view, register_view, logout_view
# from .router import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view),
    path('accounts/register/', register_view),
    path('accounts/logout/', logout_view),
    path('', include(("chess_games.urls", 'chess_games'), namespace='tournaments')),
]

