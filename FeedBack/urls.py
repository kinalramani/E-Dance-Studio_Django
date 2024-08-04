# feedback/urls.py
from django.urls import path
from .views import (
    create_feedback,
    get_all_feedbacks,
    get_feedback,
    update_feedback,
    delete_feedback,
)

urlpatterns = [
    path("create/", create_feedback),
    path("feedbacks/", get_all_feedbacks),
    path("feedback/", get_feedback),
    path("feedback/update/", update_feedback),
    path("feedback/delete/", delete_feedback),
]
