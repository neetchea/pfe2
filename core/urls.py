from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import students_grades_view

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('grades/',views.students_grades_view, name='students_grades_view'),
    
]