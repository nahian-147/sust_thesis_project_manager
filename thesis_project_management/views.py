import json

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Team
from .serializers import ArrangementSerializer
from .team_utility_functions import create_team_from_dict, get_arrangement_list_for_team


def home(request):
    return render(request, 'thesis_project_management/home.html', {'title': 'Home'})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_team(request):
    user = User.objects.get(username=request.user.username)
    request_body = json.loads(request.body)
    role_id = str(request_body['role_id'])
    if 'team_info' in request_body:
        team_info = request_body['team_info']
        if role_id == 'STUDENT':
            if create_team_from_dict(team_info):
                return Response(status=201, data={"message": "Created Team"})
            else:
                return Response(status=448,
                                data={"message": "At least one of the students is assigned to some other team."})
        # elif role_id == 'SUPERVISOR':
        #     if 'supervisor_info' in request_body:
        #         if register_user_as_a_supervisor(user=user, supervisor_data=request_body['supervisor_info']):
        #             return Response(status=201, data={"message": "Registered as a Supervisor"})
        #     else:
        #         return Response(status=403, data={"message": "Supervisor Info missing!"})
        # elif role_id == 'TEACHER':
        #     if 'teacher_info' in request_body:
        #         if register_user_as_a_teacher(user=user, teacher_data=request_body['teacher_info']):
        #             return Response(status=201, data={"message": "Registered as a Teacher"})
        #     else:
        #         return Response(status=403, data={"message": "Teacher Info missing!"})
        # else:
        #     return Response(status=403, data={"message": "You Naughty Punk !!!"})
    else:
        return Response(status=403, data={"message": "No Team Info given!"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_arrangements(request):
    user = User.objects.get(username=request.user.username)
    request_body = json.loads(request.body)
    role_id = str(request_body['role_id'])
    if 'team_info' in request_body:
        team_info = request_body['team_info']
        team = Team.objects.get(id=team_info['id'])
        return Response(status=200, data={
            "arrangements": ArrangementSerializer(get_arrangement_list_for_team(team), many=True).data})
    else:
        return Response(status=403, data={"message": "No Team Info given!"})
