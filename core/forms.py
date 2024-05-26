from django import forms
from .models import HomeworkAssignment,HomeworkSubmission

class HomeworkAssignmentForm(forms.ModelForm):
    due_date = forms.DateField(input_formats=['%d-%m-%Y', '%Y-%m-%d'])
    class Meta:
        model = HomeworkAssignment
        fields = '__all__'
        exclude = ['teacher']
class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['response', 'submission_file']    