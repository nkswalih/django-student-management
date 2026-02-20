import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management.settings")

# Run migrations on startup
import django
django.setup()

from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb')
except Exception as e:
    print(f"Migration error: {e}")

from student_management.wsgi import application
app = application