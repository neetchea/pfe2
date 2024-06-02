from django import forms
from .models import Courses, Grade, HomeworkAssignment,HomeworkSubmission, Remarks, Student, Subject

class HomeworkAssignmentForm(forms.ModelForm):
    due_date = forms.DateField(input_formats=['%d-%m-%Y', '%Y-%m-%d'])

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(HomeworkAssignmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeworkAssignment
        fields = '__all__'
        exclude = ['teacher']

    def clean(self):
        cleaned_data = super().clean()
        teacher = self.request.user.teacher
        classroom = cleaned_data.get('classroom')
        subject = cleaned_data.get('subject')

        if classroom not in teacher.classrooms.all():
            self.add_error('classroom', "You do not teach this classroom.")

        if subject not in teacher.subjects.all():
            self.add_error('subject', "You do not teach this subject.")
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




from django import forms
from .models import Grade
from .models import TRIMESTER_CHOICES 

class GradeForm(forms.ModelForm):
    trimester = forms.ChoiceField(choices=TRIMESTER_CHOICES)

    class Meta:
        model = Grade
        fields = ['grade', 'grade_type', 'trimester']