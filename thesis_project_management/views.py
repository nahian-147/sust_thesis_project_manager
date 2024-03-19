import datetime
import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.service_functions import is_student, is_teacher
from .forms import TeamCreationForm, ArrangementParticipationForm, AssignSupervisorAndTitleForm, AddFeedbackForm
from .models import Team, Arrangement, TeamTeacherMap
from .serializers import ArrangementSerializer
from .team_utility_functions import create_team_from_dict, get_arrangement_list_for_team, \
    get_full_information_about_team, get_all_teams_of_a_participant, assign_team_to_arrangement, \
    get_all_teams_for_arrangement, add_supervisor_to_team, add_teacher_to_team, add_student_to_team, \
    add_feedback_to_team

logger = logging.getLogger('django')


def home(request):
    return render(request, 'thesis_project_management/home.html', {'title': 'Home'})


@login_required()
def create_team_ui(request):
    user = User.objects.get(username=request.user.username)
    is_student_decider = is_student(user)
    if is_student_decider[0]:
        student = is_student_decider[1]
    else:
        return redirect('profile')
    if request.method == 'GET':
        form = TeamCreationForm()
        form.data.setdefault('year', datetime.date.year)
        form.data.setdefault('students', student.registration)
        return render(request, 'thesis_project_management/create-team.html', {'title': 'Create Team', 'form': form})
    elif request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            student_list = str(form.cleaned_data.get('students')).replace(' ', '').split(',')
            if student.registration in student_list:
                team_info = {
                    'year': form.cleaned_data.get('year'),
                    'course': str(form.cleaned_data.get('course').code),
                    'name': form.cleaned_data.get('name'),
                    'project_thesis_proposal_1': form.cleaned_data.get('project_thesis_proposal_1'),
                    'project_thesis_proposal_2': form.cleaned_data.get('project_thesis_proposal_2'),
                    'project_thesis_proposal_3': form.cleaned_data.get('project_thesis_proposal_3'),
                    'student_list': student_list,
                }
                if create_team_from_dict(team_info=team_info):
                    messages.success(request, f'A Team has been created.')
                    return redirect('profile')
                else:
                    messages.warning(request, f'Some students are not available')
                    return render(request, 'thesis_project_management/create-team.html',
                                  {'title': 'Create Team', 'form': form})
            else:
                messages.warning(request, f'you must include your registration')
                return render(request, 'thesis_project_management/create-team.html',
                              {'title': 'Create Team', 'form': form})
        else:
            messages.warning(request, f'Invalid Form')
            return render(request, 'thesis_project_management/create-team.html',
                          {'title': 'Create Team', 'form': form})


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
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
@authentication_classes([TokenAuthentication, SessionAuthentication])
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


@login_required()
def team_detail_view(request):
    user = User.objects.get(username=request.user.username)
    team_id = int(request.GET['id'])
    try:
        team = Team.objects.get(id=team_id)
        team_info_full = get_full_information_about_team(team)
        return render(request, 'thesis_project_management/team-detail.html',
                      {'title': f'{team.name}-{team.year}-{team.course.code}', 'team_info_full': team_info_full})
    except ObjectDoesNotExist:
        messages.warning(request, 'Team does not Exist anymore')
        return redirect('profile')


@login_required()
def show_all_arrangements(request):
    user = User.objects.get(username=request.user.username)
    is_student_decider = is_student(user)
    if is_student_decider[0]:
        student = is_student_decider[1]
    else:
        student = None
    arrangements = Arrangement.objects.all()
    active_arrangements = list(filter(lambda a: a.active, arrangements))
    past_arrangements = list(filter(lambda a: not a.active, arrangements))
    return render(request, 'thesis_project_management/arrangements.html', {
        'title': 'Arrangements',
        'active_arrangements': active_arrangements,
        'past_arrangements': past_arrangements,
        'student': student
    })


@login_required()
def participate_arrangement(request):
    user = User.objects.get(username=request.user.username)
    is_student_decider = is_student(user)
    if is_student_decider[0]:
        student = is_student_decider[1]
    else:
        student = None
    arrangement_id = int(request.GET['id'])
    arrangement = Arrangement.objects.get(id=arrangement_id)
    all_teams_of_student = get_all_teams_of_a_participant(student)
    if all_teams_of_student:
        all_teams_of_student = list(
            filter(lambda t: t.course == arrangement.course, get_all_teams_of_a_participant(student)))
        teams = list(map(lambda t: (t.id, f'{t.name}-{t.course}'), all_teams_of_student))
    else:
        teams = [(-1, 'No team Found')]

    if request.method == 'GET':
        if student and arrangement.active:
            form = ArrangementParticipationForm(team_list=teams)
            return render(request, 'thesis_project_management/participate-arrangement.html', {
                'title': f'Participate {arrangement.course}',
                'form': form
            })
        else:
            messages.warning(request, 'Arrangement has been Expired!')
            return redirect('show_all_arrangements')
    elif request.method == 'POST':
        team_id = request.POST['team']
        if team_id and int(team_id) > 0:
            team = Team.objects.get(id=team_id)
            if assign_team_to_arrangement(arrangement, team):
                messages.success(request, f'Participation Succeeded')
                return redirect(reverse('team_detail') + f'?id={team.id}')
            else:
                messages.warning(request, f'Check your Team and try again')
                form = ArrangementParticipationForm(team_list=teams)
                return render(request, 'thesis_project_management/participate-arrangement.html', {
                    'title': f'Participate {arrangement.course}',
                    'form': form
                })
        else:
            messages.warning(request, f'Check your Team and try again')
            form = ArrangementParticipationForm(team_list=teams)
            return render(request, 'thesis_project_management/participate-arrangement.html', {
                'title': f'Participate {arrangement.course}',
                'form': form
            })


