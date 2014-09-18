# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

import django_filters

from django import forms
from django.db.models import Q

from trex.models import Entry, Tag


class MultipleTextFilter(django_filters.Filter):
    field_class = forms.CharField

    def filter(self, qs, value):

        if not value:
            return qs

        if self.lookup_type:
            lookup = "__%s" % self.lookup_type
        else:
            lookup = ""

        q = Q()
        for v in value.split(","):
            q |= Q(**{"%s%s" % (self.name, lookup): v})

        qs = qs.filter(q)

        if self.distinct:
            qs = qs.distinct()
        return qs


class EntryFilter(django_filters.FilterSet):

    from_date = django_filters.DateFilter(name="date", lookup_type="gte")
    to_date = django_filters.DateFilter(name="date", lookup_type="lte")

    class Meta:
        model = Entry
        fields = ["from_date", "to_date", "state"]


class TagFilter(django_filters.FilterSet):

    name = MultipleTextFilter(name="name")
    name_like = MultipleTextFilter(name="name", lookup_type="contains")
    description = django_filters.CharFilter(name="description",
                                            lookup_type="contains")

    class Meta:
        model = Tag
        fields = ["name", "description"]