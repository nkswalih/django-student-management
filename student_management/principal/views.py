from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from accounts.decorators import role_required


# Create your views here.
@role_required('Principal')
def principal_dashboard(request):
    return render(request, 'principal/principal_dashboard.html')

@role_required('Principal')
def manage_course(request):
    return render(request, 'principal/manage_courses.html')


# def view_users(request):
#     return render(request, 'principal/my_courses.html')

@role_required('Principal')
def manage_user(request):
    return render(request, 'principal/manage_users.html')

@role_required('Principal')
def course_list(request):
    return render(request, 'principal/course_approvals.html')


# ---------Teacher---------
@role_required('Teacher')
def teacher_dashboard(request):
    return render(request, 'teacher/teacher_dashboard.html')

@role_required('Teacher')
def manage_notes(request):
    return render(request, 'teacher/manage_notes.html')

@role_required('Teacher')
def student_list(request):
    return render(request, 'teacher/student_list.html')

@role_required('Teacher')
def assign_homework(request):
    return render(request, 'teacher/assign_homework.html')

@role_required('Teacher')
def teacher_profile(request):
    return render(request, 'teacher/teacher_profile.html')

@role_required('Teacher')
def teacher_groups(request):
    return render(request, 'teacher/teacher_groups.html')
