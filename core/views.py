from datetime import datetime
import os
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from backend import settings
from core.forms import CoursesForm, HomeworkAssignmentForm, HomeworkSubmissionForm, RemarkForm, StudentSearchForm
from .decorators import allowed_users
from .models import Absences, Announcements, Calendars, Classroom, Courses, CustomUser, Grade, HomeworkAssignment, HomeworkSubmission, Calendars, LEVEL_CHOICES, Student, TRIMESTER_CHOICES
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from collections import namedtuple
from django.db.models import Q
from django.db.models import Count





def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    if request.user.user_type == 'teacher':
        template_name = 'core/teacher/teacher_dashboard.html'
    elif request.user.user_type == 'student':
        template_name = 'core/student/student_dashboard.html'
    elif request.user.user_type == 'parent':
        template_name = 'core/parent/parent_dashboard.html'
    elif request.user.is_staff or request.user.is_superuser:
        return redirect(reverse('admin:index'))
    else:
        return redirect('home')

    return render(request, template_name)


allowed_users(allowed_roles=['STAFF'])
def assign_grades(request, classroom_id):
  
    return render(request, 'grades/assign_grades.html')


from django.http import HttpResponse

def about(request):
    context = {

    }
    return render(request, 'core/about_us.html', context)

def courses(request):
    return HttpResponse("Courses Page")

