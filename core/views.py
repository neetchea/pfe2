from collections import defaultdict
import os
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model

from backend import settings
from core.forms import HomeworkAssignmentForm, HomeworkSubmissionForm
from .decorators import allowed_users
from .models import Absences, Announcements, Classroom, CustomUser,Grade, HomeworkAssignment, HomeworkSubmission
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
def announcements(request):
    if request.user.is_authenticated:
        # Authenticated users
        announcements = Announcements.objects.filter(active=True)
    else:
        # Visitors
        announcements = Announcements.objects.filter(is_user_only=False, active=True)
    
    context = {'announcements': announcements}
    return render(request, 'core/user_announcements.html', context)

def homework(request):
    return HttpResponse("This is the homework page.")

def my_calendars(request):
    return HttpResponse("This is the my calendars page.")

def courses(request):
    return HttpResponse("This is the courses page.")

def my_grades(request):
    return HttpResponse("This is the my grades page.")


from django.shortcuts import get_object_or_404

@allowed_users(allowed_roles=['TEACHERS'])
def homework_assignment(request):
    #getting the existing homework assignments
    homework_assignments = HomeworkAssignment.objects.filter(teacher=request.user.teacher)
    for hw in homework_assignments:
        print(os.path.join(settings.MEDIA_ROOT, str(hw.assignment_file)))    

    if request.method == 'POST':
        # Check if the delete button was clicked
        if 'delete' in request.POST:
            # Get the homework assignment to delete
            homework_id = request.POST.get('homework_id')
            homework_assignment = get_object_or_404(HomeworkAssignment, id=homework_id)
            # Delete the homework assignment
            homework_assignment.delete()
            messages.success(request, 'Homework assignment deleted successfully')
            return redirect('homework_assignment')
        else:
            form= HomeworkAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                homework = form.save(commit=False)
                homework.teacher = request.user.teacher
                homework.save()
                messages.success(request, 'Homework assignment created successfully')
                return redirect('homework_assignment')
            else:
                print(form.errors)
    else:
        form = HomeworkAssignmentForm()

    context = {
        'homework_assignments': homework_assignments,
        'form' : form
    }
    return render(request, 'core/teacher_homework.html', context)

@allowed_users(allowed_roles=['TEACHERS'])
def view_submissions(request):
    # Get all the homework assignments created by the current teacher
    homework_assignments = HomeworkAssignment.objects.filter(teacher=request.user.teacher)

    # Get all the submissions for those homework assignments
    submissions = HomeworkSubmission.objects.filter(homework__in=homework_assignments)

    context = {
        'homework_assignments': homework_assignments,
        'submissions': submissions,
    }

    return render(request, 'core/teacher_submissions.html', context)

@allowed_users(allowed_roles=['STUDENTS'])
def student_homeworks(request):
    student = request.user.student
    homework_assignments = HomeworkAssignment.objects.filter(classroom=student.classroom)
    if request.method == 'POST':
        if 'delete' in request.POST:
            submission_id = request.POST.get('submission_id')
            submission = get_object_or_404(HomeworkSubmission, id=submission_id, student=student)
            submission.delete()
            messages.success(request, 'Submission deleted successfully', extra_tags='delete')
            return redirect('homework_submission')
        else:
            form = HomeworkSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.student = student
                submission.homework = get_object_or_404(HomeworkAssignment, id=request.POST.get('homework_id'))
                try:
                    submission.save()
                except IntegrityError:
                    messages.error(request, 'You have already submitted this homework, if you want to change your submission delete your first submission', extra_tags='submit')
                messages.success(request, 'Homework submitted successfully', extra_tags='submit')
                return redirect('homework_submission')
    else:
        form = HomeworkSubmissionForm()
    context = {
        'homework_assignments': homework_assignments,
        'form': form
    }
    return render(request, 'core/student_homeworks.html', context)

from collections import namedtuple

@allowed_users(allowed_roles=['PARENTS'])
def parents_absences_view(request):
    parent = request.user.parent
    children = parent.children.all()

    AbsenceInfo = namedtuple('AbsenceInfo', ['child', 'absences', 'total', 'justified', 'unjustified'])

    absences_info = []

    for child in children:
        child_absences = Absences.objects.filter(student=child)
        total = child_absences.count()
        justified = child_absences.filter(is_justified=True).count()
        unjustified = child_absences.filter(is_justified=False).count()

        absences_info.append(AbsenceInfo(child, child_absences, total, justified, unjustified))

    context = {
        'absences_info': absences_info,
    }

    return render(request, 'core/parent_absences.html', context)


@allowed_users(allowed_roles=['PARENTS'])
def get_grades_parents(request):
    # Get the parent user
    parent_user = request.user

    # Get the Parent instance
    parent = parent_user.parent

    # Get the students of the parent
    students = parent.children.all()

    # For each student, get their grades
    grades_by_trimester = {1: {}, 2: {}, 3: {}}
    for student in students:
        for trimester in grades_by_trimester.keys():
            grades = Grade.objects.filter(student=student, trimester=trimester)
            subjects = set(grade.subject for grade in grades)
            total_coefficient= 0
            total_weighted_final_grade= 0
            for subject in subjects:
                subject_grades = [grade for grade in grades if grade.subject == subject]
                grades_dict = {}
                total_weight = 0
                total_weighted_grade = 0
                for grade in subject_grades:
                    grades_dict[grade.grade_type] = {'weight': grade.weight, 'grade': grade.grade}
                    total_weight += grade.weight
                    total_weighted_grade += grade.grade * grade.weight
                average = total_weighted_grade / total_weight if total_weight != 0 else None
                final_grade = round(average) if average is not None else None
                if student.user.username not in grades_by_trimester[trimester]:
                    grades_by_trimester[trimester][student.user.username] = {}
                grades_by_trimester[trimester][student.user.username][subject.name] = {'grades': grades_dict, 'average': average, 'final': final_grade}

                if final_grade is not None:
                    total_coefficient += grade.subject.coeffiecient
                    total_weighted_final_grade += final_grade * grade.subject.coeffiecient
            trimester_average = total_weighted_final_grade / total_coefficient if total_coefficient > 0 else None

            #if student has no grades assigned yet
            if student.user.username not in grades_by_trimester[trimester]:
                grades_by_trimester[trimester][student.user.username] = {'grades': [], 'average': None, 'final': None, 'trimester_average': None}        
            else:
                grades_by_trimester[trimester][student.user.username]['trimester_average'] = trimester_average
                
    context = {
        'grades_by_trimester': grades_by_trimester
    }

    return render(request, 'grades/parents_grades.html', context)