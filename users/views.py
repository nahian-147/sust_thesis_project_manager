import logging

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Student, Supervisor, Teacher

logger = logging.getLogger('django')


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
    user = User.objects.get(username=request.user.username)
    student_avatar = Student.objects.filter(user=user)
    if student_avatar:
        logger.info('found student avatar for this profile')
    supervisor_avatar = Supervisor.objects.filter(user=user)
    if supervisor_avatar:
        logger.info('found supervisor avatar for this profile')
    teacher_avatar = Teacher.objects.filter(user=user)
    if teacher_avatar:
        logger.info('found teacher avatar for this profile')
    return render(request, 'users/profile.html', {
        'title': request.user,
        'student_avatar': student_avatar.first() if student_avatar else None,
        'supervisor_avatar': supervisor_avatar.first() if supervisor_avatar else None,
        'teacher_avatar': teacher_avatar.first() if teacher_avatar else None
    })
