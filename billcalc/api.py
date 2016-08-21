from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .models import *
from .serializers import *


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ClientView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        client = Client.objects.get(user=request.user)
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)


class ProjectList(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        client = Client.objects.get(user=request.user)
        projects = Project.objects.filter(client=client)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy()
        data['client'] = Client.objects.get(user=request.user).id
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, client):
        try:
            return Project.objects.get(id=pk, client=client)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = Client.objects.get(user=request.user)
        project = self.get_object(pk, client)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class TimeSheetDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, project_ids):
        try:
            return TimeSheet.objects.get(id=pk, project_id__in=project_ids)
        except TimeSheet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = Client.objects.get(user=request.user)
        project_ids = list(
            map(lambda x: x['id'], Project.objects.filter(client=client).values('id')))
        timesheet = self.get_object(pk, project_ids)
        serializer = TimeSheetSerializer(timesheet)
        return Response(serializer.data)


class TimeSheetList(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        client = Client.objects.get(user=request.user)
        projects = Project.objects.filter(client=client)
        timesheets = []
        for project in projects:
            entries = TimeSheet.objects.filter(project=project)
            for entry in entries:
                timesheets.append(entry)
        serializer = TimeSheetSerializer(timesheets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TimeSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Report(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        client = Client.objects.get(user=request.user)
        projects = Project.objects.filter(client=client)
        res = []
        project_id = request.query_params.get('project', None)
        period = request.query_params.get('period', None)

        if period == "weekly":
            if project_id:
                project = projects.get(id=project_id)
                res = project.weekly_report()
            else:
                res = client.weekly_report()
            return Response(res)

        if period == "monthly":
            if project_id:
                project = projects.get(id=project_id)
                res = project.monthly_report()
            else:
                res = client.monthly_report()
            return Response(res)

        if period == "yearly":
            if project_id:
                project = projects.get(id=project_id)
                res = project.yearly_report()
            else:
                res = client.yearly_report()
            return Response(res)

        for project in projects:
            cost_per_hour = project.cost_per_hour
            total_time_spent = TimeSheet.objects.filter(project=project).aggregate(
                total_time_spent=Sum('time_spent'))['total_time_spent']
            total_cost = total_time_spent * cost_per_hour
            res.append({'name': project.id, 'total_cost': total_cost,
                        'total_time_spent': total_time_spent, 'cost_per_hour': project.cost_per_hour})
        return Response(res)
