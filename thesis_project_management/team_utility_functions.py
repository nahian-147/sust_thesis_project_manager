from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
    if len(_map) > 0:
        teams = list(map(lambda m: m.team, _map))
        logger.info(
            f"found {len(teams)} for the participant {participant}. titles: {list(map(lambda t: t.project_thesis_title, teams))}")
        return teams
    else:
        return None


def add_student_to_team(team: Team, student: Student) -> bool:
    if type(student) is Student:
        all_related_teams = get_all_teams_of_a_participant(student)
        if team.students is None:
            team.students = {
                "students": []
            }
        if not all_related_teams or not any(
                [team.year == _.year and team.course == _.course for _ in all_related_teams]):
            team_student_map = TeamStudentMap()
            team_student_map.team = team
            team_student_map.student = student
            if team.students is not None and 'students' in team.students:
                team.students['students'].append(student.registration)
            else:
                team.students['students'] = [student.registration]
            team.save()
            team_student_map.save()
            return True
        else:
            return False
    else:
        return False


def add_teacher_to_team(team: Team, teacher: Teacher) -> bool:
    if type(teacher) is Teacher:
        team_teacher_map = TeamTeacherMap()
        team_teacher_map.team = team
        team_teacher_map.teacher = teacher
        if 'teachers' in team.assigned_teachers:
            team.assigned_teachers['teachers'].append(teacher.email)
        else:
            team.assigned_teachers['teachers'] = [teacher.email]
        team.save()
        team_teacher_map.save()
        return True
    else:
        return False


def add_supervisor_to_team(team: Team, supervisor: Supervisor) -> bool:
    if type(supervisor) is Supervisor:
        try:
            team_supervisor_map = TeamSupervisorMap.objects.get(team=team, supervisor=supervisor)
            return True
        except ObjectDoesNotExist:
            team_supervisor_map = TeamSupervisorMap()
            team_supervisor_map.team = team
            team_supervisor_map.supervisor = supervisor
            if 'supervisors' in team.assigned_supervisors:
                team.assigned_supervisors['supervisors'].append(supervisor.email)
            else:
                team.assigned_supervisors['supervisors'] = [supervisor.email]
            team.save()
            team_supervisor_map.save()
            return True
        except MultipleObjectsReturned:
            return True
    else:
        return False


def get_student_from_registration_number(registration_number: str):
    try:
        student = Student.objects.get(registration=registration_number)
        return student
    except ObjectDoesNotExist:
        return None


def create_team_from_dict(team_info: dict):
    year = team_info['year'] if 'year' in team_info else datetime.now().date().year
    course = Course.objects.get(code=team_info['course'])
    try:
        team = Team.objects.get(name=team_info['name'], year=year, course=course)
    except ObjectDoesNotExist:
        team = Team()
    team.name = team_info['name']
    team.year = year
    team.project_thesis_proposal_1 = team_info['project_thesis_proposal_1']
    team.project_thesis_proposal_2 = team_info['project_thesis_proposal_2']
    team.project_thesis_proposal_3 = team_info['project_thesis_proposal_3']
    team.course = course
    student_list = list(map(get_student_from_registration_number, team_info['student_list']))
    logger.info(student_list)
    team_progress = TeamProgress()
    team_progress.team = team
    team_progress.total_progress = 0.0
    team_progress.last_updated = datetime.date
    try:
        team.save()
        team_progress.save()
        if all(student_list):
            return all([add_student_to_team(team, student) for student in student_list])
        else:
            return False
    except Exception as e:
        return False


def get_arrangement_list_for_team(team: Team) -> list[Arrangement]:
    return list(filter(lambda a: a.end_date > datetime.now().date() and a.active,
                       Arrangement.objects.filter(course=team.course, year=team.year)))


