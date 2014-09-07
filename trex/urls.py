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
    url(r"^projects/$",
        project.ProjectListCreateAPIView.as_view(),
        name="project-list"),
    url(r"^projects/(?P<pk>[0-9]+)/$",
        project.ProjectDetailAPIView.as_view(),
        name="project-detail"),
    url(r"^entries/(?P<pk>[0-9]+)/$",
        project.EntryDetailAPIView.as_view(),
        name="entry-detail"),
)
