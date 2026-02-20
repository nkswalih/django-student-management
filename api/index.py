import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management.settings")

import django
django.setup()

from django.core.management import call_command
call_command('collectstatic', '--noinput', verbosity=0)

from student_management.wsgi import application
app = application