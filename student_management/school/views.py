from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from accounts.decorators import role_required

# Create your views here.
def home(request):
    return render(request, 'school/home.html')

@login_required
@role_required('Student')
def dashboard(request):
    return render(request, 'school/dashboard.html')

@login_required
@role_required('Student')
def my_courses(request):
    return render(request, 'school/my_courses.html')

@login_required
@role_required('Student')
def purchase_course(request):
    return render(request, 'school/purchase.html')

@login_required
@role_required('Student')
def class_group(request):
    return render(request, 'school/class_group.html')

@login_required
@role_required('Student')
def student_profile(request):
    if request.method == 'POST':
        user = request.user

        # Update profile picture
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        # Update email
        new_email = request.POST.get('email')
        if new_email and new_email != user.email:
            from accounts.models import Student
            if Student.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, "This email is already in use.")
                return redirect('student_profile')
            user.email = new_email
            user.username = new_email.split('@')[0]

        # Update password
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password:
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('student_profile')
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keep user logged in

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('student_profile')

    return render(request, 'school/profile.html')

def old(request):
    return render(request, 'school/old.html')