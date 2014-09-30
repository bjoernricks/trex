# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):

    help = "Create a SECRET_KEY for settings.py"

    option_list = BaseCommand.option_list + (
        make_option("-o", "--out", dest="file",
                    help="File to write the generated key"),
    )

    def handle(self, *args, **options):
        # see django/core/management/commands/startproject.py
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)

        filename = options.get("file")
        if filename:
            with open(filename, "w") as f:
                f.write(secret_key)
                f.write("\n")
        else:
            print secret_key
