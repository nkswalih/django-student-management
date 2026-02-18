from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student

@admin.register(Student)
class StudentAdmin(UserAdmin):
    """
    Admin interface for Student model
    """
    
    # Columns to display in the admin list
    list_display = [
        'email',
        'first_name',
        'last_name',
        'reg_number',
        'department',
        'course',
        'year_of_admission',
        'phone',
        'gender',
        'is_active',
        'date_joined'
    ]
    
    # Fields to search
    search_fields = ['email', 'first_name', 'last_name', 'reg_number', 'phone']
    
    # Sidebar filters
    list_filter = ['is_active', 'is_staff', 'gender', 'department', 'year_of_admission']
    
    # How to order results
    ordering = ['email']
    
    # Detailed view - organized in sections
    fieldsets = (
        ('Login Info', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'gender', 'profile_picture')
        }),
        ('Academic Info', {
            'fields': ('reg_number', 'department', 'course', 'year_of_admission')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # When adding a new student through admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'reg_number',
                'department',
                'course',
                'year_of_admission',
                'phone',
                'gender'
            )
        }),
    )