def services(request):
    context = {

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
            form= HomeworkAssignmentForm(request.POST, request.FILES,  request=request)
            if form.is_valid():
                homework = form.save(commit=False)
                homework.teacher = request.user.teacher
                homework.save()
                messages.success(request, 'Homework assignment created successfully')
                return redirect('homework_assignment')
            else:
                print(form.errors)
    else:
        form = HomeworkAssignmentForm( request=request)
    context = {
        'homework_assignments': homework_assignments,
        'form' : form
    }
    return render(request, 'core/teacher/teacher-homework.html', context)

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

    return render(request, 'core/teacher/teacher-submissions.html', context)

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
    return render(request, 'core/student/student-homework.html', context)



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

    return render(request, 'core/parent/parent-absences.html', context)
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
            if grades:  # Check if there are grades
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
                    average = total_weighted_grade / total_weight if total_weight == 1 else None
                    final_grade = average
                    if student.user.username not in grades_by_trimester[trimester]:
                        grades_by_trimester[trimester][student.user.username] = {}
                    grades_by_trimester[trimester][student.user.username][subject.name] = {'grades': grades_dict, 'average': average, 'final': final_grade}

                    if final_grade is not None:
                        total_coefficient += grade.subject.coefficient
                        total_weighted_final_grade += final_grade * grade.subject.coefficient
                trimester_average = total_weighted_final_grade / total_coefficient if total_coefficient > 0 else None
                grades_by_trimester[trimester][student.user.username]['trimester_average'] = trimester_average
            else:
                # If there are no grades, initialize the student's data with an empty dictionary
                grades_by_trimester[trimester][student.user.username] = {}

    context = {
        'grades_by_trimester': grades_by_trimester
    }

    return render(request, 'core/parent/parents-grades.html', context)

@allowed_users(allowed_roles=['STUDENTS'])
def get_grades_student(request):
    # Get the student user
    student_user = request.user

    # Get the Student instance
    student = student_user.student

    # Get the student's grades
    grades_by_trimester = {1: {}, 2: {}, 3: {}}
    for trimester in grades_by_trimester.keys():
        grades = Grade.objects.filter(student=student, trimester=trimester)
        if grades:  # Check if there are grades
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
                average = total_weighted_grade / total_weight if total_weight == 1 else None
                final_grade = average
                if student.user.username not in grades_by_trimester[trimester]:
                    grades_by_trimester[trimester][student.user.username] = {}
                grades_by_trimester[trimester][student.user.username][subject.name] = {'grades': grades_dict, 'average': average, 'final': final_grade}

                if final_grade is not None:
                    total_coefficient += grade.subject.coefficient
                    total_weighted_final_grade += final_grade * grade.subject.coefficient
            trimester_average = total_weighted_final_grade / total_coefficient if total_coefficient > 0 else None
            grades_by_trimester[trimester][student.user.username]['trimester_average'] = trimester_average
        else:
            # If there are no grades, initialize the student's data with an empty dictionary
            grades_by_trimester[trimester][student.user.username] = {}

    context = {
        'grades_by_trimester': grades_by_trimester
    }

    return render(request, 'core/student/student-grades.html', context)



@allowed_users(allowed_roles=['STUDENTS'])
def view_schedule_student(request):
    student = request.user.student
    classroom = student.classroom
    classroom_calendar = classroom.calendar

    # Get the current week's cafeteria menu and events calendars
    now = datetime.now().date()
    cafe_calendar = Calendars.objects.filter(calendar_type='CAFE', start_week__lte=now, end_week__gte=now).first()
    event_calendar = Calendars.objects.filter(calendar_type='EVENT', start_week__lte=now, end_week__gte=now).first()

    # Get the timeslots for each calendar
    classroom_timeslots = classroom_calendar.timeslots.all() if classroom_calendar else []
    cafe_timeslots = cafe_calendar.timeslots.all() if cafe_calendar else []
    event_timeslots = event_calendar.timeslots.all() if event_calendar else []

    # Create table data for each calendar
    classroom_table_data = _create_table_data(classroom_timeslots, 'CLASS')
    cafe_table_data = _create_table_data(cafe_timeslots, 'CAFE')
    event_table_data = _create_table_data(event_timeslots, 'EVENT')

    # Convert Python None to empty string
    classroom_table_data = [{k: v if v is not None else '' for k, v in d.items()} for d in classroom_table_data]
    cafe_table_data = [{k: v if v is not None else '' for k, v in d.items()} for d in cafe_table_data]
    event_table_data = [{k: v if v is not None else '' for k, v in d.items()} for d in event_table_data]

    # print(event_table_data) (debugging)
    return render(request, 'core/student/student-cal.html', {
        'classroom_table_data': classroom_table_data,
        'cafe_table_data': cafe_table_data,
        'event_table_data': event_table_data,
    })




def _create_table_data(timeslots, calendar_type):
    # Create a dictionary where the keys are the days of the week and the values are dictionaries
    # where the keys are the time ranges and the values are the content or subject
    table_data = {}
    for timeslot in timeslots:
        day = timeslot.get_day_display()
        time_range = timeslot.time_range
        if calendar_type == 'CLASS':
            value = timeslot.subject.name if timeslot.subject else ''
        else:
            value = timeslot.content
        if day not in table_data:
            table_data[day] = {}
        table_data[day][time_range] = value

    # Convert the dictionary to a list of dictionaries to make it easy to loop over in the template
    table_data_list = []
    for day, times in table_data.items():
        row = {'day': day}
        row.update(times)
        table_data_list.append(row)

    return table_data_list

@allowed_users(allowed_roles=['PARENTS'])
def view_schedule_parent(request):
    children = request.user.parent.children.all()

    # Get the current week's cafeteria menu and events calendars
    now = datetime.now().date()
    cafe_calendar = Calendars.objects.filter(calendar_type='CAFE', start_week__lte=now, end_week__gte=now).first()
    event_calendar = Calendars.objects.filter(calendar_type='EVENT', start_week__lte=now, end_week__gte=now).first()

    # Get the timeslots for each calendar
    cafe_timeslots = cafe_calendar.timeslots.all() if cafe_calendar else []
    event_timeslots = event_calendar.timeslots.all() if event_calendar else []

    # Create table data for each calendar
    cafe_table_data = _create_table_data(cafe_timeslots, 'CAFE')
    event_table_data = _create_table_data(event_timeslots, 'EVENT')

    # Convert Python None to empty string
    cafe_table_data = [{k: v if v is not None else '' for k, v in d.items()} for d in cafe_table_data]
    event_table_data = [{k: v if v is not None else '' for k, v in d.items()} for d in event_table_data]

    # Create table data for each child's classroom calendar
    children_table_data = {}
    for child in children:
        classroom = child.classroom
        classroom_calendar = classroom.calendar
        classroom_timeslots = classroom_calendar.timeslots.all() if classroom_calendar else []
        classroom_table_data = _create_table_data(classroom_timeslots, 'CLASS')
        classroom_table_data = [{k: v if v is not None else '' for k, v in d.items()} for d in classroom_table_data]
        children_table_data[child.user.username] = classroom_table_data

    return render(request, 'core/parent/parent-schedule.html', {
        'children_table_data': children_table_data,
        'cafe_table_data': cafe_table_data,
        'event_table_data': event_table_data,
    })


from django.db.models import Q

@allowed_users(allowed_roles=['TEACHERS'])
def teacher_courses(request):
    # Get the existing courses
    courses = Courses.objects.all()
    #and the teachers
    teachers = CustomUser.objects.filter(teacher__courses__in=courses).annotate(num_courses=Count('teacher__courses')).order_by('-num_courses')
    #and classrooms
    classrooms = Classroom.objects.filter(classroom__in=courses).annotate(num_classrooms=Count('classroom')).order_by('-num_classrooms')

    if request.method == 'POST':
        # Check if the delete button was clicked
        if 'delete' in request.POST:
            # Get the course to delete
            course_id = request.POST.get('course_id')
            course = get_object_or_404(Courses, id=course_id)
            # Check if the current user is the teacher who uploaded the course
            if course.teacher == request.user.teacher:
                # Delete the course
                course.delete()
                messages.success(request, 'Course deleted successfully')
            else:
                messages.error(request, 'You can only delete courses you have uploaded')
            return redirect('teacher_courses')
        else:
            form = CoursesForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)
                course.teacher = request.user.teacher
                course.save()
                messages.success(request, 'Course uploaded successfully')
                return redirect('teacher_courses')
            else:
                print(form.errors)
    else:
        form = CoursesForm()
        # Get the search query (returns None if no query)
        search_query = request.GET.get('search', None)
        level_query = request.GET.get('level', None)  # Get the level query
        teacher_query= request.GET.get('teacher', None)
        classroom_query = request.GET.get('classroom', None)


        # Get the courses that match the search query
        if search_query is None or search_query.lower() == 'all':
            courses = Courses.objects.all()
        else:
            courses = Courses.objects.filter(
                Q(title__icontains=search_query) | 
                Q(subject__icontains=search_query) | 
                Q(classroom__name__icontains=search_query)
            )

        # Filter the courses by level or by teacher
        if level_query is not None and level_query != '':
            courses = courses.filter(level=level_query)
        if teacher_query is not None and teacher_query != '':
           courses= courses.filter(teacher__user__username= teacher_query)
        if classroom_query is not None and classroom_query != '':
            courses = courses.filter(classroom__name=classroom_query)
    context = {
        'courses': courses,
        'form': form,
        'levels': LEVEL_CHOICES,
        'teachers': teachers,
        'classrooms':classrooms

    }
    return render(request, 'core/teacher/teacher-courses.html', context)
    


