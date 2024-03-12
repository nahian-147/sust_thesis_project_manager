from django.core.exceptions import ObjectDoesNotExist

from users.models import Participant
from .models import *
import logging
from datetime import datetime

logger = logging.getLogger('django')


def get_all_participant_of_team(team: Team) -> dict:
    students = list(map(lambda tsm: tsm.student, TeamStudentMap.objects.filter(team=team)))
    logger.info(f"found {len(students)} for the team {team}. regs: {list(map(lambda s: s.registration, students))}")

    teachers = list(map(lambda ttm: ttm.teacher, TeamTeacherMap.objects.filter(team=team)))
    logger.info(f"found {len(teachers)} for the team {team}. regs: {list(map(lambda t: t.email, teachers))}")

    supervisors = list(map(lambda tsm: tsm.supervisor, TeamSupervisorMap.objects.filter(team=team)))
    logger.info(f"found {len(supervisors)} for the team {team}. regs: {list(map(lambda s: s.email, supervisors))}")
    return {
        'teachers': teachers,
        'supervisors': supervisors,
        'students': students
    }


def get_all_teams_of_a_participant(participant: Participant) -> list[Team]:
    teams = None
    _map = None
    logger.info(f'found {type(participant)}')
    if type(participant) is Student:
        _map = TeamStudentMap.objects.filter(student=participant)
    elif type(participant) is Supervisor:
        _map = TeamSupervisorMap.objects.filter(supervisor=participant)
    elif type(participant) is Teacher:
        _map = TeamTeacherMap.objects.filter(teacher=participant)
    if _map:
        teams = list(map(lambda m: m.team, _map))
        logger.info(
            f"found {len(teams)} for the participant {participant}. titles: {list(map(lambda t: t.project_thesis_title, teams))}")
    return teams


def add_participant_to_team(team: Team, participant: Participant) -> bool:
    if type(participant) is Student:
        all_related_teams = get_all_teams_of_a_participant(participant)
        if team.students is None:
            team.students = {
                "students": []
            }
        if not all_related_teams or not any(
                [team.year == _.year and team.course == _.course for _ in all_related_teams]):
            team_student_map = TeamStudentMap()
            team_student_map.team = team
            team_student_map.student = participant
            if team.students is not None and 'students' in team.students:
                team.students['students'].append(participant.registration)
            else:
                team.students['students'] = [participant.registration]
            team.save()
            team_student_map.save()
        else:
            return False
    elif type(participant) is Supervisor:
        team_supervisor_map = TeamSupervisorMap()
        team_supervisor_map.team = team
        team_supervisor_map.supervisor = participant
        if 'supervisors' in team.assigned_supervisors:
            team.students['supervisors'].append(participant.email)
        else:
            team.students['supervisors'] = [participant.email]
        team.save()
        team_supervisor_map.save()
    elif type(participant) is Teacher:
        team_teacher_map = TeamTeacherMap()
        team_teacher_map.team = team
        team_teacher_map.teacher = participant
        if 'teachers' in team.assigned_teachers:
            team.students['teachers'].append(participant.email)
        else:
            team.students['teachers'] = [participant.email]
        team.save()
        team_teacher_map.save()
    return True


def create_team_from_dict(team_info: dict):
    year = team_info['year'] if 'year' in team_info else datetime.now().date().year
    course = Course.objects.get(code=team_info['course'])
    try:
        team = Team.objects.get(name=team_info['name'], year=year, course=course)
    except ObjectDoesNotExist:
        team = Team()
    team.name = team_info['name']
    team.year = year
    team.project_thesis_title = team_info['project_thesis_title']
    team.course = course
    student_list = map(lambda r: Student.objects.get(registration=r['registration']), team_info['student_list'])
    team.save()
    return all([add_participant_to_team(team, student) for student in student_list])


def get_arrangement_list_for_team(team: Team) -> list[Arrangement]:
    return list(filter(lambda a: a.end_date > datetime.now().date() and a.active, Arrangement.objects.filter(course=team.course, year=team.year)))
