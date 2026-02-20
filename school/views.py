from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from principal.models import Course, Enrollment, Note, Homework, VoiceSubmission
from datetime import date
from django.db import models

# Create your views here.
def home(request):
    return render(request, 'school/home.html')


@role_required('Student')
def dashboard(request):

    # Enrollment stats
    enrollments = Enrollment.objects.filter(student=request.user)
    approved = enrollments.filter(status='approved').count()
    pending = enrollments.filter(status='pending').count()
    rejected = enrollments.filter(status='rejected').count()

    # Total spend
    total_spend = sum(
        e.course.price for e in enrollments.filter(status='approved')
    )

    # Homework from approved courses
    approved_course_ids = enrollments.filter(
        status='approved'
    ).values_list('course_id', flat=True)

    homeworks = Homework.objects.filter(
        course__id__in=approved_course_ids
    ).select_related('course').order_by('due_date')[:5]

    context = {
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'total_spend': total_spend,
        'homeworks': homeworks,
        'today': date.today(),
    }
    return render(request, 'school/dashboard.html', context)


@role_required('Student')
def my_courses(request):
    
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-enrolled_at')

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'school/my_courses.html', context)


@role_required('Student')
def purchase_course(request):

    all_courses = Course.objects.filter(is_active=True)

    # Get all course IDs where the currently logged-in user is enrolled.
    enrolled_course_ids = Enrollment.objects.filter(
        student=request.user
    ).values_list('course_id', flat=True)

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Check if already enrolled
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, "You already purchased this course.")
        else:
            Enrollment.objects.create(
                student=request.user,
                course=course,
                status='pending'
            )
            messages.success(request, f"Purchase request for '{course.course_name}' sent! Awaiting approval.")

        return redirect('purchase_course')

    context = {
        'courses': all_courses,
        'enrolled_ids': list(enrolled_course_ids),
    }
    return render(request, 'school/purchase.html', context)


@role_required('Student')
def view_course(request, pk):
    enrollment = get_object_or_404(
        Enrollment,
        course__id=pk,
        student=request.user,
        # status='approved'
    )

    if enrollment.status == 'pending':
        messages.warning(request, "This course is still awaiting approval.")
        return redirect('my_courses')

    if enrollment.status == 'rejected':
        messages.error(request, "Your enrollment was rejected.")
        return redirect('my_courses')

    course = enrollment.course
    notes = course.notes.all().order_by('-uploaded_at')

    context = {
        'course': course,
        'enrollment': enrollment,
        'notes': notes,
    }
    return render(request, 'school/view_course.html', context)


@role_required('Student')
def submit_voice(request):
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        audio_file = request.FILES.get('audio_file')

        if not homework_id or not audio_file:
            messages.error(request, "Missing homework or audio file.")
            return redirect('student_dashboard')

        homework = get_object_or_404(Homework, id=homework_id)

        # Check if already submitted
        existing = VoiceSubmission.objects.filter(
            homework=homework,
            student=request.user
        ).first()

        if existing:
            # Update existing submission
            existing.audio_file.delete()
            existing.audio_file = audio_file
            existing.is_reviewed = False
            existing.save()
            messages.success(request, "Voice submission updated.")
        else:
            VoiceSubmission.objects.create(
                homework=homework,
                student=request.user,
                audio_file=audio_file
            )
            messages.success(request, "Voice submitted to teacher.")

        return redirect('student_dashboard')

    return redirect('student_dashboard')

@role_required('Student')
def class_group(request):
    return render(request, 'school/class_group.html')


@role_required('Student')
def student_profile(request):
    if request.method == 'POST':
        user = request.user

        # Update profile picture - upload directly to Cloudinary
        if 'profile_picture' in request.FILES:
            import cloudinary.uploader
            file = request.FILES['profile_picture']
            result = cloudinary.uploader.upload(
                file,
                folder='students/profile_pics/',
                public_id=f'student_{user.pk}',
                overwrite=True,
                resource_type='image'
            )
            # Save the Cloudinary URL directly to the field
            user.profile_picture = result['secure_url']

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
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('student_profile')

    return render(request, 'school/profile.html')

@role_required('Student')
def search(request):

    query = request.GET.get('q', '').strip()
    results = {
        'courses': [],
        'homeworks': [],
        'query': query,
    }

    if query:
        # Search courses student is enrolled in
        enrolled_course_ids = Enrollment.objects.filter(
            student=request.user
        ).values_list('course_id', flat=True)

        results['courses'] = Course.objects.filter(
            id__in=enrolled_course_ids
        ).filter(
            models.Q(course_name__icontains=query) |
            models.Q(course_id__icontains=query) |
            models.Q(department__icontains=query) |
            models.Q(description__icontains=query)
        )

        # Search homework
        results['homeworks'] = Homework.objects.filter(
            course__id__in=enrolled_course_ids
        ).filter(
            models.Q(title__icontains=query) |
            models.Q(instructions__icontains=query)
        )

        # All available courses (shop)
        results['available_courses'] = Course.objects.filter(
            is_active=True
        ).filter(
            models.Q(course_name__icontains=query) |
            models.Q(course_id__icontains=query) |
            models.Q(department__icontains=query)
        ).exclude(id__in=enrolled_course_ids)

    return render(request, 'school/student_search.html', results)

def old(request):
    return render(request, 'school/old.html')

from django.http import JsonResponse
import os

def debug_env(request):
    return JsonResponse({
        'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET'),
        'api_key': os.environ.get('CLOUDINARY_API_KEY', 'NOT SET'),
        'secret': 'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET',
        'storage': 'MediaCloudinaryStorage' if 'cloudinary' in __import__('django.conf', fromlist=['settings']).settings.DEFAULT_FILE_STORAGE else 'FILESYSTEM',
    })