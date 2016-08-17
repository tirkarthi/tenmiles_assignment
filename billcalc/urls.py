from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import billcalc.views as views

urlpatterns = [
    url('^signin/$', views.signin, name="signin"),
    url('^signup/$', views.signup, name="signup"),
    url('^signout/$', views.signout, name="signout"),
    url('^dashboard/$', views.dashboard, name="dashboard"),
    url('^api/clients/$', views.ClientList.as_view()),
    url('^api/projects/$', views.ProjectList.as_view()),
    url('^api/projects/(?P<pk>[0-9]+)$', views.ProjectDetail.as_view()),
    url('^api/timesheets/$', views.TimeSheetList.as_view()),
    url('^api/timesheets/(?P<pk>[0-9]+)$', views.TimeSheetDetail.as_view()),
    url('^api/reports/(?P<pk>[0-9]+)$', views.Report.as_view()),
]
