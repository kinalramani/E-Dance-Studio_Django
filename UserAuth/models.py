from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u_name = models.CharField(max_length=150, unique=True)
    f_name = models.CharField(max_length=150)
    l_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    address = models.TextField()
    mob_no = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.f_name} {self.l_name}"


from django.utils import timezone


class Otp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=32, null=False)
    otp = models.CharField(max_length=6, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OTP for {self.otp}"
