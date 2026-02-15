from django.shortcuts import redirect
from functools import wraps  # ✅ this is the fix

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)  # ✅ without this, pk never reaches the view
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.groups.filter(name=role).exists():
                return view_func(request, *args, **kwargs)

            if request.user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            elif request.user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')
            elif request.user.groups.filter(name='Principal').exists():
                return redirect('principal_dashboard')

            return redirect('login')

        return wrapper
    return decorator