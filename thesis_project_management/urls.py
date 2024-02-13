from django.urls import path
from .views import foo

urlpatterns = [
    path("api/v0/foo", foo, name='foo'),
]
