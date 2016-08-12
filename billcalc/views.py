from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from .models import *
from .serializers import *

class ClientList(APIView):

    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

class ProjectList(APIView):

    def get(self, request, format=None):
        clients = Project.objects.all()
        serializer = ProjectSerializer(clients, many=True)
        return Response(serializer.data)

class TimeSheetList(APIView):

    def get(self, request, format=None):
        clients = TimeSheet.objects.all()
        serializer = TimeSheetSerializer(clients, many=True)
        return Response(serializer.data)
