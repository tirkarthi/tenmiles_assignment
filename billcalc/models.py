from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    company_info = models.CharField(max_length=200)

class Project(models.Model):
    client = models.ForeignKey(Client)
    start_date = models.DateField()
    cost_per_hour = models.FloatField()

class TimeSheet(models.Model):
    project = models.ForeignKey(Project)
    date = models.DateField()
    time_spent = models.FloatField()
