from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boxscore', views.boxscore, name='boxscore'),
    path('players/<int:player_id>', views.player, name='player'),
    path('comparison', views.comparison, name='comparison'),
    path('comparisons/<str:playerone_name>&<str:playertwo_name>', views.comparisons, name='comparisons'),
    path('index/<str:letter>', views.index, name='index'),
    path('createDebate', views.createDebate, name='createDebate'),
    path('deleteDebate', views.deleteDebate, name='deleteDebate'),
    path('submitStatus', views.submitStatus, name='submitStatus'),
    path('statusCount/<int:status_id>&<str:approval>', views.statusCount, name='statusCount'),    
]
