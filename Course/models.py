from django.db import models
import uuid
from Instructor.models import Instructor


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    c_name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    batch_time = models.CharField(max_length=255)
    time_duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.c_name
