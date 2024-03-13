from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("thesis-project-manager/", include('thesis_project_management.urls')),
    path('register/', user_views.ui_register, name='register'),
    path('api/register/', user_views.RegisterUserAPIView.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('api-token-auth/', views.obtain_auth_token),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.user_profile, name='profile'),
    path('api/profile/', user_views.api_user_profile, name='api_profile'),
    path('api/register-role/', user_views.register_role, name='register_role'),
    path('register-student/', user_views.register_as_student, name='register_student'),
]
