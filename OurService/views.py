# services/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OurService
from .serializers import OurServiceSerializer


@api_view(["POST"])
def create_service(request):
    data = request.data
    serializer = OurServiceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_services(request):
    services = OurService.objects.all()
    serializer = OurServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_service(request):
    service_id = request.headers.get("Service-ID")
    if not service_id:
        return Response(
            {"message": "Service ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    service = get_object_or_404(OurService, id=service_id)
    serializer = OurServiceSerializer(service)
    return Response(serializer.data)


@api_view(["PUT"])
def update_service(request):
    service_id = request.headers.get("Service-ID")
    if not service_id:
        return Response(
            {"message": "Service ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    service = get_object_or_404(OurService, id=service_id)
    data = request.data
    serializer = OurServiceSerializer(service, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_service(request):
    service_id = request.headers.get("Service-ID")
    if not service_id:
        return Response(
            {"message": "Service ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    service = get_object_or_404(OurService, id=service_id)

    if service.is_deleted:
        return Response(
            {"message": "Service already deleted"}, status=status.HTTP_400_BAD_REQUEST
        )

    service.is_deleted = True
    service.is_active = False
    service.save()
    return Response(
        {"message": "Service deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )
