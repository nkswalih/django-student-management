from django import forms
from .models import Student

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
    # date_of_birth = forms.DateField(
    #     input_formats=['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y'],
    #     widget=forms.DateInput(attrs={'type': 'date'})
    #     )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'text',
            'class': 'flatpickr',
            'placeholder': 'Select your dob',
        })
    )

    class Meta:
        model = Student
        fields = [
            'profile_picture', 'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'gender',
            'reg_number', 'department', 'course', 'year_of_admission'
        ]
        
    gender = forms.ChoiceField(widget=forms.Select)
    department = forms.ChoiceField(widget=forms.Select)
    course = forms.ChoiceField(widget=forms.Select)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")