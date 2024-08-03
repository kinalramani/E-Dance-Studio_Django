from django.db import models
import uuid
from Instructor.models import Instructor
from UserAuth.models import User
from Course.models import Course


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    final_fee = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.u_name} enrolled in {self.course.c_name}"
