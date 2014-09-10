# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from rest_framework.serializers import (
    HyperlinkedModelSerializer, HyperlinkedIdentityField,
)

from trex.models.project import Project, Entry


class ProjectSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ("url", "id", "name", "description", "active", "created")


class ProjectDetailSerializer(HyperlinkedModelSerializer):

    entries = HyperlinkedIdentityField(view_name="project-entries-list")

    class Meta:
        model = Project
        fields = ("id", "name", "description", "active", "created", "entries")


class EntryDetailSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Entry
        fields = ("date", "duration", "description", "state", "user", "created")
