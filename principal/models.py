from django.db import models
from accounts.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics'),
        ('MECH', 'Mechanical'),
        ('BBA', 'Business Administration'),
    ]

    course_id = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='principal/course_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_courses',
        limit_choices_to={'groups__name': 'Teacher'}
    )

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"


class Note(models.Model):
    """PDF notes uploaded by teacher for a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='notes/pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='uploaded_notes'
    )

    def __str__(self):
        return f"{self.title} - {self.course.course_name}"


class Enrollment(models.Model):
    """Tracks which student purchased which course."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.email} → {self.course.course_name} ({self.status})"
    
class Homework(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.course_name}"


class VoiceSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='voice_submissions')
    audio_file = models.FileField(upload_to='voice_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('homework', 'student')

    def __str__(self):
        return f"{self.student.email} - {self.homework.title}"