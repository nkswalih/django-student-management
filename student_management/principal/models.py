from django.db import models

# Create your models here.
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

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"