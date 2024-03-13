import datetime

import django
from django.db import models
from users.models import Course, Teacher, Supervisor, Student


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    project_thesis_title = models.CharField(max_length=300)
    students = models.JSONField(max_length=100, default=dict)
    assigned_teachers = models.JSONField(max_length=100, default=dict)
    assigned_supervisors = models.JSONField(max_length=100, default=dict)
    status = models.CharField(max_length=50, null=True, default='UNASSIGNED')
    all_links = models.JSONField(max_length=2500, default=dict)

    class Meta:
        unique_together = ('name', 'year', 'course')

    def __str__(self):
        return f'team: {self.name} of year: {self.year} for course {self.course}'


class TeamStudentMap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'team: {self.team.name} for arrangement {self.student}'


class TeamSupervisorMap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)

    def __str__(self):
        return f'team: {self.team.name} for arrangement {self.supervisor}'


class TeamTeacherMap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'team: {self.team.name} for arrangement {self.teacher}'


class TeamProgress(models.Model):
    id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    last_updated = models.DateTimeField()
    total_progress = models.FloatField()
    meta = models.JSONField(max_length=2500)
    milestones = models.JSONField(max_length=1500)
    timeline = models.JSONField(max_length=500)


class Arrangement(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField(default=django.utils.timezone.now().date().year)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    odd_semester = models.BooleanField()
    course_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    begin_date = models.DateField(default=django.utils.timezone.now)
    end_date = models.DateField(default=datetime.datetime.fromtimestamp(django.utils.timezone.now().timestamp()+3600*24*30*8).date())
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('course', 'year', 'odd_semester')

    def __str__(self):
        return f'{self.course} of year: {self.year} odd semester {self.odd_semester}'


class TeamParticipation(models.Model):
    id = models.BigAutoField(primary_key=True)
    arrangement = models.ForeignKey(Arrangement, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500)
    result = models.CharField(max_length=20)
    artifacts = models.JSONField(max_length=200)

    class Meta:
        unique_together = ('arrangement', 'team')

    def __str__(self):
        return f'team: {self.team.name} for arrangement {self.arrangement} result {self.result}'
