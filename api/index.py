import os
import sys

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management.settings")

from student_management.wsgi import application

app = application