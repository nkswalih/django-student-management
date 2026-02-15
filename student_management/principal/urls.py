from django.urls import path
from . import views

urlpatterns = [
    path('principal-dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('manage-courses/', views.manage_course, name='manage_courses'),
    # path('user/<int:student_id>/', views.view_users, name='view_users'),
    path('manage-users/', views.manage_user, name='manage_users'),
    path('course-approvals/', views.course_approvals, name='course_approvals'),
    path('delete-course/<int:pk>/', views.delete_course, name='delete_course'),
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('view-course/<int:pk>/', views.view_course, name='view_course'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    # Teacher
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('manage-notes/', views.manage_notes, name='manage_notes'),
    # path('user/<int:student_id>/', views.view_users, name='view_users'),
    path('student-list/', views.student_list, name='student_list'),
    path('assign-homework/', views.assign_homework, name='assign_homework'),
    path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher-groups/', views.teacher_groups, name='teacher_groups'),

]