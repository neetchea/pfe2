from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import allowed_users
from .models import Classroom, ParentChildRelationship, StudentInClassroom, Grade, Subject


def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    if request.user.user_type == 'teacher':
        template_name = 'core/teacher_dashboard.html'
    elif request.user.user_type == 'student':
        template_name = 'core/student_dashboard.html'
    elif request.user.user_type == 'parent':
        template_name = 'core/parent_dashboard.html'
    elif request.user.is_staff or request.user.is_superuser:
        return redirect(reverse('admin:index'))
    else:
        return redirect('home')

    return render(request, template_name)

from django.core.exceptions import ObjectDoesNotExist

@allowed_users(allowed_roles=['ELEVES'])
def students_grades_view(request):
    subjects = request.user.subjects.all()
    grades = []
    for subject in subjects:
        try:
            grade = subject.grades.get(student=request.user)
            grades.append(grade)
        except ObjectDoesNotExist:
            # Handle the case where there's no grade for a subject
             grade = None
             grades.append((subject, grade))
    
    context = {
        'grades': grades
    }
    return render(request, 'grades/students_grades.html', context)


from django.shortcuts import render
from .models import ParentChildRelationship

@allowed_users(allowed_roles=['PARENTS'])
def parents_grades_view(request):
    relationships = ParentChildRelationship.objects.filter(parent=request.user)
    children_grades = {}
    for relationship in relationships:
        child = relationship.child
        subjects = child.subjects.all()
        grades = []
        for subject in subjects:
            try:
                grade = subject.grades.get(student=child)
                grades.append(grade)
            except ObjectDoesNotExist:
                grades.append(None)
        children_grades[child] = grades
    
    context = {
        'children_grades': children_grades
    }
    return render(request, 'grades/parents_grades.html', context)

from django.http import HttpResponse

def about(request):
    return HttpResponse("About Page")

def courses(request):
    return HttpResponse("Courses Page")

def services(request):
    return HttpResponse("Services Page")

def contact(request):
    return HttpResponse("Contact Page")
from django.shortcuts import render
from .decorators import allowed_users

from django.shortcuts import render
from .decorators import allowed_users

@allowed_users(allowed_roles=['STAFF'])
def assign_grades(request, classroom_id):
    # Fetch the classroom based on the provided id
    classroom = Classroom.objects.get(id=classroom_id)

    # Fetch the StudentInClassroom instances for the classroom
    student_in_classroom_instances = classroom.studentinclassroom_set.all()

    # Fetch the students in the classroom
    students = [instance.student for instance in student_in_classroom_instances]

    # Fetch the subjects in the classroom
    subjects = classroom.subjects.all()

    # Render the 'assign_grades.html' template and pass the classroom, students, and subjects to it
    return render(request, 'grades/assign_grades.html', {'classroom': classroom, 'students': students, 'subjects': subjects})