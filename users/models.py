from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    year_established = models.IntegerField()

    def __str__(self):
        return f'{self.name} since {self.year_established}'


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credit = models.FloatField()
    course_type = models.CharField(max_length=50)
    general_scope = models.JSONField(max_length=500)

    class Meta:
        unique_together = ('title', 'code', 'department')

    def __str__(self):
        return f'{self.code} credit: {self.credit}'


class Participant(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('full_name', 'department', 'email')

    def __str__(self):
        return f'{self.full_name}, {self.department.code} dept.'


class Teacher(Participant):
    expertise = models.CharField(max_length=100)


class Supervisor(Teacher):
    pass


class Student(Participant):
    registration = models.CharField(primary_key=True, max_length=12)
