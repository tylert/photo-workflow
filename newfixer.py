#!/usr/bin/env python3


# gir1.2-gexiv2-0.10


from gi.repository import GExiv2


def rename_photo_and_dump_exif(old_photo_filename):
    exif = GExiv2.Metadata('')
