from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import billcalc.views as views

urlpatterns = [
    url('^api/clients/$', views.ClientList.as_view()),
    url('^api/projects/$', views.ProjectList.as_view()),
    url('^api/timesheets/$', views.TimeSheetList.as_view()),
]
