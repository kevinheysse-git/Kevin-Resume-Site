from django.urls import path
from . import views

app_name = 'nba_visualizer'

urlpatterns = [
    path('', views.player_search, name='player_search'),
    path('player/<int:player_id>/', views.player_stats, name='player_stats'),
    path('player/<int:player_id>/shots/<str:game_id>/', views.shot_chart_data, name='shot_chart_data'),  # ← new
]