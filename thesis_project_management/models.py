from django.db import models


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
    department = models.ForeignKey(Department, related_name='course', on_delete=models.CASCADE)
    credit = models.FloatField()
    course_type = models.CharField(max_length=50)
    general_scope = models.JSONField(max_length=500)

    class Meta:
        unique_together = ('title', 'code', 'department')

    def __str__(self):
        return f'{self.code} credit: {self.credit}'


class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='teacher', on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    publications = models.JSONField(max_length=1500)

    class Meta:
        unique_together = ('name', 'department')

    def __str__(self):
        return f'{self.name} dept. {self.department}'


class Supervisor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='supervisor', on_delete=models.CASCADE, null=True)
    expertise = models.CharField(max_length=100)
    publications = models.JSONField(max_length=1500)

    def __str__(self):
        return f'{self.name} dept. {self.department}'


class Student(models.Model):
    registration = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='student', on_delete=models.CASCADE)

    def __str__(self):
        return f'name: {self.name} dept: {self.registration} reg: {self.registration}'


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    course = models.ForeignKey(Course, related_name='team', on_delete=models.CASCADE)
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

    class Meta:
        unique_together = ('course', 'year', 'odd_semester')


class Participation(models.Model):
    id = models.BigAutoField(primary_key=True)
    arrangement = models.ForeignKey(Arrangement, related_name='participation', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='participation', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500)
    result = models.CharField(max_length=20)
    artifacts = models.JSONField(max_length=200)

    class Meta:
        unique_together = ('arrangement', 'team')
