from .models import Student, Supervisor, Teacher, Participant
from django.contrib.auth.models import User
from users.models import Department
from django.core.exceptions import ObjectDoesNotExist


def bootstrap_a_participant(user: User, participant: Participant, participant_data: dict):
    participant.user = user
    participant.email = participant_data['email']
    participant.department = Department.objects.get(code=str(participant_data['department']).upper())
    participant.full_name = participant_data['full_name']
    return participant


def register_user_as_a_student(user: User, student_data: dict):
    try:
        student = Student.objects.get(user=user)
    except ObjectDoesNotExist:
        try:
            duplicate_student = Student.objects.get(registration=student_data['registration'])
            return None
        except ObjectDoesNotExist:
            student = bootstrap_a_participant(user, Student(), student_data)
    student.registration = student_data['registration']
    student.save()
    return student


def register_user_as_a_teacher(user: User, teacher_data: dict):
    try:
        teacher = Teacher.objects.get(user=user)
    except ObjectDoesNotExist:
        teacher = bootstrap_a_participant(user, Teacher(), teacher_data)
    teacher.expertise = teacher_data['expertise']
    teacher.publications = {
        "publications": teacher_data['publications']
    }
    teacher.save()
    return teacher


def register_user_as_a_supervisor(user: User, supervisor_data: dict):
    try:
        supervisor = Supervisor.objects.get(user=user)
    except ObjectDoesNotExist:
        supervisor = bootstrap_a_participant(user, Supervisor(), supervisor_data)
    supervisor.expertise = supervisor_data['expertise']
    supervisor.publications = {
        "publications": supervisor_data['publications']
    }
    supervisor.save()
    return supervisor
