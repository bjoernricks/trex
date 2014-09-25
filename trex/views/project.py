# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from rest_framework import generics, status
from rest_framework.response import Response

import trex.filters as filters

from trex.models.project import Project, Entry, Tag
from trex.parsers import PlainTextParser
from trex.serializers import (
    ProjectSerializer, ProjectDetailSerializer, EntryDetailSerializer,
    TagDetailSerializer, ProjectEntrySerializer, ProjectTagSerializer,
    ProjectUserSerializer,
)
from trex.utils import Zeiterfassung


class ProjectListCreateAPIView(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class ProjectZeiterfassungAPIView(generics.CreateAPIView):

    queryset = Project.objects.all()
    parser_classes = (PlainTextParser,)
    serializer_class = ProjectDetailSerializer

    def create(self, request, *args, **kwargs):
        try:
            proj = self.get_object()
        except Project.DoesNotExist:
            errors = self._create_errors("Project does not exist")
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        zeiterfassung = Zeiterfassung(request.DATA)
        try:
            proj.create_entries_from_zeiterfassung(zeiterfassung)
        except Exception, e:
            errors = self._create_errors(str(e))
            # TODO review if e could contain info not suited for the user
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(proj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def _create_errors(self, msg):
        return {"non_field_errors": [msg]}


class ProjectMixin(object):

    def get_project_queryset(self):
        return Project.objects.all()

    def get_project(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        filter = {
            "pk": pk,
        }
        return self.get_project_queryset().get(**filter)


class ProjectEntriesListAPIView(ProjectMixin, generics.ListAPIView):

    serializer_class = ProjectEntrySerializer
    filter_class = filters.EntryFilter

    def get_queryset(self):
        project = self.get_project()
        return project.entries.all().order_by("id")


class ProjectTagsListAPIView(ProjectMixin, generics.ListAPIView):

    serializer_class = ProjectTagSerializer
    filter_class = filters.TagFilter

    def get_queryset(self):
        project = self.get_project()
        return project.tags.all().order_by("id")


class ProjectUsersListAPIView(ProjectMixin, generics.ListAPIView):

    serializer_class = ProjectUserSerializer
    filter_class = filters.ProjectUserFilter

    def get_queryset(self):
        project = self.get_project()
        return project.project_users.all().order_by("user_abbr")


class EntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Entry.objects.all()
    serializer_class = EntryDetailSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Tag.objects.all()
    serializer_class = TagDetailSerializer
