# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from trex.models.project import Project
from trex.utils import Zeiterfassung


class Command(BaseCommand):

    args = "<project> <name>"
    help = "Load entries from a zeiterfassung.txt to a project"

    option_list = BaseCommand.option_list + (
        make_option("-e", "--encoding", dest="encoding", default="utf-8",
                    help="Encoding of the input file", type="string"),
        make_option("--report-skipped", dest="skipped", action="store_true",
                    default=False, help="Show details of skipped entries")
    )

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError("You must specifiy a project name and a "
                               "zeiterfassung.txt")

        name = args[0]
        zeiterfassung_txt = args[1]

        encoding = options.get("encoding")

        try:
            project = Project.objects.get(name=name)
        except Project.DoesNotExist:
            raise CommandError("Unknown project name %s" % name)

        with open(zeiterfassung_txt, "r") as f:
            zeiterfassung = Zeiterfassung(f, encoding)
            written, skipped = project.create_entries_from_zeiterfassung(
                zeiterfassung)
            self.stdout.write(u"Wrote %s loaded entries. %s entries have been "
                              u"skipped." % (len(written), len(skipped)))
            if options.get("skipped", False) and skipped:
                self.stdout.write(u"Skipped entries:")
                for entry in skipped:
                    self.stdout.write(u"Line: %s %s %s" % (
                        entry.get_line_number(), entry.get_user(),
                        entry.get_description))
