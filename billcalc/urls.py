from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import billcalc.views as views
import billcalc.api as api

urlpatterns = [
    url('^$', views.signin, name="signin"),
    url('^signin/$', views.signin, name="signin"),
    url('^signup/$', views.signup, name="signup"),
    url('^signout/$', views.signout, name="signout"),
    url('^dashboard/$', views.dashboard, name="dashboard"),
    url('^projects/(?P<pk>[0-9]+)$',
        views.project_dashboard, name="project-dashboard"),
    url('^add_entry/$', views.add_entry, name="add-entry"),
    url('^api/clients/$', api.ClientView.as_view(), name="api-client-detail"),
    url('^api/projects/$', api.ProjectList.as_view(), name="api-project-list"),
    url('^api/projects/(?P<pk>[0-9]+)$', api.ProjectDetail.as_view(), name="api-project-detail"),
    url('^api/timesheets/$', api.TimeSheetList.as_view(), name="api-timesheet-list"),
    url('^api/timesheets/(?P<pk>[0-9]+)$', api.TimeSheetDetail.as_view(), name="api-timesheet-detail"),
    url('^api/reports/(?P<pk>[0-9]+)$', api.Report.as_view(), name="api-reports"),
]
