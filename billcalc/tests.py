from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

import datetime

from .models import *

class APITestCase(APITestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.username = 'q@q.com'
        self.password = 'q'
        self.client = APIClient()
        self.client.login(username=self.username, password=self.password)

    def test_get_projects(self):
        url = reverse('api-project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_timesheets(self):
        url = reverse('api-timesheet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
        
    def test_create_projects(self):
        url = reverse('api-project-list')
        response = self.client.get(url)
        initial_count = len(response.data)

        url = reverse('api-project-list')
        client = Client.objects.get(user=User.objects.get(username=self.username))
        response = self.client.post('/api/projects/', {'start_date' : datetime.date.today() - datetime.timedelta(days=10), 'cost_per_hour' : 12, client: client})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api-project-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), initial_count + 1)


    def test_future_date(self):
        url = reverse('api-project-list')
        client = Client.objects.get(user=User.objects.get(username=self.username))
        response = self.client.post(url, {'start_date' : datetime.date.today() + datetime.timedelta(days=10), 'cost_per_hour' : 12, client: client})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_timesheets(self):
        url = reverse('api-timesheet-list')
        response = self.client.get(url)
        initial_count = len(response.data)

        client = Client.objects.get(user=User.objects.get(username=self.username))
        project = Project.objects.filter(client=client)[0]
        response = self.client.post(url, {'date' : project.start_date + datetime.timedelta(days=5), 'time_spent' : 12, 'project': project.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(len(response.data), initial_count + 1)
        
        response = self.client.post(url, {'date' : project.start_date - datetime.timedelta(days=5), 'time_spent' : 12, 'project': project.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.get(url)
        self.assertEqual(len(response.data), initial_count + 1)
