from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(role):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):

            if request.user.groups.filter(name=role).exists():
                return view_func(request, *args, **kwargs)

            # 🔁 Redirect based on actual role
            if request.user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')

            elif request.user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')

            elif request.user.groups.filter(name='Principal').exists():
                return redirect('principal_dashboard')

            # fallback
            return redirect('login')

        return wrapper
    return decorator
