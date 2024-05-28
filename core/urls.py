
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
    # path('grades/parents/',views.parents_grades_view, name='parents_grades_view'),
    # Placeholder URLs
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.announcements, name='events'),
    path('calendars/', views.my_calendars, name='my_calendars'),
    path('courses/', views.courses, name='courses'),
    path('grades/', views.my_grades, name='grades'),
   
    path('assign-grades/<int:classroom_id>/change/', views.assign_grades, name='assign-grades'),
    path('homework_assignment/', views.homework_assignment, name='homework_assignment'),
    path('homework_submission/', views.student_homeworks, name='homework_submission'),
    path('view_submissions/', views.view_submissions, name='view_submissions'),
    path('view_absences/', views.parents_absences_view, name='view_absences'),
    path('view_children_grades/', views.get_grades_parents, name='view_children_grades'),
    path('view_student_grades', views.get_grades_student, name='view_student_grades'),
    path('calendar/<int:cal_id>/', views.display_calendar, name='display_calendar'),
    path('student_calendar/', views.view_schedule_student,name='student_calendar'),
    path('parent_calendar/', views.view_schedule_parent,name='parent_calendar'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

