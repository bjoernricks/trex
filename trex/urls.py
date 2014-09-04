from django.conf.urls import patterns, include, url
from django.contrib import admin

from trex.views.project import (
    ProjectListCreateAPIView, ProjectDetailAPIView)


urlpatterns = patterns(
    '',
    url(r"^admin/", include(admin.site.urls)),
    url(r"^projects/$", ProjectListCreateAPIView.as_view(),
        name="project-list"),
    url(r"^projects/(?P<pk>[0-9]+)/$", ProjectDetailAPIView.as_view(),
        name="project-details"),
)
