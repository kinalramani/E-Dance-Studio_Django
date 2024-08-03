from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment, User, Course
from .serializers import EnrollmentSerializer

@api_view(['POST'])
def create_enrollment(request):
    serializer = EnrollmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_enrollments(request):
    enrollments = Enrollment.objects.all()
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_enrollment_by_id(request, pk):
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EnrollmentSerializer(enrollment)
    return Response(serializer.data)

@api_view(['PUT'])
def update_enrollment(request, pk):
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Verify user and course
    user_verified = request.data.get('user_verified', False)
    course_verified = request.data.get('course_verified', False)
    if user_verified and course_verified:
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'User and course must be verified'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_enrollment(request, pk):
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Verify user and course
    user_verified = request.data.get('user_verified', False)
    course_verified = request.data.get('course_verified', False)
    if user_verified and course_verified:
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'User and course must be verified'}, status=status.HTTP_400_BAD_REQUEST)
