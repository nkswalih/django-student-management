from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from accounts.decorators import role_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count, Q, Prefetch, Sum, Case, When, IntegerField
from django.core.cache import cache
from .models import Course
from .forms import CourseForm, UserEditForm, EditUsersForm
from accounts.models import Student
from principal.models import Course, Note, Homework, VoiceSubmission, Enrollment

# Create your views here.
User = get_user_model()


@role_required("Principal")
def principal_dashboard(request):
    cache_key = "principal_dashboard_stats"
    cached_data = cache.get(cache_key)

    if cached_data:
        context = cached_data
    else:
        students_group = Group.objects.get(name="Student")
        teachers_group = Group.objects.get(name="Teacher")

        total_students = User.objects.filter(groups=students_group).count()
        total_teachers = User.objects.filter(groups=teachers_group).count()
        total_courses = Course.objects.count()
        active_courses = Course.objects.filter(is_active=True).count()

        dept_labels = ["CSE", "ECE", "MECH", "CIVIL", "BBA"]
        dept_counts = list(
            Student.objects.filter(department__in=dept_labels)
            .values("department")
            .annotate(count=Count("id"))
            .order_by("department")
            .values_list("count", flat=True)
        )

        while len(dept_counts) < len(dept_labels):
            dept_counts = list(dept_counts) + [0]

        recent_students = list(
            Student.objects.filter(groups=students_group)
            .only(
                "id",
                "first_name",
                "last_name",
                "email",
                "profile_picture",
                "reg_number",
                "date_joined",
            )
            .order_by("-date_joined")[:5]
        )

        context = {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_courses": total_courses,
            "active_courses": active_courses,
            "dept_labels": dept_labels,
            "dept_counts": dept_counts,
            "recent_students": recent_students,
        }
        cache.set(cache_key, context, 60)

    return render(request, "principal/principal_dashboard.html", context)


@role_required("Principal")
def manage_course(request):
    courses = list(
        Course.objects.all()
        .select_related("teacher")
        .only(
            "id",
            "course_id",
            "course_name",
            "price",
            "department",
            "is_active",
            "created_at",
            "teacher__first_name",
            "teacher__last_name",
        )
        .order_by("-created_at")
    )
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Course created succesfully")
            cache.delete("principal_dashboard_stats")
            return redirect("manage_courses")
        else:
            messages.error(request, "please correct the errors below")
    else:
        form = CourseForm()

    context = {"form": form, "courses": courses}

    return render(request, "principal/manage_courses.html", context)


@role_required("Principal")
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect("manage_courses")


@role_required("Principal")
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("manage_courses")
    else:
        form = CourseForm(instance=course)

    context = {"form": form, "course": course}

    return render(request, "principal/edit_course.html", context)


@role_required("Principal")
def view_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "principal/view_course.html", {"course": course})


@role_required("Principal")
def manage_user(request):
    cache_key = "user_groups_lookup"
    group_ids = cache.get(cache_key)

    if not group_ids:
        students_group = Group.objects.get(name="Student")
        teachers_group = Group.objects.get(name="Teacher")
        group_ids = {"students": students_group.id, "teachers": teachers_group.id}
        cache.set(cache_key, group_ids, 300)

    students = list(
        User.objects.filter(groups__id=group_ids["students"]).only(
            "id", "username", "first_name", "last_name", "email", "is_active"
        )
    )
    teachers = list(
        User.objects.filter(groups__id=group_ids["teachers"]).only(
            "id", "username", "first_name", "last_name", "email", "is_active"
        )
    )

    context = {
        "students": students,
        "teachers": teachers,
    }

    return render(request, "principal/manage_users.html", context)


@role_required("Principal")
def edit_user(request, pk):
    user_obj = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = EditUsersForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect("manage_users")
        else:
            messages.error(request, f"Please fix the errors: {form.errors}")
    else:
        form = EditUsersForm(instance=user_obj)

    return render(
        request, "principal/edit_user.html", {"form": form, "user_obj": user_obj}
    )


@role_required("Principal")
def course_approvals(request):

    pending = list(
        Enrollment.objects.filter(status="pending")
        .select_related("student", "course")
        .order_by("-enrolled_at")
    )

    status_counts = Enrollment.objects.filter(
        status__in=["approved", "rejected"]
    ).aggregate(
        approved_count=Count(Case(When(status="approved", then=1))),
        rejected_count=Count(Case(When(status="rejected", then=1))),
    )

    if request.method == "POST":
        enrollment_id = request.POST.get("enrollment_id")
        action = request.POST.get("action")
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)

        if action == "approve":
            enrollment.status = "approved"
            messages.success(
                request,
                f"Approved {enrollment.student.first_name}'s request for {enrollment.course.course_name}.",
            )
        elif action == "reject":
            enrollment.status = "rejected"
            messages.warning(
                request,
                f"Rejected {enrollment.student.first_name}'s request for {enrollment.course.course_name}.",
            )

        enrollment.save()
        cache.delete("principal_dashboard_stats")
        return redirect("course_approvals")

    context = {
        "pending": pending,
        "approved_count": status_counts["approved_count"],
        "rejected_count": status_counts["rejected_count"],
    }
    return render(request, "principal/course_approvals.html", context)


# ---------Teacher---------
@role_required("Teacher")
def teacher_dashboard(request):

    my_courses = list(
        Course.objects.filter(is_active=True).only(
            "id", "course_id", "course_name", "department", "price"
        )
    )
    course_ids = [c.id for c in my_courses]

    homeworks = list(
        Homework.objects.filter(teacher=request.user)
        .select_related("course")
        .order_by("-created_at")[:5]
    )

    pending_voices = list(
        VoiceSubmission.objects.filter(
            homework__teacher=request.user, is_reviewed=False
        ).select_related("student", "homework")[:5]
    )

    total_students = (
        Enrollment.objects.filter(course__in=course_ids, status="approved")
        .values("student")
        .distinct()
        .count()
    )

    voice_stats = VoiceSubmission.objects.filter(
        homework__teacher=request.user
    ).aggregate(
        total_voices=Count("id"),
        reviewed_voices=Count(Case(When(is_reviewed=True, then=1))),
    )

    context = {
        "my_courses": my_courses,
        "homeworks": homeworks,
        "pending_voices": pending_voices,
        "total_students": total_students,
        "total_courses": len(my_courses),
        "total_homeworks": Homework.objects.filter(teacher=request.user).count(),
        "pending_voice_count": VoiceSubmission.objects.filter(
            homework__teacher=request.user, is_reviewed=False
        ).count(),
        "reviewed_voices": voice_stats["reviewed_voices"],
        "total_voices": voice_stats["total_voices"],
    }
    return render(request, "teacher/teacher_dashboard.html", context)


def manage_notes(request):
    my_courses = Course.objects.filter(is_active=True)
    notes = (
        Note.objects.filter(uploaded_by=request.user)
        .select_related("course")
        .order_by("-uploaded_at")
    )

    if request.method == "POST":
        course_id = request.POST.get("course_id")
        title = request.POST.get("title")
        pdf_file = request.FILES.get("pdf_file")

        if not all([course_id, title, pdf_file]):
            messages.error(request, "All fields are required.")
            return redirect("manage_notes")

        course = get_object_or_404(Course, id=course_id)
        Note.objects.create(
            course=course, title=title, pdf_file=pdf_file, uploaded_by=request.user
        )
        messages.success(request, f"Note '{title}' uploaded successfully.")
        return redirect("manage_notes")

    return render(
        request,
        "teacher/manage_notes.html",
        {
            "my_courses": my_courses,
            "notes": notes,
        },
    )


@role_required("Teacher")
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, uploaded_by=request.user)
    note.pdf_file.delete()
    note.delete()
    messages.success(request, "Note deleted.")
    return redirect("manage_notes")


