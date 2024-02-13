from django.db import models
from users.models import Course, Teacher


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    project_thesis_title = models.CharField(max_length=300)
    students = models.JSONField(max_length=100)
    assigned_teachers = models.JSONField(max_length=100)
    assigned_supervisors = models.JSONField(max_length=100)
    status = models.JSONField(max_length=50)
    all_links = models.JSONField(max_length=2500)

    class Meta:
        unique_together = ('name', 'year', 'course')

    def __str__(self):
        return f'team: {self.name} of year: {self.year}'


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
    year = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    odd_semester = models.BooleanField()
    course_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'year', 'odd_semester')


class Participation(models.Model):
    id = models.BigAutoField(primary_key=True)
    arrangement = models.ForeignKey(Arrangement, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500)
    result = models.CharField(max_length=20)
    artifacts = models.JSONField(max_length=200)

    class Meta:
        unique_together = ('arrangement', 'team')
