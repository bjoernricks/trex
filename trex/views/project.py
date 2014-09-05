# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from rest_framework import generics

from trex.models.project import Project, Entry
from trex.serializers import (
    ProjectSerializer, ProjectDetailSerializer, EntryDetailSerializer)


class ProjectListCreateAPIView(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class EntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Entry.objects.all()
    serializer_class = EntryDetailSerializer
