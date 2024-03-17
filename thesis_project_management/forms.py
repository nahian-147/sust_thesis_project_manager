from users.models import Course, Student, Supervisor, Teacher
from .models import Team, TeamStudentMap
from django.forms import Form
from django import forms
from .team_utility_functions import get_all_teams_of_a_participant


class TeamCreationForm(Form):
    name = forms.CharField(max_length=100)
    year = forms.IntegerField()
    course = forms.ModelChoiceField(widget=forms.Select, queryset=Course.objects.all(), empty_label="Select Course")
    project_thesis_title = forms.CharField(max_length=300)
    students = forms.CharField(max_length=50)


class ArrangementParticipationForm(Form):
    team = forms.ChoiceField(choices=[])

    def __init__(self, team_list: list, *args, **kwargs):
        super(ArrangementParticipationForm, self).__init__(*args, **kwargs)
        self.fields['team'].choices = team_list


class AssignSupervisorForm(Form):
    supervisor_1 = forms.ModelChoiceField(widget=forms.Select, queryset=Teacher.objects.all(), empty_label="Select Supervisor")
    supervisor_2 = forms.ModelChoiceField(widget=forms.Select, queryset=Teacher.objects.all(), empty_label="Select Supervisor")
    supervisor_3 = forms.ModelChoiceField(widget=forms.Select, queryset=Teacher.objects.all(), empty_label="Select Supervisor")

