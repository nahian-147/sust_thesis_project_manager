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


class Arrangement(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField()


class Participation(models.Model):
    id = models.BigAutoField(primary_key=True)
