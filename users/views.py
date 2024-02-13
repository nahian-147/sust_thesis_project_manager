from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for user {username}. Please Login to continue.')
            return redirect('login')
        else:
            messages.warning(request, f'Please check your input')
            return render(request, 'users/register.html', {'title': 'Register', 'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'users/register.html', {'title': 'Register', 'form': form})


def user_profile(request):

    return render(request, 'users/profile.html', {'title': request.user})
