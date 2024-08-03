from django.db import models
import uuid
from django.utils import timezone


class Instructor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    f_name = models.CharField(max_length=150)
    l_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    mob_no = models.CharField(max_length=15)
    bio = models.TextField()
    expertise = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.f_name} {self.l_name}"


class Otp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instructor = models.ForeignKey("Instructor", on_delete=models.CASCADE)
    email = models.EmailField(max_length=32, null=False)
    otp = models.CharField(max_length=6, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OTP for {self.email}"
