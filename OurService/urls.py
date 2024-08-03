from django.urls import path
from .views import (
    create_service,
    get_all_services,
    get_service_by_id,
    update_service,
    delete_service,
    
)



urlpatterns = [
    path('services/',create_service),
    path('services/',get_all_services),
    path('services/<uuid:pk>/',get_service_by_id),
    path('services/<uuid:pk>/',update_service),
    path('services/<uuid:pk>/',delete_service),
]