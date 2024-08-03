from django.contrib import admin
from django.urls import path
from .views import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    generate_otp,
    verify_otp,
    login,
)

urlpatterns = [
    path("create_user/", create_user),
    path("get_all_users/", get_all_users),
    path("get_user_by_id/", get_user_by_id),
    path("update_user/", update_user),
    path("delete_user/", delete_user),
    path("generate_otp/", generate_otp),
    path("verify_otp/", verify_otp),
    path("login/", login),
]
