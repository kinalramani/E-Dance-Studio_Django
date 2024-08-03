from django.urls import path
from .views import (
    create_enrollment,
    get_all_enrollments,
    get_enrollment_by_id,
    update_enrollment,
    delete_enrollment,
    
)

urlpatterns = [
    path('create-enrollments/',create_enrollment),
    path('enrollments/', get_all_enrollments),
    path('enrollments/<uuid:pk>/', get_enrollment_by_id),
    path('enrollments/<uuid:pk>/',update_enrollment),
    path('enrollments/<uuid:pk>/', delete_enrollment),
]