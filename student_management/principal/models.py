from django.db import models
from accounts.models import Student

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

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"


class Note(models.Model):
    """PDF notes uploaded by teacher for a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='notes/pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

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
    progress = models.PositiveIntegerField(default=0)  # 0-100%

    class Meta:
        unique_together = ('student', 'course')  # prevent duplicate purchases

    def __str__(self):
        return f"{self.student.email} → {self.course.course_name} ({self.status})"