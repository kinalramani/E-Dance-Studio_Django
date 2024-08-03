from django.db import models
import uuid
from Instructor.models import Instructor
from UserAuth.models import User
from Course.models import Course


# Create your models here.
class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"Feedback by {self.user.u_name} for {self.course.c_name}"
