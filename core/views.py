from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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
    else:
        return redirect('home')

    return render(request, template_name)