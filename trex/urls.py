# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

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
