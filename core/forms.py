from django import forms
from .models import HomeworkAssignment

class HomeworkAssignmentForm(forms.ModelForm):
    due_date = forms.DateField(input_formats=['%d-%m-%Y', '%Y-%m-%d'])
    class Meta:
        model = HomeworkAssignment
        fields = '__all__'
        exclude = ['teacher']
        