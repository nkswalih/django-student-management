from django.contrib import admin
from .models import Course

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('course_id', 'course_name', 'department', 'price', 'created_at')
    search_fields = ('course_name', 'course_id')
    list_filter = ('department',)
    ordering = ('-created_at',)