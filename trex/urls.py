# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from trex.views import project

urlpatterns = patterns(
    '',
    url(r"^$",
        TemplateView.as_view(template_name="index.html"),
        name="index",
        ),
    url(r"^api/1/projects/?$",
        project.ProjectListCreateAPIView.as_view(),
        name="project-list"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/$",
        project.ProjectDetailAPIView.as_view(),
        name="project-detail"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/entries/?$",
        project.ProjectEntriesListAPIView.as_view(),
        name="project-entries-list"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/entries/sums/?$",
        project.ProjectEntrySumsAPIView.as_view(),
        name="project-entries-sums"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/tags/?$",
        project.ProjectTagsListAPIView.as_view(),
        name="project-tags-list"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/users/?$",
        project.ProjectUsersListAPIView.as_view(),
        name="project-users-list"),
    url(r"^api/1/projects/(?P<pk>[0-9]+)/zeiterfassung/?$",
        project.ProjectZeiterfassungAPIView.as_view(),
        name="project-zeiterfassung"),
    url(r"^api/1/entries/(?P<pk>[0-9]+)/?$",
        project.EntryDetailAPIView.as_view(),
        name="entry-detail"),
    url(r"^api/1/tags/(?P<pk>[0-9]+)/?$",
        project.TagDetailAPIView.as_view(),
        name="tag-detail"),
)
