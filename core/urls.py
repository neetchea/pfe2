
from django.urls import path
from django.contrib.auth import views as auth_views

from backend import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.announcements, name='events'),
    path('calendars/', views.my_calendars, name='my_calendars'),
    path('grades/', views.my_grades, name='grades'),
   
    path('assign-grades/<int:classroom_id>/change/', views.assign_grades, name='assign-grades'),
    path('homework_assignment/', views.homework_assignment, name='homework_assignment'),
    path('homework_submission/', views.student_homeworks, name='homework_submission'),
    path('view_submissions/', views.view_submissions, name='view_submissions'),
    path('view_absences/', views.parents_absences_view, name='view_absences'),
    path('view_children_grades/', views.get_grades_parents, name='view_children_grades'),
    path('view_student_grades', views.get_grades_student, name='view_student_grades'),
    path('student_calendar/', views.view_schedule_student,name='student_calendar'),
    path('parent_calendar/', views.view_schedule_parent,name='parent_calendar'),
    path('teacher_courses/', views.teacher_courses, name='teacher_courses'),
    path('courses/', views.view_courses, name='Courses'),
    path('my_student_courses/', views.student_courses, name='my_student_courses'),
    path('teacher_remarks/', views.teacher_remarks, name='teacher_remarks'),
    path('parent_remarks/', views.parent_remarks, name="parent_remarks")


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

