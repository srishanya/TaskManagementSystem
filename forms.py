from django import forms
from .models import Project, ProjectMember, Sprint

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['user', 'role']

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name', 'goal', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
