from django.urls import path
from .views import home

urlpatterns = [
    path("api/v0/foo", home, name='foo'),
    path('home/', home, name='home')
]
