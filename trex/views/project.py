# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from django.http import Http404

from rest_framework import generics, status
from rest_framework.response import Response

from trex.models.project import Project, Entry, Tag
from trex.parsers import PlainTextParser
from trex.serializers import (
    ProjectSerializer, ProjectDetailSerializer, EntryDetailSerializer,
    TagDetailSerializer, ProjectEntrySerializer, ProjectTagSerializer,
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


class ProjectEntriesListAPIView(generics.ListAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectEntrySerializer

    def list(self, request, *args, **kwargs):
        proj = self.get_object()
        self.object_list = proj.entries.all()
        page = self.paginate_queryset(self.object_list)

        if not self.allow_empty and not self.object_list:
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)


class ProjectTagsListAPIView(generics.ListAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectTagSerializer

    def list(self, request, *args, **kwargs):
        proj = self.get_object()
        self.object_list = proj.tags.all()
        page = self.paginate_queryset(self.object_list)

        if not self.allow_empty and not self.object_list:
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)


class EntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Entry.objects.all()
    serializer_class = EntryDetailSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Tag.objects.all()
    serializer_class = TagDetailSerializer
