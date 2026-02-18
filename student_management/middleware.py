from django.shortcuts import redirect

class RoleBasedRedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow admin always
        if request.path.startswith('/admin'):
            return self.get_response(request)

        if request.user.is_authenticated:

            # If user visits login page after login
            if request.path == '/accounts/login/':

                if request.user.groups.filter(name='Student').exists():
                    return redirect('student_dashboard')

                elif request.user.groups.filter(name='Teacher').exists():
                    return redirect('teacher_dashboard')

                elif request.user.groups.filter(name='Principal').exists():
                    return redirect('principal_dashboard')

        return self.get_response(request)
