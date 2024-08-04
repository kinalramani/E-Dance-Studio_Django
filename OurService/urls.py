# services/urls.py
from django.urls import path
from .views import (
    create_service,
    get_all_services,
    get_service,
    update_service,
    delete_service,
)

urlpatterns = [
    path("create/", create_service),
    path("services/", get_all_services),
    path("service/", get_service),
    path("update-service/", update_service),
    path("delete-service/", delete_service),
]