@role_required("Teacher")
def student_list(request):

    enrolled_students = (
        Enrollment.objects.filter(status="approved").values("student").distinct()
    )

    voice_submissions_prefetch = Prefetch(
        "voice_submissions",
        queryset=VoiceSubmission.objects.select_related(
            "homework", "homework__course"
        ).order_by("-submitted_at"),
    )

    students = (
        Student.objects.filter(id__in=enrolled_students)
        .prefetch_related(voice_submissions_prefetch)
        .only(
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "reg_number",
            "department",
        )
        .order_by("first_name")
    )

    student_data = []
    for student in students:
        voices = list(student.voice_submissions.all())
        student_data.append(
            {
                "student": student,
                "latest_voice": voices[0] if voices else None,
                "voice_count": len(voices),
                "unreviewed": sum(1 for v in voices if not v.is_reviewed),
            }
        )

    context = {
        "student_data": student_data,
    }
    return render(request, "teacher/student_list.html", context)


@role_required("Teacher")
def student_detail(request, pk):

    student = get_object_or_404(Student, pk=pk)

    submissions = list(
        VoiceSubmission.objects.filter(student=student)
        .select_related("homework", "homework__course")
        .order_by("-submitted_at")
    )

    if request.method == "POST":
        submission_id = request.POST.get("submission_id")
        if submission_id:
            sub = get_object_or_404(VoiceSubmission, pk=submission_id, student=student)
            sub.is_reviewed = True
            sub.save()
            messages.success(request, "Marked as reviewed.")
            return redirect("student_detail", pk=pk)

    enrollments = list(
        Enrollment.objects.filter(student=student, status="approved").select_related(
            "course"
        )
    )

    submission_counts = VoiceSubmission.objects.filter(student=student).aggregate(
        total=Count("id"),
        reviewed=Count(Case(When(is_reviewed=True, then=1))),
        pending=Count(Case(When(is_reviewed=False, then=1))),
    )

    context = {
        "student": student,
        "submissions": submissions,
        "enrollments": enrollments,
        "total_submissions": submission_counts["total"],
        "reviewed_count": submission_counts["reviewed"],
        "pending_count": submission_counts["pending"],
    }
    return render(request, "teacher/student_detail.html", context)


@role_required("Teacher")
def assign_homework(request):

    my_courses = Course.objects.filter(is_active=True)
    homeworks = (
        Homework.objects.filter(teacher=request.user)
        .select_related("course")
        .order_by("-created_at")
    )

    if request.method == "POST":
        course_id = request.POST.get("course_id")
        title = request.POST.get("title")
        instructions = request.POST.get("instructions")
        due_date = request.POST.get("due_date")

        if not all([course_id, title, instructions, due_date]):
            messages.error(request, "All fields are required.")
            return redirect("assign_homework")

        course = get_object_or_404(Course, id=course_id)
        Homework.objects.create(
            course=course,
            teacher=request.user,
            title=title,
            instructions=instructions,
            due_date=due_date,
        )
        messages.success(request, f"Homework '{title}' assigned.")
        return redirect("assign_homework")

    return render(
        request,
        "teacher/assign_homework.html",
        {
            "my_courses": my_courses,
            "homeworks": homeworks,
        },
    )


@role_required("Teacher")
def delete_homework(request, pk):
    hw = get_object_or_404(Homework, pk=pk, teacher=request.user)
    hw.delete()
    messages.success(request, "Homework deleted.")
    return redirect("assign_homework")


@role_required("Teacher")
def teacher_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)

        new_email = request.POST.get("email", "").strip()
        if new_email and new_email != user.email:
            from accounts.models import Student

            if Student.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, "Email already in use.")
                return redirect("teacher_profile")
            user.email = new_email
            user.username = new_email.split("@")[0]

        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]

        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        if new_password:
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("teacher_profile")
            user.set_password(new_password)
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("teacher_profile")

    return render(request, "teacher/teacher_profile.html")


@role_required("Teacher")
def teacher_groups(request):
    return render(request, "teacher/teacher_groups.html")


@role_required("Teacher")
def review_voices(request):

    submissions = (
        VoiceSubmission.objects.filter(homework__teacher=request.user)
        .select_related("student", "homework")
        .order_by("-submitted_at")
    )

    if request.method == "POST":
        submission_id = request.POST.get("submission_id")
        submission = get_object_or_404(VoiceSubmission, pk=submission_id)
        submission.is_reviewed = True
        submission.save()
        messages.success(request, "Marked as reviewed.")
        return redirect("review_voices")

    context = {"submissions": submissions}
    return render(request, "teacher/review_voices.html", context)
