# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from rest_framework.serializers import (
    HyperlinkedModelSerializer, HyperlinkedIdentityField,
)

from trex.models.project import Project, Entry, Tag


class ProjectSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ("url", "id", "name", "description", "active", "created")


class ProjectDetailSerializer(HyperlinkedModelSerializer):

    entries = HyperlinkedIdentityField(view_name="project-entries-list")

    class Meta:
        model = Project
        fields = ("id", "name", "description", "active", "created", "entries")


class EntryTagsSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ("url", "id", "name")


class EntryProjectSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ("url", "id", "name")


class EntryDetailSerializer(HyperlinkedModelSerializer):

    tags = EntryTagsSerializer(many=True)
    project = EntryProjectSerializer()

    class Meta:
        model = Entry
        fields = ("url", "id", "date", "duration", "description", "state",
                  "user_abbr", "user", "created", "project", "tags")


class TagDetailSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "project", "name", "description", "created")
