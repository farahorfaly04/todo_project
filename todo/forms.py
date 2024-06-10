from django import forms
from .modelsAPI import TaskAPI

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskAPI
        fields = ['title', 'description', 'completed']
