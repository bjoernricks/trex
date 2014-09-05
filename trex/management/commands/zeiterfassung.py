# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from django.core.management.base import BaseCommand, CommandError

from trex.models.project import Project
from trex.utils import Zeiterfassung


class Command(BaseCommand):

    args = "<project> <name>"
    help = "Load entries from a zeiterfassung.txt to a project"

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError("You must specifiy a project name and a "
                               "zeiterfassung.txt")

        name = args[0]
        zeiterfassung_txt = args[1]

        try:
            project = Project.objects.get(name=name)
        except Project.DoesNotExist:
            raise CommandError("Unknown project name %s" % name)

        with open(zeiterfassung_txt, "r") as f:
            zeiterfassung = Zeiterfassung(f)
            created = project.create_entries_from_zeiterfassung(zeiterfassung)
            self.stdout.write(u"Loaded %s entries" % created)
