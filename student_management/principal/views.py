from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from accounts.decorators import role_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Course
from .forms import CourseForm, UserEditForm


# Create your views here.
User = get_user_model()

@role_required('Principal')
def principal_dashboard(request):
    return render(request, 'principal/principal_dashboard.html')

@role_required('Principal')
def manage_course(request):
    courses = Course.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Course created succesfully")
            return redirect('manage_courses')
        else:
            messages.error(request, "please correct the errors below")
    else:
        form = CourseForm()

    context = {
        'form':form,
        'courses':courses
    }
    

    return render(request, 'principal/manage_courses.html', context)

@role_required('Principal')
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('manage_courses')

@role_required('Principal')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)

    context = {
        'form':form,
        'course':course
    }
   
    return render(request, 'principal/edit_course.html', context)

@role_required('Principal')
def view_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'principal/view_course.html', {
        'course': course
    })

@role_required('Principal')
def manage_user(request):
    students_group = Group.objects.get(name='Student')
    teachers_group = Group.objects.get(name='Teacher')

    students = User.objects.filter(groups=students_group)
    teachers = User.objects.filter(groups=teachers_group)

    context = {
        'students': students,
        'teachers': teachers,
    }

    return render(request, 'principal/manage_users.html', context)

@role_required('Principal')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'principal/edit_user.html', {
        'form': form,
        'user_obj': user
    })


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
