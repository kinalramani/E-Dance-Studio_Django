from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OurService
from .serializers import OurServiceSerializer

@api_view(['POST'])
def create_service(request):
    serializer = OurServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_services(request):
    services = OurService.objects.all()
    serializer = OurServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_service_by_id(request, pk):
    try:
        service = OurService.objects.get(pk=pk)
    except OurService.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OurServiceSerializer(service)
    return Response(serializer.data)

@api_view(['PUT'])
def update_service(request, pk):
    try:
        service = OurService.objects.get(pk=pk)
    except OurService.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OurServiceSerializer(service, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_service(request, pk):
    try:
        service = OurService.objects.get(pk=pk)
    except OurService.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    service.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
