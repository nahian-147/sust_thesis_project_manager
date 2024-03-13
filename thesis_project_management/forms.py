from users.models import Course, Student
from .models import Team
from django.forms import Form
from django import forms


class TeamCreationForm(Form):

    course_queryset = Course.objects.all()
    student_queryset = Student.objects.all()

    name = forms.CharField(max_length=100)
    year = forms.IntegerField()
    course = forms.ModelChoiceField(widget=forms.Select, queryset=Course.objects.all(), empty_label="Select Course")
    project_thesis_title = forms.CharField(max_length=300)
    students = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=student_queryset)
