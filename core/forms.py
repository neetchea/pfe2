from django import forms
from .models import Courses, HomeworkAssignment,HomeworkSubmission, Remarks, Student

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
class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'
        exclude = ['teacher']


class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remarks
        fields = '__all__'
        exclude =['teacher','student']

class StudentSearchForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())