@login_required
def view_courses(request):
    # Get the existing courses
    courses = Courses.objects.all()

    #and the teachers
    teachers = CustomUser.objects.filter(teacher__courses__in=courses).annotate(num_courses=Count('teacher__courses')).order_by('-num_courses')

    #and classrooms
    classrooms = Classroom.objects.filter(classroom__in=courses).annotate(num_classrooms=Count('classroom')).order_by('-num_classrooms')

    # Get the search query (returns None if no query)
    search_query = request.GET.get('search', None)
    level_query = request.GET.get('level', None)  # Get the level query
    teacher_query= request.GET.get('teacher', None)
    classroom_query = request.GET.get('classroom', None)


    # Get the courses that match the search query
    if search_query is None or search_query.lower() == 'all':
        courses = Courses.objects.all()
    else:
        courses = Courses.objects.filter(
            Q(title__icontains=search_query) | 
            Q(subject__icontains=search_query) | 
            Q(classroom__name__icontains=search_query)
        )

    # Filter the courses by level
    if level_query is not None and level_query != '':
        courses = courses.filter(level=level_query)

    if teacher_query is not None and teacher_query != '':
        courses= courses.filter(teacher__user__username= teacher_query)
    if classroom_query is not None and classroom_query != '':
        courses = courses.filter(classroom__name=classroom_query)

    context = {
        'courses': courses,
        'levels': LEVEL_CHOICES ,
        'teachers': teachers,
        'classrooms': classrooms
    }
    return render(request, 'core/view_courses.html', context)

