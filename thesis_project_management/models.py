import datetime

import django
from django.db import models
from users.models import Course, Teacher, Supervisor, Student


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    project_thesis_title = models.CharField(max_length=300, blank=True, null=True)
    project_thesis_proposal_1 = models.CharField(max_length=300)
    project_thesis_proposal_2 = models.CharField(max_length=300)
    project_thesis_proposal_3 = models.CharField(max_length=300)
    students = models.JSONField(max_length=100, default=dict)
    assigned_teachers = models.JSONField(max_length=100, default=dict)
    assigned_supervisors = models.JSONField(max_length=100, default=dict)
    status = models.CharField(max_length=50, null=True, default='UNASSIGNED')

    class Meta:
        unique_together = ('name', 'year', 'course')

    def __str__(self):
        return f'{self.name} of year: {self.year} for course {self.course}'


class TeamStudentMap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team}'


class TeamSupervisorMap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.name}-{self.supervisor}'


class TeamTeacherMap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.name}-{self.teacher}'


class TeamProgress(models.Model):
    id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    last_updated = models.DateTimeField()
    total_progress = models.FloatField(default=0.0)


class Arrangement(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField(default=django.utils.timezone.now().date().year)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    odd_semester = models.BooleanField()
    course_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    begin_date = models.DateField(default=django.utils.timezone.now)
    end_date = models.DateField(
        default=datetime.datetime.fromtimestamp(django.utils.timezone.now().timestamp() + 3600 * 24 * 30 * 8).date())
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('course', 'year', 'odd_semester')

    def __str__(self):
        return f'{self.course} of year: {self.year} odd semester {self.odd_semester}'


class TeamParticipation(models.Model):
    id = models.BigAutoField(primary_key=True)
    arrangement = models.ForeignKey(Arrangement, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    result = models.CharField(max_length=20, null=True, blank=True)
    artifacts = models.JSONField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = ('arrangement', 'team')

    def __str__(self):
        return f'team: {self.team.name} for arrangement {self.arrangement} result {self.result}'
