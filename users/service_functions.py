from .models import *
from django.core.exceptions import ObjectDoesNotExist


def is_student(user: User):
    student = None
    try:
        student = Student.objects.get(user=user)
        return True, student
    except ObjectDoesNotExist:
        return False, student


def is_teacher(user: User):
    teacher = None
    try:
        teacher = Teacher.objects.get(user=user)
        return True, teacher
    except ObjectDoesNotExist:
        return False, teacher