from django.db.models import Count

@allowed_users(allowed_roles=['STUDENTS'])
def student_courses(request):
    # Get the student's classroom
    classroom = request.user.student.classroom

    # Get the courses for the student's classroom
    courses = Courses.objects.filter(classroom=classroom)

    # Get the search query (returns None if no query)
    search_query = request.GET.get('search', None)
    teacher_query = request.GET.get('teacher', None)  # Get the teacher query

    # Get the courses that match the search query
    if search_query is not None and search_query.lower() != 'all':
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(subject__icontains=search_query)
        )


    # Filter the courses by teacher
    if teacher_query is not None and teacher_query != '':
        courses = courses.filter(teacher__user__username=teacher_query)

    # Get the teachers for the dropdown
    teachers = CustomUser.objects.filter(teacher__courses__in=courses).annotate(num_courses=Count('teacher__courses')).order_by('-num_courses')

    context = {
        'courses': courses,
        'teachers': teachers
    }
    return render(request, 'core/student/student-courses.html', context)





from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Remarks
from .forms import RemarkForm, StudentSearchForm

@allowed_users(allowed_roles=['TEACHERS'])
def teacher_remarks(request):
    # Get the remarks made by the current user
    remarks = Remarks.objects.filter(teacher=request.user.teacher)

    if request.method == 'POST':
        # Check if the delete button was clicked
        if 'delete' in request.POST:
            # Get the remark to delete
            remark_id = request.POST.get('remark_id')
            remark = get_object_or_404(Remarks, id=remark_id)
            # Check if the current user is the teacher who wrote the remark
            if remark.teacher == request.user.teacher:
                # Delete the remark
                remark.delete()
                messages.success(request, 'Remark deleted successfully')
            else:
                messages.error(request, 'Something Went Wrong Remark Wasn\'t Deleted')
            return redirect('teacher_remarks')
        else:
            form = StudentSearchForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                remark_form = RemarkForm(request.POST)
                if remark_form.is_valid():
                    remark = remark_form.save(commit=False)
                    remark.student = student
                    remark.teacher = request.user.teacher
                    remark.save()
                    messages.success(request, 'Remark created successfully')
                    return redirect('teacher_remarks')
    else:
        form = StudentSearchForm()
        remark_form = RemarkForm()

    context = {
        'form': form,
        'remark_form': remark_form,
        'remarks': remarks,
    }
    return render(request, 'core/teacher/teacher-remarks.html', context)

@allowed_users(allowed_roles=['PARENTS'])
def parent_remarks(request):
    # Get the children of the current user
    children = Student.objects.filter(parent=request.user.parent)

    # Get the remarks made to the children of the current user
    remarks = Remarks.objects.filter(student__in=children)

    context = {
        'remarks': remarks,
    }
    return render(request, 'core/parent/parent-remarks.html', context)