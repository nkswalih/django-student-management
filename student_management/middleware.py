from django.shortcuts import redirect
from django.core.cache import cache

class RoleBasedRedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow admin always
        if request.path.startswith('/admin'):
            return self.get_response(request)

        # Only check on login page (no need to run on every page!)
        if request.user.is_authenticated and request.path == '/accounts/login/':
            
            # Cache the user role
            cache_key = f'user_role_{request.user.id}'
            role = cache.get(cache_key)
            
            if role is None:
                # Single query to get all groups at once
                groups = list(request.user.groups.values_list('name', flat=True))
                if 'Student' in groups:
                    role = 'Student'
                elif 'Teacher' in groups:
                    role = 'Teacher'
                elif 'Principal' in groups:
                    role = 'Principal'
                else:
                    role = 'none'
                cache.set(cache_key, role, 300)  # cache 5 minutes
            
            if role == 'Student':
                return redirect('student_dashboard')
            elif role == 'Teacher':
                return redirect('teacher_dashboard')
            elif role == 'Principal':
                return redirect('principal_dashboard')

        return self.get_response(request)