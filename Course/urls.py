# courses/urls.py
from django.urls import path
from .views import (
    create_course,
    get_all_courses,
    get_course,
    update_course,
    delete_course,
)

urlpatterns = [
    path("create_course/", create_course),
    path("get_all_courses/", get_all_courses),
    path("get_course_by_id/", get_course),
    path("course-update/", update_course),
    path("course-delete/", delete_course),
]
