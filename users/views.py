import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from thesis_project_management.serializers import TeamSerializer
from thesis_project_management.team_utility_functions import get_all_teams_of_a_participant
from .models import Student, Supervisor, Teacher
from .serializers import RegisterSerializer, StudentSerializer, SupervisorSerializer, TeacherSerializer
from .register_roles import register_user_as_a_student, register_user_as_a_teacher, register_user_as_a_supervisor

logger = logging.getLogger('django')


def ui_register(request):
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


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@login_required
def user_profile(request):
    user = User.objects.get(username=request.user.username)
    teams = None

    student_avatar = Student.objects.filter(user=user)
    if student_avatar:
        logger.info('found student avatar for this profile')
        teams = get_all_teams_of_a_participant(student_avatar.first())

    supervisor_avatar = Supervisor.objects.filter(user=user)
    if supervisor_avatar:
        logger.info('found supervisor avatar for this profile')
        teams = get_all_teams_of_a_participant(supervisor_avatar.first())

    teacher_avatar = Teacher.objects.filter(user=user)
    if teacher_avatar:
        logger.info('found teacher avatar for this profile')
        teams = get_all_teams_of_a_participant(teacher_avatar.first())
    return render(request, 'users/profile.html', {
        'title': request.user,
        'student_avatar': student_avatar.first() if student_avatar else None,
        'supervisor_avatar': supervisor_avatar.first() if supervisor_avatar else None,
        'teacher_avatar': teacher_avatar.first() if teacher_avatar else None,
        'teams': teams
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    user = User.objects.get(username=request.user.username)
    teams = []
    participant_data = None

    student_avatar = Student.objects.filter(user=user)
    if student_avatar:
        logger.info('found student avatar for this profile')
        student_avatar = student_avatar.first()
        teams = get_all_teams_of_a_participant(student_avatar)
        participant_data = StudentSerializer(student_avatar).data
        teams = TeamSerializer(teams, many=True).data
        return Response(status=200, data={
            'participant_data': participant_data,
            'teams': teams
        })

    supervisor_avatar = Supervisor.objects.filter(user=user)
    if supervisor_avatar:
        logger.info('found supervisor avatar for this profile')
        supervisor_avatar = supervisor_avatar.first()
        teams_as_supervisor = get_all_teams_of_a_participant(supervisor_avatar)
        participant_data = SupervisorSerializer(supervisor_avatar).data
        teams_as_supervisor = TeamSerializer(teams_as_supervisor, many=True).data
        teams += teams_as_supervisor

    teacher_avatar = Teacher.objects.filter(user=user)
    if teacher_avatar:
        logger.info('found teacher avatar for this profile')
        teacher_avatar = teacher_avatar.first()
        teams_as_teacher = get_all_teams_of_a_participant(teacher_avatar)
        participant_data = TeacherSerializer(teacher_avatar).data
        teams_as_teacher = TeamSerializer(teams_as_teacher, many=True).data
        teams += teams_as_teacher

    if teacher_avatar or supervisor_avatar:
        return Response(status=200, data={
            'participant_data': participant_data,
            'teams': teams
        })

    return Response(status=449, data={"message": "User Profile not ready yet. please register as a participant first."})


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def register_role(request):
    user = User.objects.get(username=request.user.username)
    request_body = json.loads(request.body)
    role_id = str(request_body['role_id'])
    if role_id == 'STUDENT':
        if 'student_info' in request_body:
            if register_user_as_a_student(user=user, student_data=request_body['student_info']):
                return Response(status=201, data={"message": "Registered as a Student"})
        else:
            return Response(status=403, data={"message": "Student Info missing!"})
    elif role_id == 'SUPERVISOR':
        if 'supervisor_info' in request_body:
            if register_user_as_a_supervisor(user=user, supervisor_data=request_body['supervisor_info']):
                return Response(status=201, data={"message": "Registered as a Supervisor"})
        else:
            return Response(status=403, data={"message": "Supervisor Info missing!"})
    elif role_id == 'TEACHER':
        if 'teacher_info' in request_body:
            if register_user_as_a_teacher(user=user, teacher_data=request_body['teacher_info']):
                return Response(status=201, data={"message": "Registered as a Teacher"})
        else:
            return Response(status=403, data={"message": "Teacher Info missing!"})
    else:
        return Response(status=403, data={"message": "You Naughty Punk !!!"})
