from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('dashboard/my-courses/', views.my_courses, name='my_courses'),
    path('dashboard/purchase/', views.purchase_course, name='purchase_course'),
    path('dashboard/class-group/', views.class_group, name='class_group'),
    path('dashboard/profile/', views.student_profile, name='student_profile'),
    path('old/', views.old, name='student_old'),
]