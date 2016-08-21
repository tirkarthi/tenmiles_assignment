from django.shortcuts import render_to_response, redirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def signin(request):
    if request.method == "POST":
        password = request.POST.get("password", "")
        email_id = request.POST.get("email", "")
        user = authenticate(username=email_id, password=password)
        if user:
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            error = {"message": "Invalid email or password"}
            return render_to_response('signin.html', error, RequestContext(request))

    return render_to_response('signin.html', RequestContext(request))


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        company_info = request.POST.get("company_info", "")

        user = User.objects.filter(email=email)

        if user:
            error = {"message": "Email already exists"}
            return render_to_response('signup.html', error, RequestContext(request))
        else:
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
    client, created = Client.objects.get_or_create(user=user)
    name = client.name
    company_info = client.company_info
    monthly_report = client.monthly_report()
    weekly_report = client.weekly_report()
    yearly_report = client.yearly_report()
    return render_to_response('dashboard.html', {"weekly": weekly_report, "monthly": monthly_report, "yearly": yearly_report, "name": name, "company_info": company_info}, RequestContext(request))


def signout(request):
    logout(request)
    return render_to_response('signin.html', RequestContext(request))


@login_required
def add_entry(request):
    user = request.user
    client = Client.objects.get(user=user)
    projects = Project.objects.filter(client=client)
    timesheets = []
    for project in projects:
        timesheet_entries = TimeSheet.objects.filter(project=project)
        for timesheet in timesheet_entries:
            timesheets.append(timesheet)
    return render_to_response('add_entry.html', {"name": client.name, "company_info": client.company_info, "projects": projects, "timesheets": timesheets}, RequestContext(request))


@login_required
def project_dashboard(request, pk):
    client = Client.objects.get(user=request.user)
    project = Project.objects.get(id=pk, client=client)
    name = client.name
    company_info = client.company_info
    monthly_report = project.monthly_report()
    weekly_report = project.weekly_report()
    yearly_report = project.yearly_report()
    return render_to_response('project_report.html', {"weekly": weekly_report, "monthly": monthly_report, "yearly": yearly_report, "name": name, "company_info": company_info, "project": project}, RequestContext(request))
