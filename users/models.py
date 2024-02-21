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


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    publications = models.JSONField(max_length=1500)
    USERNAME_FIELD = 'email'

    class Meta:
        unique_together = ('username', 'department')

    def __str__(self):
        return f'{self.username} dept. {self.department}'


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    expertise = models.CharField(max_length=100)
    publications = models.JSONField(max_length=1500)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.username} dept. {self.department}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'name: {self.username} dept: {self.department} reg: {self.registration}'
