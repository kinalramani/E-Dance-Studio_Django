# enrollment/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment
from .serializers import EnrollmentSerializer
from Instructor.models import Instructor
from UserAuth.models import User
from Course.models import Course


def validate_foreign_keys(user_id, course_id, instructor_id):
    user = get_object_or_404(User, id=user_id)
    course = get_object_or_404(Course, id=course_id)
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return user, course, instructor


@api_view(["POST"])
def create_enrollment(request):
    data = request.data
    user_id = data.get("user")
    course_id = data.get("course")
    instructor_id = data.get("instructor")
    user, course, instructor = validate_foreign_keys(user_id, course_id, instructor_id)

    serializer = EnrollmentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_enrollments(request):
    enrollments = Enrollment.objects.all()
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_enrollment(request):
    enrollment_id = request.headers.get("Enrollment-ID")
    if not enrollment_id:
        return Response(
            {"message": "Enrollment ID not provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    serializer = EnrollmentSerializer(enrollment)
    return Response(serializer.data)


@api_view(["PUT"])
def update_enrollment(request):
    enrollment_id = request.headers.get("Enrollment-ID")
    if not enrollment_id:
        return Response(
            {"message": "Enrollment ID not provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    data = request.data
    if "user" in data or "course" in data or "instructor" in data:
        user_id = data.get("user", enrollment.user.id)
        course_id = data.get("course", enrollment.course.id)
        instructor_id = data.get("instructor", enrollment.instructor.id)
        validate_foreign_keys(user_id, course_id, instructor_id)

    serializer = EnrollmentSerializer(enrollment, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_enrollment(request):
    enrollment_id = request.headers.get("Enrollment-ID")
    if not enrollment_id:
        return Response(
            {"message": "Enrollment ID not provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if enrollment.is_deleted:
        return Response(
            {"message": "Enrollment already deleted"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    enrollment.is_deleted = True
    enrollment.is_active = False
    enrollment.save()
    return Response(
        {"message": "Enrollment deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )
