# instructors/serializers.py
from rest_framework import serializers
from .models import Instructor, Otp


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"
