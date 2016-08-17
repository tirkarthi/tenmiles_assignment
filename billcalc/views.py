from django.shortcuts import render_to_response, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Sum
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import json
from .models import *
from .serializers import *


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        company_info = request.POST.get("company_info", "")

        user = User.objects.filter(email=email)

        status = {}

        if user:
            status = json.dumps({'signin_error': 'Email already exists'})
        else:
            status = json.dumps({'success': 'account successfully created'})
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            Client.objects.create(
                user=user, name=name, email=email, company_info=company_info)
        return redirect(reverse("signin"))

    return render_to_response('signup.html', RequestContext(request))


@login_required
def dashboard(request):
    user = request.user
    client = Client.objects.get(user=user)
    name = client.name
    company_info = client.company_info
    monthly_report = client.monthly_report()
    weekly_report = client.weekly_report()
    yearly_report = client.yearly_report()
    return render_to_response('dashboard.html', {"weekly": weekly_report, "monthly": monthly_report, "yearly": yearly_report, "name": name, "company_info": company_info}, RequestContext(request))


def signin(request):
    if request.method == "POST":
        password = request.POST.get("password", "")
        email_id = request.POST.get("email", "")
        user = authenticate(username=email_id, password=password)
        if user:
            login(request, user)
            return redirect(reverse("dashboard"))

    return render_to_response('signin.html', RequestContext(request))


def signout(request):
    logout(request)
    return render_to_response('signin.html', RequestContext(request))


class ClientList(APIView):

    def get_object(self, pk):
        try:
            return Client.objects.get(id=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ProjectList(APIView):

    def get(self, request, format=None):
        clients = Project.objects.all()
        serializer = ProjectSerializer(clients, many=True)
        return Response(serializer.data)


class ProjectDetail(APIView):

    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class TimeSheetDetail(APIView):

    def get_object(self, pk):
        try:
            return TimeSheet.objects.get(id=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        timesheet = self.get_object(pk)
        serializer = TimeSheetSerializer(timesheet)
        return Response(serializer.data)


class TimeSheetList(APIView):

    def get(self, request, format=None):
        timesheets = TimeSheet.objects.all()
        serializer = TimeSheetSerializer(timesheets, many=True)
        return Response(serializer.data)


class Report(APIView):

    def get(self, request, pk, format=None):
        client = Client.objects.get(id=pk)
        projects = Project.objects.filter(client__id=pk)
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
                res = project.annual_report()
            else:
                res = client.annual_report()
            return Response(res)

        for project in projects:
            cost_per_hour = project.cost_per_hour
            total_time_spent = TimeSheet.objects.filter(project=project).aggregate(
                total_time_spent=Sum('time_spent'))['total_time_spent']
            total_cost = total_time_spent * cost_per_hour
            res.append({'name': project.id, 'total_cost': total_cost,
                        'total_time_spent': total_time_spent, 'cost_per_hour': project.cost_per_hour})
        return Response(res)