def get_full_information_about_team(team: Team) -> dict:
    team_info_full = dict()

    teachers = TeamTeacherMap.objects.filter(team=team)
    if len(teachers) >= 1:
        team_info_full['teachers'] = str(list(map(lambda t: t.teacher.full_name, teachers))).replace('[', '').replace(
            ']', '').replace("'", '')
    else:
        team_info_full['teachers'] = ''

    supervisors = TeamSupervisorMap.objects.filter(team=team)
    if len(supervisors) >= 1:
        team_info_full['supervisors'] = str(list(map(lambda s: s.supervisor.full_name, supervisors))).replace('[',
                                                                                                              '').replace(
            ']', '').replace("'", '')
    else:
        team_info_full['supervisors'] = ''

    students = TeamStudentMap.objects.filter(team=team)
    if len(students) >= 1:
        team_info_full['students'] = str(
            list(map(lambda s: f'{s.student.full_name} - {s.student.registration}', students))).replace('[',
                                                                                                        '').replace(']',
                                                                                                                    '').replace(
            "'", '')
    else:
        team_info_full['students'] = ''

    try:
        team_progress = TeamProgress.objects.get(team=team)
    except ObjectDoesNotExist:
        team_progress = TeamProgress()
        team_progress.team = team
        team_progress.last_updated = datetime.now()
        team_progress.total_progress = 0.0
        team_progress.save()

    try:
        team_participation = TeamParticipation.objects.get(team=team)
    except ObjectDoesNotExist:
        team_participation = None

    team_info_full['course'] = str(team.course)
    team_info_full['name'] = str(team.name)
    team_info_full['year'] = str(team.year)
    team_info_full['title'] = str(team.project_thesis_title)
    team_info_full['status'] = str(team.status)
    team_info_full['progress'] = str(team_progress.total_progress)
    team_info_full['last_updated'] = str(team_progress.last_updated)
    if team_participation is not None:
        team_info_full['result'] = str(team_participation.result)
        team_info_full['remarks'] = str(team_participation.remarks)
    else:
        team_info_full['result'] = 'N/A'
        team_info_full['remarks'] = 'N/A'

    logger.info(f'found team detail {team_info_full}')
    return team_info_full


def assign_team_to_arrangement(arrangement: Arrangement, team: Team) -> bool:
    try:
        team_participation = TeamParticipation.objects.get(arrangement=arrangement, team=team)
        return True
    except ObjectDoesNotExist:
        team_participation = TeamParticipation()
        if team.course == arrangement.course and team.year == arrangement.year:
            team_participation.team = team
            team_participation.arrangement = arrangement
            team.status = 'ASSIGNED'
            team.save()
            teacher_assignment = add_teacher_to_team(team, arrangement.course_teacher)
            team_participation.result = 'PENDING'
            team_participation.artifacts = None
            team_participation.save()
            team.assigned_teachers = {"COURSE_TEACHER": arrangement.course_teacher.full_name}
            team.save()
            try:
                team_progress = TeamProgress.objects.get(team=team)
                team_progress.total_progress = 0.1
            except ObjectDoesNotExist:
                team_progress = TeamProgress()
                team_progress.team = team
                team_progress.last_updated = datetime.now()
                team_progress.total_progress = 0.1
                team_progress.save()
            return True and teacher_assignment
        else:
            return False


def get_all_teams_for_arrangement(arrangement: Arrangement) -> list[Team]:
    participation = TeamParticipation.objects.filter(arrangement=arrangement)
    teams = list(map(lambda p: p.team, participation))
    return teams


def add_feedback_to_team(team: Team, feedback: dict):
    try:
        team_progress = TeamProgress.objects.get(team=team)
        team_progress.total_progress = float(feedback['progress'])
        team_progress.last_updated = datetime.now()
        team_progress.save()
    except ObjectDoesNotExist:
        team_progress = TeamProgress()
        team_progress.team = team
        team_progress.last_updated = datetime.now()
        team_progress.total_progress = 0.1
        team_progress.save()
    try:
        team_participation = TeamParticipation.objects.get(team=team)
        team_participation.result = feedback['result']
        team_participation.remarks = feedback['remarks']
        team_participation.save(0)
    except ObjectDoesNotExist:
        team_participation = None
        return False
    if feedback['closed']:
        team.status = 'CLOSED'
        team.save()
    return True
