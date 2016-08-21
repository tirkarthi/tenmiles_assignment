from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(
        User, null=True, verbose_name='user', related_name='user_profile')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    company_info = models.CharField(max_length=200)

    def weekly_report(self):
        res = []
        for entry in TimeSheet.objects.raw("select t.id, week(t.date) as week, sum(t.time_spent * p.cost_per_hour) as cost from billcalc_timesheet as t join billcalc_project as p on p.id = t.project_id and p.client_id = %s group by week(t.date)", [self.id]):
            res.append({"week": entry.week, "cost": entry.cost})
        return res

    def monthly_report(self):
        res = []
        for entry in TimeSheet.objects.raw("select t.id, month(t.date) as month, sum(t.time_spent * p.cost_per_hour) as cost from billcalc_timesheet as t join billcalc_project as p on p.id = t.project_id and p.client_id = %s group by month(t.date)", [self.id]):
            res.append({"month": entry.month, "cost": entry.cost})
        return res

    def yearly_report(self):
        res = []
        for entry in TimeSheet.objects.raw("select t.id, year(t.date) as year, sum(t.time_spent * p.cost_per_hour) as cost from billcalc_timesheet as t join billcalc_project as p on p.id = t.project_id and p.client_id = %s group by year(t.date)", [self.id]):
            res.append({"year": entry.year, "cost": entry.cost})
        return res


class Project(models.Model):
    client = models.ForeignKey(Client)
    start_date = models.DateField()
    cost_per_hour = models.FloatField()

    def calculate_cost(self, time_spent, project):
        project_cost = project.cost_per_hour
        return project_cost * time_spent

    def weekly_report(self):
        project = self
        project_id = project.id
        project_start_date = project.start_date
        res = []
        for entry in TimeSheet.objects.raw("select id, sum(time_spent) as time_spent, week(date) as week from billcalc_timesheet where project_id= %s group by week(date)", [project_id]):
            week = abs(entry.week - project_start_date.isocalendar()[1] + 1)
            time_spent = entry.time_spent
            cost = self.calculate_cost(time_spent, project)
            res.append({"time_spent": time_spent, "week": week, "cost": cost})
        return res

    def monthly_report(self):
        project = self
        project_id = project.id
        project_start_date = project.start_date
        res = []
        for entry in TimeSheet.objects.raw("select id, sum(time_spent) as time_spent, month(date) as month from billcalc_timesheet where project_id= %s group by month(date)", [project_id]):
            month = abs(entry.month - project_start_date.month + 1)
            time_spent = entry.time_spent
            cost = self.calculate_cost(time_spent, project)
            res.append(
                {"time_spent": time_spent, "month": month, "cost": cost})
        return res

    def yearly_report(self):
        project = self
        project_id = project.id
        project_start_date = project.start_date
        res = []
        for entry in TimeSheet.objects.raw("select id, sum(time_spent) as time_spent, year(date) as year from billcalc_timesheet where project_id= %s group by year(date)", [project_id]):
            year = abs(entry.year - project_start_date.year + 1)
            time_spent = entry.time_spent
            cost = self.calculate_cost(time_spent, project)
            res.append({"time_spent": time_spent, "year": year, "cost": cost})
        return res


class TimeSheet(models.Model):
    project = models.ForeignKey(Project)
    date = models.DateField()
    time_spent = models.FloatField()
