from django import forms
from .models import Course
from django.contrib.auth import get_user_model
from accounts.models import Student

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

class EditUsersForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'phone',
            'gender',
            'reg_number',
            'year_of_admission',
            'department',
            'course',
            'is_active',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'reg_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'year_of_admission': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-brand text-sm text-slate-800 font-medium'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'peer h-5 w-5 cursor-pointer appearance-none rounded-md border border-slate-300 transition-all checked:border-brand checked:bg-brand'
            }),
        }