from django.urls import path
from .views import home, create_team, get_arrangements, create_team_ui

urlpatterns = [
    path('home/', home, name='home'),
    path('api/create-team/', create_team, name='create_team_rest'),
    path('api/get-arrangements/', get_arrangements, name='get_arrangements'),
    path('create-team/', create_team_ui, name='create_team'),
]
