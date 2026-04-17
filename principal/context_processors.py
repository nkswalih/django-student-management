from principal.models import Enrollment
from django.core.cache import cache


def pending_count(request):
    if not request.user.is_authenticated:
        return {"pending_count": 0}

    if not request.user.groups.filter(name="Principal").exists():
        return {"pending_count": 0}

    cache_key = "pending_enrollment_count"
    count = cache.get(cache_key)

    if count is None:
        count = Enrollment.objects.filter(status="pending").count()
        cache.set(cache_key, count, 60)

    return {"pending_count": count}
