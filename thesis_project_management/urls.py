from django.urls import path
from .views import home, create_team, get_arrangements, create_team_ui, team_detail_view, show_all_arrangements, \
    participate_arrangement, view_arrangement, assign_supervisor

urlpatterns = [
    path('home/', home, name='home'),
    path('api/create-team/', create_team, name='create_team_rest'),
    path('api/get-arrangements/', get_arrangements, name='get_arrangements'),
    path('create-team/', create_team_ui, name='create_team'),
    path('team-detail/', team_detail_view, name='team_detail'),
    path('arrangements/', show_all_arrangements, name='show_all_arrangements'),
    path('participate-arrangement/', participate_arrangement, name='participate_arrangement'),
    path('view-arrangement/', view_arrangement, name='view_arrangement'),
    path('assign-supervisor/', assign_supervisor, name='assign_supervisor'),
]
