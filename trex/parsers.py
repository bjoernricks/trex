# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from io import TextIOWrapper, BytesIO

from django.core.handlers.wsgi import WSGIRequest

from rest_framework.parsers import BaseParser


class PlainTextParser(BaseParser):

    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        charset = self.get_charset(media_type)
        if charset:

            if isinstance(stream, WSGIRequest):
                stream = BytesIO(stream.read())

            stream = TextIOWrapper(stream, encoding=charset)

        return stream

    def get_charset(self, media_type):
        if not media_type:
            return None

        charset = None
        msplit = media_type.split(" ")
        for m in msplit:
            m = m.strip()
            if "charset" in m:
                csplit = m.split("=")
                if len(csplit) > 1:
                    charset = csplit[1]
                    return charset.strip().lower()
        return None
