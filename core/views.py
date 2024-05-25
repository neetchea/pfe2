from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model
from .decorators import allowed_users
from .models import Announcements, Classroom, CustomUser,Grade
from django.core.exceptions import ObjectDoesNotExist


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


@allowed_users(allowed_roles=['PARENTS'])
def get_grades(request, parent_username):
    # Get the parent user
    CustomUser = get_user_model()
    parent_user = CustomUser.objects.get(username=parent_username)

    # Check if the CustomUser instance has an associated Parent instance
    if hasattr(parent_user, 'parent'):
        # Get the Parent instance
        parent = parent_user.parent

        # Get the students of the parent
        students = parent.children.all()

        # For each student, get their grades
        grades_list = []
        for student in students:
            # Get the CustomUser instance for the student
            student_user = student.user
            grades = Grade.objects.filter(student=student_user)
            for grade in grades:
                grades_list.append(f"Student: {student_user.username}, Subject: {grade.subject.name}, Grade: {grade.grade}")

        return HttpResponse('<br>'.join(grades_list))
    else:
        return HttpResponse("This user is not a parent.")





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

@allowed_users(allowed_roles=['STAFF','STUDENTS','TEACHERS','PARENTS'])
def user_announcements(request):
    announcements= Announcements.objects.filter(active=True)
    context ={'announcements': announcements}
    return render(request, 'core/user_announcements.html',context)
def visitor_announcements(request):
    announcements= Announcements.objects.filter(is_user_only=False, active=True)






def homework(request):
    return HttpResponse("This is the homework page.")

def my_calendars(request):
    return HttpResponse("This is the my calendars page.")

def courses(request):
    return HttpResponse("This is the courses page.")

def my_grades(request):
    return HttpResponse("This is the my grades page.")
