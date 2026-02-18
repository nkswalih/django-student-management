from django.urls import path
from . import views

urlpatterns = [
    path('principal-dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('manage-courses/', views.manage_course, name='manage_courses'),
    path('manage-users/', views.manage_user, name='manage_users'),
    path('course-approvals/', views.course_approvals, name='course_approvals'),
    path('delete-course/<int:pk>/', views.delete_course, name='delete_course'),
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('view-course/<int:pk>/', views.view_course, name='view_course'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),

    # Teacher
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('manage-notes/', views.manage_notes, name='manage_notes'),
    path('teacher/delete-note/<int:pk>/', views.delete_note, name='delete_note'),
    path('student-list/', views.student_list, name='student_list'),
    path('student-list/<int:pk>/', views.student_detail, name='student_detail'),
    path('assign-homework/', views.assign_homework, name='assign_homework'),
    path('assign-homework/delete/<int:pk>/', views.delete_homework, name='delete_homework'),
    path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher-groups/', views.teacher_groups, name='teacher_groups'),
    path('teacher/review-voices/', views.review_voices, name='review_voices'),

]