from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class StudentManager(BaseUserManager):
    """Custom manager — fixes createsuperuser crash."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class Student(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    
    DEPT_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics & Comm'),
        ('MECH', 'Mechanical Eng'),
        ('CIVIL', 'Civil Engineering'),
        ('BBA', 'Business Admin'),
    ]

    COURSE_CHOICES = [
        ('BTECH', 'B.Tech'),
        ('MTECH', 'M.Tech'),
        ('BCA', 'BCA'),
        ('MCA', 'MCA'),
        ('MBA', 'MBA'),
    ]
    # -- Personal Details --
    # profile_picture = models.ImageField(upload_to='students/profile_pics/', blank=True, null=True)
    profile_picture = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')

    # -- Academic Details --
    reg_number = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Unique Student Registration ID")
    department = models.CharField(max_length=100, choices=DEPT_CHOICES, blank=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, blank=True)
    year_of_admission = models.PositiveIntegerField(default=2026)

    # Username is auto-generated
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Attached a custom manager
    objects = StudentManager()

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            while Student.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.reg_number})"