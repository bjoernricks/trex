# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from rest_framework import generics, status
from rest_framework.response import Response

from trex.models.project import Project, Entry
from trex.parsers import PlainTextParser
from trex.serializers import (
    ProjectSerializer, ProjectDetailSerializer, EntryDetailSerializer)
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


class ProjectEntriesListAPIView(generics.ListAPIView):

    queryset = Project.objects.all()
    serializer_class = EntryDetailSerializer


class EntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Entry.objects.all()
    serializer_class = EntryDetailSerializer
