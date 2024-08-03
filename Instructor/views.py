# instructors/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Instructor, Otp
from .serializers import InstructorSerializer
import bcrypt
import jwt
import datetime
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


def get_token_from_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except (IndexError, jwt.DecodeError):
        return None


@api_view(["POST"])
def create_instructor(request):
    data = request.data
    data["password"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    serializer = InstructorSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_instructors(request):
    instructors = Instructor.objects.all()
    serializer = InstructorSerializer(instructors, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_instructor(request):
    decoded_token = get_token_from_request(request)
    if not decoded_token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    instructor_id = decoded_token["user_id"]
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if not instructor.is_verified:
        return Response(
            {"message": "Instructor not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    serializer = InstructorSerializer(instructor)
    return Response(serializer.data)


@api_view(["PUT"])
def update_instructor(request):
    decoded_token = get_token_from_request(request)
    if not decoded_token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    instructor_id = decoded_token["user_id"]
    instructor = get_object_or_404(Instructor, id=instructor_id)

    # Check if the instructor is verified, not deleted, and active
    if not instructor.is_verified:
        return Response(
            {"message": "Instructor not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    if instructor.is_deleted:
        return Response(
            {"message": "Instructor is deleted"}, status=status.HTTP_403_FORBIDDEN
        )
    if not instructor.is_active:
        return Response(
            {"message": "Instructor is not active"}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data
    if "password" in data:
        data["password"] = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
    serializer = InstructorSerializer(instructor, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_instructor(request):
    decoded_token = get_token_from_request(request)
    if not decoded_token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    instructor_id = decoded_token["user_id"]
    instructor = get_object_or_404(Instructor, id=instructor_id)

    # Check if the instructor is already deleted
    if instructor.is_deleted and not instructor.is_active:
        return Response(
            {"message": "Instructor already deleted"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if the instructor is verified
    if not instructor.is_verified:
        return Response(
            {"message": "Instructor not verified"}, status=status.HTTP_403_FORBIDDEN
        )

    # Mark the instructor as deleted and inactive
    instructor.is_deleted = True
    instructor.is_active = False
    instructor.save()

    return Response(
        {"message": "Instructor deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["POST"])
def generate_otp(request):
    email = request.data.get("email")
    instructor = get_object_or_404(Instructor, email=email)
    otp = str(random.randint(100000, 999999))
    Otp.objects.create(instructor=instructor, email=email, otp=otp)

    # Send OTP email
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = email
    msg["Subject"] = "Your OTP Code"
    msg.attach(MIMEText(f"Your OTP code is {otp}", "plain"))
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
    server.quit()

    return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    otp_record = get_object_or_404(Otp, email=email, otp=otp)
    if otp_record:
        instructor = otp_record.instructor
        instructor.is_verified = True
        instructor.save()
        otp_record.delete()  # Delete the OTP record after successful verification
        return Response(
            {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
        )
    return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    u_name_or_email = request.data.get("u_name_or_email")
    password = request.data.get("password")
    try:
        instructor = Instructor.objects.get(email=u_name_or_email)
    except Instructor.DoesNotExist:
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    if instructor and bcrypt.checkpw(
        password.encode("utf-8"), instructor.password.encode("utf-8")
    ):
        if not instructor.is_verified:
            return Response(
                {"message": "Instructor not verified"}, status=status.HTTP_403_FORBIDDEN
            )
        payload = {
            "user_id": str(instructor.id),
            "u_name": instructor.email,  # Assuming email as the username
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return Response({"token": token}, status=status.HTTP_200_OK)
    return Response(
        {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
    )
