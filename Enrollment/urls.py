# enrollment/urls.py
from django.urls import path
from .views import (
    create_enrollment,
    get_all_enrollments,
    get_enrollment,
    update_enrollment,
    delete_enrollment,
)

urlpatterns = [
    path("create/", create_enrollment),
    path("enrollments/", get_all_enrollments),
    path("enrollment/", get_enrollment),
    path("enrollment/update/", update_enrollment),
    path("enrollment/delete/", delete_enrollment),
]
