from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .decorators import allowed_users
from .models import Classroom, CustomUser,Grade


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

@allowed_users(allowed_roles=['STUDENTS'])
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

# @allowed_users(allowed_roles=['PARENTS'])
# def parents_grades_view(request):
#     relationships = ParentChildRelationship.objects.filter(parent=request.user)
#     children_grades = {}
#     for relationship in relationships:
#         child = relationship.child
#         subjects = child.subjects.all()
#         grades = []
#         for subject in subjects:
#             try:
#                 grade = subject.grades.get(student=child)
#                 grades.append(grade)
#             except ObjectDoesNotExist:
#                 grades.append(None)
#         children_grades[child] = grades
    
#     context = {
#         'children_grades': children_grades
#     }
#     return render(request, 'grades/parents_grades.html', context)

allowed_users(allowed_roles=['STAFF'])
def assign_grades(request, classroom_id):
  
    return render(request, 'grades/assign_grades.html')


from django.http import HttpResponse

def about(request):
    return HttpResponse("About Page")

def courses(request):
    return HttpResponse("Courses Page")

def services(request):
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
    }
    return render(request, 'core/services.html', context)

def contact(request):
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
    }
    return render(request, 'core/contact.html', context)





from django.http import HttpResponse

def homework(request):
    return HttpResponse("This is the homework page.")

def my_calendars(request):
    return HttpResponse("This is the my calendars page.")

def courses(request):
    return HttpResponse("This is the courses page.")

def my_grades(request):
    return HttpResponse("This is the my grades page.")
