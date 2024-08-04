# feedback/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback
from .serializers import FeedbackSerializer
from Instructor.models import Instructor
from UserAuth.models import User
from Course.models import Course


def validate_foreign_keys(user_id, course_id, instructor_id):
    user = get_object_or_404(User, id=user_id)
    course = get_object_or_404(Course, id=course_id)
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return user, course, instructor


@api_view(["POST"])
def create_feedback(request):
    data = request.data
    user_id = data.get("user")
    course_id = data.get("course")
    instructor_id = data.get("instructor")
    user, course, instructor = validate_foreign_keys(user_id, course_id, instructor_id)

    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_feedbacks(request):
    feedbacks = Feedback.objects.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_feedback(request):
    feedback_id = request.headers.get("Feedback-ID")
    if not feedback_id:
        return Response(
            {"message": "Feedback ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    feedback = get_object_or_404(Feedback, id=feedback_id)
    serializer = FeedbackSerializer(feedback)
    return Response(serializer.data)


@api_view(["PUT"])
def update_feedback(request):
    feedback_id = request.headers.get("Feedback-ID")
    if not feedback_id:
        return Response(
            {"message": "Feedback ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    feedback = get_object_or_404(Feedback, id=feedback_id)
    data = request.data
    if "user" in data or "course" in data or "instructor" in data:
        user_id = data.get("user", feedback.user.id)
        course_id = data.get("course", feedback.course.id)
        instructor_id = data.get("instructor", feedback.instructor.id)
        validate_foreign_keys(user_id, course_id, instructor_id)

    serializer = FeedbackSerializer(feedback, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_feedback(request):
    feedback_id = request.headers.get("Feedback-ID")
    if not feedback_id:
        return Response(
            {"message": "Feedback ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return Response(
        {"message": "Feedback deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )
