from django.urls import path
from .views import (
    create_instructor,
    get_all_instructors,
    get_instructor,
    update_instructor,
    delete_instructor,
    generate_otp,
    verify_otp,
    login,
)

urlpatterns = [
    path("create/", create_instructor),
    path("instructors/", get_all_instructors),
    path("instructor/", get_instructor),
    path("instructor-update/", update_instructor),
    path("instructor-delete/", delete_instructor),
    path("generate-otp/", generate_otp),
    path("verify-otp/", verify_otp),
    path("login/", login),
]
