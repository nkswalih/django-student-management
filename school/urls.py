from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('dashboard/my-courses/', views.my_courses, name='my_courses'),
    path('dashboard/my-courses/<int:pk>/', views.view_course, name='student_view_course'),
    path('dashboard/purchase/', views.purchase_course, name='purchase_course'),
    path('dashboard/class-group/', views.class_group, name='class_group'),
    path('dashboard/profile/', views.student_profile, name='student_profile'),
    path('dashboard/submit-voice/', views.submit_voice, name='submit_voice'),
    path('search/', views.search, name='student_search'),
    path('old/', views.old, name='student_old'),
]