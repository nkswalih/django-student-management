from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    """
    Custom User model for Students.
    Inherits from AbstractUser to handle authentication (username, password, first_name, last_name, email).
    """
    
    # -- Personal Details --
    profile_picture = models.ImageField(upload_to='students/profile_pics/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')

    # -- Academic Details --
    reg_number = models.CharField(max_length=20, unique=True, help_text="Unique Student Registration ID")
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_of_admission = models.PositiveIntegerField(default=2026)

    # Make username optional since we're using email for login
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    # Use email for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'reg_number']

    def save(self, *args, **kwargs):
        # Auto-generate username from email if not provided
        if not self.username:
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            
            # Handle duplicate usernames by appending a number
            while Student.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            self.username = username
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.reg_number})"