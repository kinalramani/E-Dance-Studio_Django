# courses/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from Instructor.models import Instructor


def validate_instructor(instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if not instructor.is_active or instructor.is_deleted or not instructor.is_verified:
        return None
    return instructor


@api_view(["POST"])
def create_course(request):
    data = request.data
    instructor_id = data.get("instructor")
    instructor = validate_instructor(instructor_id)
    if not instructor:
        return Response(
            {"message": "Invalid instructor"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CourseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_course(request):
    course_id = request.headers.get("Course-ID")
    if not course_id:
        return Response(
            {"message": "Course ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    course = get_object_or_404(Course, id=course_id)
    instructor = validate_instructor(course.instructor.id)
    if not instructor:
        return Response(
            {"message": "Invalid instructor"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(["PUT"])
def update_course(request):
    course_id = request.headers.get("Course-ID")
    if not course_id:
        return Response(
            {"message": "Course ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    course = get_object_or_404(Course, id=course_id)
    instructor = validate_instructor(course.instructor.id)
    if not instructor:
        return Response(
            {"message": "Invalid instructor"}, status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data
    if "instructor" in data:
        instructor_id = data["instructor"]
        instructor = validate_instructor(instructor_id)
        if not instructor:
            return Response(
                {"message": "Invalid instructor"}, status=status.HTTP_400_BAD_REQUEST
            )

    serializer = CourseSerializer(course, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_course(request):
    course_id = request.headers.get("Course-ID")
    if not course_id:
        return Response(
            {"message": "Course ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    course = get_object_or_404(Course, id=course_id)
    instructor = validate_instructor(course.instructor.id)
    if not instructor:
        return Response(
            {"message": "Invalid instructor"}, status=status.HTTP_400_BAD_REQUEST
        )

    if course.is_deleted:
        return Response(
            {"message": "Course already deleted"}, status=status.HTTP_400_BAD_REQUEST
        )

    course.is_deleted = True
    course.is_active = False
    course.save()
    return Response(
        {"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )
