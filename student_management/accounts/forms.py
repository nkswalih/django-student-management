from django import forms
from .models import Student

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = [
            'profile_picture', 'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'gender',
            'reg_number', 'department', 'course', 'year_of_admission'
        ]

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
        
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select)
    department = forms.ChoiceField(choices=DEPT_CHOICES, widget=forms.Select)
    course = forms.ChoiceField(choices=COURSE_CHOICES, widget=forms.Select)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")