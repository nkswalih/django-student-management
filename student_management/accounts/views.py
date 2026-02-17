from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import Student

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Smtp Welcome Email
            try:
                send_mail(
                    subject='Welcome to Student Management System 🎓',
                    message=f'Hi {user.first_name},\n\nYour account has been successfully created.\n\nLogin and start learning!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed: {e}")

            group, _ = Group.objects.get_or_create(name='Student')
            user.groups.add(group)
            messages.success(request, "Registration successful! You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                
                # Handle "Remember Me" checkbox
                remember_me = request.POST.get('remember_me')
                if not remember_me:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                else:
                    # Session lasts for 2 weeks (1209600 seconds)
                    request.session.set_expiry(1209600)

                messages.success(request, f"Welcome back, {user.first_name}!")
                
                if user.groups.filter(name='Principal').exists():
                    return redirect('principal_dashboard')

                elif user.groups.filter(name='Teacher').exists():
                    return redirect('teacher_dashboard')

                elif user.groups.filter(name='Student').exists():
                    return redirect('student_dashboard')

                else:
                    return redirect('login')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect("login")

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Student.objects.get(email=email)
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset URL
            current_site = get_current_site(request)
            reset_url = f"http://{current_site.domain}/accounts/reset/{uid}/{token}/"
            
            # Send email
            try:
                send_mail(
                    subject='Password Reset Request',
                    message=f'Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, "Password reset link has been sent to your email.")
            except Exception as e:
                messages.error(request, "Failed to send email. Please try again later.")
                print(f"Email failed: {e}")
                
        except Student.DoesNotExist:
            # Don't reveal if email exists or not (security)
            messages.success(request, "If that email exists, a password reset link has been sent.")
        
        return redirect('login')
    
    return render(request, 'accounts/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully. You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        
        return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('password_reset')