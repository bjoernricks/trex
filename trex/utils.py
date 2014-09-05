# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

import re

from datetime import date, timedelta

from django.utils.encoding import force_unicode


class ZeitEntry(object):

    """
    Representation of one entry in a zeiterfassung.txt
    """

    def __init__(self, line_number, day, month, year, hours, minutes, state,
                 user, workpackage, description):
        self.line_nr = line_number
        self.day = day
        self.month = month
        self.year = year
        self.hours = hours
        self.minutes = minutes
        self.state = state
        self.user = user
        self.wp = workpackage
        self.desc = description or ""

    def add_desc(self, desc):
        self.desc = u"%s %s" % (force_unicode(self.desc), force_unicode(desc))

    def __str__(self):
        return u"%s.%s.%s %s:%s %s %s [%s] %s" % (
            self.day, self.month, self.year,
            self.hours, self.minutes,
            self.get_state(), self.get_user(),
            self.get_workpackage(), self.get_description())

    def get_duration(self):
        # requires python 2.7
        return timedelta(minutes=self.minutes, hours=self.hours).total_seconds()

    def get_date(self):
        return date(self.year, self.month, self.day)

    def get_state(self):
        return self.state

    def get_description(self):
        return self.desc

    def get_workpackage(self):
        return self.wp

    def get_user(self):
        return self.user

    def get_line_number(self):
        return self.line_nr


class Zeiterfassung(object):

    """
    Reads entries from a zeiterfassung.txt formatted iterable
    """

    zeitline = re.compile(
        "(?P<day>[0-9]{2})\.(?P<month>[0-9]{2})\.(?P<year>[0-9]{4})\s+"
        "(?P<hour>\d+)\:(?P<minutes>\d{2})h\s(?P<state>.)\s+(?P<user>\w+)\s+"
        "\[(?P<ap>[a-zA-Z0-9_\-]+)\]\s+(?P<desc>.*)"
    )

    zeitline_comment = re.compile("\s+(?P<desc>.*)")

    def __init__(self, zeiterfassung):
        self.zeiterfassung = zeiterfassung

    def read(self):
        entry = None
        for nr, line in enumerate(self.zeiterfassung, start=1):
            zmatch = self.zeitline.match(line)
            zcmatch = self.zeitline_comment.match(line)
            if zmatch:
                # matches a zeiterfassung line
                if entry:
                    # a new entry has stated add the last one
                    yield entry

                entry = ZeitEntry(
                    line_number=nr,
                    day=int(zmatch.group("day")),
                    month=int(zmatch.group("month")),
                    year=int(zmatch.group("year")),
                    hours=int(zmatch.group("hour")),
                    minutes=int(zmatch.group("minutes")),
                    state=force_unicode(zmatch.group("state")),
                    user=force_unicode(zmatch.group("user")),
                    workpackage=force_unicode(zmatch.group("ap")),
                    description=force_unicode(zmatch.group("desc"))
                    )
            elif entry and zcmatch:
                # matches an longer description in the next line for a
                # zeiterfassung line
                entry.add_desc(zcmatch.group("desc").rstrip())
            elif entry:
                # additional content -> end of an entry
                yield entry
                entry = None

        if entry:
            # add the last parsed entry
            yield entry
