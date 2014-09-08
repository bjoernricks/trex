# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from django.conf.urls import patterns, include, url
from django.contrib import admin

from trex.views import project

urlpatterns = patterns(
    '',
    url(r"^admin/", include(admin.site.urls)),
    url(r"^api/1/projects/$",
        project.ProjectListCreateAPIView.as_view(),
        name="project-list"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/$",
        project.ProjectDetailAPIView.as_view(),
        name="project-detail"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/entries$",
        project.ProjectEntriesListAPIView.as_view(),
        name="project-detail"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/zeiterfassung/$",
        project.ProjectZeiterfassungAPIView.as_view(),
        name="project-zeiterfassung"),
    url(r"^api/1/entries/(?P<pk>[0-9]+)/$",
        project.EntryDetailAPIView.as_view(),
        name="entry-detail"),
)