@login_required()
def view_arrangement(request):
    user = User.objects.get(username=request.user.username)
    is_teacher_decider = is_teacher(user)
    if is_teacher_decider[0]:
        teacher = is_teacher_decider[1]
    else:
        teacher = None
    arrangement_id = int(request.GET['id'])
    arrangement = Arrangement.objects.get(id=arrangement_id)
    participated_teams = get_all_teams_for_arrangement(arrangement)
    return render(request, 'thesis_project_management/arrangement-view.html', {
        'title': 'Arrangement view',
        'arrangement': arrangement,
        'participated_teams': participated_teams,
        'course_teacher': True if teacher is not None and teacher == arrangement.course_teacher else False
    })


@login_required()
def assign_supervisor(request):
    user = User.objects.get(username=request.user.username)
    team_id = int(request.GET['id'])
    team = Team.objects.get(id=team_id)
    is_teacher_decider = is_teacher(user)
    if is_teacher_decider[0]:
        teacher = is_teacher_decider[1]
    else:
        teacher = None
    if teacher is None:
        messages.warning(request, 'Access to that page is reserved for Course Teacher only')
        return redirect('show_all_arrangements')
    else:
        try:
            course_teacher_team_map = TeamTeacherMap.objects.get(team=team, teacher=teacher)
        except ObjectDoesNotExist:
            messages.warning(request, 'Access to that page is reserved for Course Teacher only')
            return redirect('show_all_arrangements')
    if request.method == 'GET':
        form = AssignSupervisorAndTitleForm()
        return render(request, 'thesis_project_management/assign-supervisors.html', {
            'title': f'Assign supervisor',
            'form': form,
            'team': team
        })
    elif request.method == 'POST':
        form = AssignSupervisorAndTitleForm(request.POST)
        if form.is_valid():
            selected_title = form.cleaned_data['selected_title']
            team.project_thesis_title = selected_title
            team.save()
            supervisor_1 = form.cleaned_data['supervisor_1']
            s1_success = add_supervisor_to_team(team, supervisor_1)
            supervisor_2 = form.cleaned_data['supervisor_2']
            s2_success = add_supervisor_to_team(team, supervisor_2)
            supervisor_3 = form.cleaned_data['supervisor_3']
            s3_success = add_supervisor_to_team(team, supervisor_3)
            if all([s1_success, s2_success, s3_success]):
                team.status = 'SUCCESSFULLY_REGISTERED'
                team.save()
                messages.success(request, f'Successfully Assigned Supervisors to the Team')
                return redirect(reverse('team_detail') + f'?id={team.id}')
            else:
                messages.warning(request, f'At least one supervisor is not available. Please check and try again')
                return render(request, 'thesis_project_management/assign-supervisors.html', {
                    'title': f'Assign supervisor',
                    'form': form,
                    'team': team
                })
        else:
            messages.warning(request, f'Invalid Form Submission')
            return render(request, 'thesis_project_management/assign-supervisors.html', {
                'title': f'Assign supervisor',
                'form': form,
                'team': team
            })


@login_required()
def give_feedback(request):
    user = User.objects.get(username=request.user.username)
    team_id = int(request.GET['id'])
    team = Team.objects.get(id=team_id)
    team_info_full = get_full_information_about_team(team)
    is_teacher_decider = is_teacher(user)
    if is_teacher_decider[0]:
        teacher = is_teacher_decider[1]
    else:
        teacher = None
    if teacher is None:
        messages.warning(request, 'Access to that page is reserved for Course Teacher only')
        return redirect('show_all_arrangements')
    else:
        try:
            course_teacher_team_map = TeamTeacherMap.objects.get(team=team, teacher=teacher)
        except ObjectDoesNotExist:
            messages.warning(request, 'Access to that page is reserved for Course Teacher only')
            return redirect('show_all_arrangements')
    if request.method == 'GET':
        form = AddFeedbackForm()
        return render(request, 'thesis_project_management/update-team-feedback.html', {
            'title': f'Assign supervisor',
            'form': form,
            'team_info_full': team_info_full,
            'team': team
        })
    elif request.method == 'POST':
        form = AddFeedbackForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data['result']
            progress = form.cleaned_data['progress']
            remarks = form.cleaned_data['remarks']
            closed = form.cleaned_data['closed']
            if add_feedback_to_team(team, {
                "result": result,
                "progress": progress,
                "remarks": remarks,
                "closed": closed
            }):
                messages.success(request, f'Successfully Added Feedback')
                return redirect(reverse('team_detail') + f'?id={team.id}')
        else:
            messages.warning(request, f'Operation could not be performed, Please try again')
            return render(request, 'thesis_project_management/update-team-feedback.html', {
                'title': f'Assign supervisor',
                'form': form,
                'team_info_full': team_info_full,
                'team': team
            })
