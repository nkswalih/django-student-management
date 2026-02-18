from principal.models import Enrollment

def pending_count(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Principal').exists():
        count = Enrollment.objects.filter(status='pending').count()
        return {'pending_count': count}
    return {'pending_count': 0}