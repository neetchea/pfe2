
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import students_grades_view, parents_grades_view, assign_grades

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('grades/students/',views.students_grades_view, name='students_grades_view'),
    path('grades/parents/',views.parents_grades_view, name='parents_grades_view'),
    # Placeholder URLs
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('assign-grades/<int:classroom_id>/', views.assign_grades, name='assign-grades'),
]