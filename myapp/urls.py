from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boxscore', views.boxscore, name='boxscore'),
    path('players/<int:player_id>', views.player, name='player'),
    path('comparison', views.comparison, name='comparison'),
    path('comparisons/<str:playerone_name>&<str:playertwo_name>', views.comparisons, name='comparisons'),
]
