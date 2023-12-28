from django.db import models


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    year_established = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, related_name='course', on_delete=models.CASCADE)
    credit = models.FloatField()
    course_type = models.CharField(max_length=50)
    general_scope = models.JSONField(max_length=500)


class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='teacher', on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    publications = models.JSONField(max_length=1500)


class Supervisor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='supervisor', on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    publications = models.JSONField(max_length=1500)


class Student(models.Model):
    registration = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='student', on_delete=models.CASCADE)


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    team_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='team', on_delete=models.CASCADE)
    project_thesis_title = models.CharField(max_length=300)
    students = models.JSONField(max_length=100)
    assigned_teachers = models.JSONField(max_length=100)
    assigned_supervisors = models.JSONField(max_length=100)
    status = models.JSONField(max_length=50)
    all_links = models.JSONField(max_length=2500)


class TeamProgress(models.Model):
    id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, related_name='team_progress', on_delete=models.CASCADE)
    last_updated = models.DateTimeField()
    total_progress = models.FloatField()
    meta = models.JSONField(max_length=2500)
    milestones = models.JSONField(max_length=1500)
    timeline = models.JSONField(max_length=500)


class Arrangement(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField()
    course = models.ForeignKey(Course, related_name='arrangement', on_delete=models.CASCADE)
    odd_semester = models.BooleanField()
    course_teacher = models.ForeignKey(Teacher, related_name='arrangement', on_delete=models.CASCADE)


class Participation(models.Model):
    id = models.BigAutoField(primary_key=True)
    arrangement = models.ForeignKey(Team, related_name='participation', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='participation', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500)
    result = models.CharField(max_length=20)
    artifacts = models.JSONField(max_length=200)
