# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

import django_filters

from trex.models import Entry


class EntryFilter(django_filters.FilterSet):

    from_date = django_filters.DateFilter(name="date", lookup_type="gte")
    to_date = django_filters.DateFilter(name="date", lookup_type="lte")

    class Meta:
        model = Entry
        fields = ["from_date", "to_date", "state"]
