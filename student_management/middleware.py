from django.shortcuts import redirect
from django.urls import resolve
from django.http import Http404

class RoleBasedRedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            resolve(request.path)
        except Http404:

            if request.user.is_authenticated:

                if request.user.groups.filter(name='Student').exists():
                    return redirect('student_dashboard')

                elif request.user.groups.filter(name='Teacher').exists():
                    return redirect('teacher_dashboard')

                elif request.user.groups.filter(name='Principal').exists():
                    return redirect('principal_dashboard')

            return redirect('login')

        return self.get_response(request)
