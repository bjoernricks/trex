# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

import warnings

from django.core.paginator import Page

from rest_framework.serializers import (
    HyperlinkedModelSerializer, HyperlinkedIdentityField,
)

from trex.models.project import Project, Entry, Tag, ProjectUser


class UpdateDataSerializerMixin(object):

    @property
    def data(self):
        """
        Returns the serialized data on the serializer.
        """
        if self._data is None:

            data = self.get_data()

            self.update_data(data)

            self._data = data

        return self._data

    def update_data(self, data):
        """
        Update and add additional data here
        """

    def get_data(self):
        """
        Serializes an model instance or queryset to primitive data
        """
        obj = self.object

        if self.many is not None:
            many = self.many
        else:
            many = hasattr(obj, '__iter__') and not isinstance(
                obj, (Page, dict))
            if many:
                warnings.warn('Implicit list/queryset serialization '
                              'is deprecated. Use the `many=True` flag '
                              'when instantiating the serializer.',
                              DeprecationWarning, stacklevel=2)

        if many:
            return [self.to_native(item) for item in obj]
        else:
            return self.to_native(obj)


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
                  "user", "created", "project", "workpackage", "tags")


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
                  "user", "created", "workpackage", "tags")


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
