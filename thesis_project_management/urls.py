from django.urls import path
from .views import home, create_team, get_arrangements

urlpatterns = [
    path('home/', home, name='home'),
    path('api/create-team/', create_team, name='create_team'),
    path('api/get-arrangements/', get_arrangements, name='get_arrangements'),
]
