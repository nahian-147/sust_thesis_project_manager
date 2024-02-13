from django.shortcuts import render


def home(request):
    return render(request, 'thesis_project_management/home.html', {'title': 'Home'})
