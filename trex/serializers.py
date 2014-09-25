# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from rest_framework.serializers import (
    HyperlinkedModelSerializer, HyperlinkedIdentityField,
)

from trex.models.project import Project, Entry, Tag, ProjectUser


class ProjectSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ("url", "id", "name", "description", "active", "created")


class ProjectDetailSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the details of a Project
    """

    entries = HyperlinkedIdentityField(view_name="project-entries-list")
    tags = HyperlinkedIdentityField(view_name="project-tags-list")
    users = HyperlinkedIdentityField(view_name="project-users-list")

    class Meta:
        model = Project
        fields = ("id", "name", "description", "active", "created", "entries",
                  "tags", "users")


class EntryTagsSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the Tags of an Entry
    """

    class Meta:
        model = Tag
        fields = ("url", "id", "name")


class EntryProjectSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the Project of an Entry
    """

    class Meta:
        model = Project
        fields = ("url", "id", "name")


class EntryDetailSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the details of an Entry
    """

    tags = EntryTagsSerializer(many=True)
    project = EntryProjectSerializer()

    class Meta:
        model = Entry
        fields = ("url", "id", "date", "duration", "description", "state",
                  "user", "created", "project", "tags")


class ProjectUserSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the Users of a Project
    """

    class Meta:
        model = ProjectUser
        fields = ("id", "user_abbr")


class ProjectEntrySerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the Entries of a Project
    """

    tags = EntryTagsSerializer(many=True)
    user = ProjectUserSerializer()

    class Meta:
        model = Entry
        fields = ("url", "id", "date", "duration", "description", "state",
                  "user", "created", "tags")


class ProjectTagSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the Tags of a Project
    """

    class Meta:
        model = Tag
        fields = ("id", "name", "description", "created")


class TagDetailSerializer(HyperlinkedModelSerializer):
    """
    Serializer to show the details of a Tag
    """

    class Meta:
        model = Tag
        fields = ("id", "project", "name", "description", "created")
