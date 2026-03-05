import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superuser {email} created.")
else:
    print(f"Superuser {email} already exists.")