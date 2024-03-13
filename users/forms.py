from django.forms import Form
from django import forms


class StudentRegistrationForm(Form):
    full_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    department = forms.CharField(max_length=10)
    registration = forms.CharField(max_length=12)
