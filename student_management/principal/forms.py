from django import forms
from .models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'price', 'department', 'description', 'image']
        widgets = {
            'course_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl bg-slate-50 border-none focus:ring-brand text-sm',
                'placeholder': 'e.g. CS101'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl bg-slate-50 border-none focus:ring-brand text-sm',
                'placeholder': 'Intro to Python'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-xl bg-slate-50 border-none focus:ring-brand text-sm',
                'placeholder': '49.99'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-xl bg-slate-50 border-none focus:ring-brand text-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-xl bg-slate-50 border-none focus:ring-brand text-sm',
                'rows': 3,
                'placeholder': 'Brief details...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brandLight file:text-brand hover:file:bg-indigo-100'
            })
        }

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['password', 'email', 'groups', 'user_permissions']