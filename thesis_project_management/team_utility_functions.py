from users.models import Participant
from .models import *
import logging

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


def add_participant_to_team(team: Team, participant: Participant):
    if type(participant) is Student:
        team_student_map = TeamStudentMap()
        team_student_map.team = team
        team_student_map.student = participant
        if 'students' in team.students:
            team.students['students'].append(participant.email)
        else:
            team.students['students'] = [participant.email]
        team.save()
        team_student_map.save()
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
