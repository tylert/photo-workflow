#!/usr/bin/env python

# debian packages used:
#   python-pyexiv2
#   python-magic (may need to use file instead)

import os
import stat
import sys
import shutil
import datetime
import pyexiv2


def rename_photo_and_dump_exif(old_photo_filename):
    '''Extract info from the exif header to rename the file and move it'''

    # Remove dumb permissions.
    try:
        os.chmod(old_photo_filename,
                  stat.S_IWUSR|stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)
    except:
        sys.exit('Unable to chmod {}.'.format(old_photo_filename))

    # Extract the exif header.
    try:
        metadata = pyexiv2.ImageMetadata(old_photo_filename)
        metadata.read()
    except:
        sys.exit('Unable to find a valid exif header in {}.'
                 .format(old_photo_filename))

    # Find the file type.
    try:
        a_type = metadata.mime_type
    except:
        # try:
        #     see if its a video file
        # except:
        sys.exit('Unable to determine image type for {}.'
                 .format(old_photo_filename))

    if a_type == 'image/x-nikon-nef':
        new_photo_extension = '.nef'
    # elif a_type == 'image/canon-something':
    #     new_photo_extension = '.cr2'
    elif a_type == 'image/jpeg':
        new_photo_extension = '.jpg'
    else:
        new_photo_extension = os.path.splitext(old_photo_filename)[-1].lower()

    # Find a datetime string.
    try:
        a_photo_date = metadata['Exif.Photo.DateTimeDigitized'].value
    except:
        try:
            a_photo_date = metadata['Exif.Image.DateTime'].value
        except:
            # try:
            #     a_photo_date = datetime.datetime.fromtimestamp(
            #                    os.stat(old_photo_filename).st_ctime)
            # except:
            sys.exit('Unable to find a valid timestamp in {}.'
                     .format(old_photo_filename))

    # Work with the actual files.
    try:
        an_album_location = a_photo_date.strftime('%Y') + os.sep + \
            a_photo_date.strftime('%Y-%m-%d')
        new_photo_basename = an_album_location + os.sep + \
            a_photo_date.strftime('%Y-%m-%d-%H-%M-%S')
        new_photo_filename = new_photo_basename + new_photo_extension
        new_exif_filename = new_photo_filename + '.txt'

        if not os.path.exists(an_album_location):
            os.makedirs(an_album_location)
    except:
        sys.exit('Unable to build a valid filename for {}'
                 .format(old_photo_filename))

    # Move the photo into the correct album.
    try:
        if not os.path.exists(new_photo_filename):
            shutil.move(old_photo_filename, new_photo_filename)
        else:
            new_photo_filename = new_photo_basename + 'a' + new_photo_extension
            if not os.path.exists(new_photo_filename):
                shutil.move(old_photo_filename, new_photo_filename)
            else:
                new_photo_filename = new_photo_basename + 'b' + \
                    new_photo_extension
                if not os.path.exists(new_photo_filename):
                    shutil.move(old_photo_filename, new_photo_filename)
                else:
                    sys.exit('Unable to rename {}'.format(old_photo_filename))
    except:
        sys.exit('Unable to move photo {}.'.format(old_photo_filename))

    # Dump the exif fields.
    try:
        if not os.path.exists(new_exif_filename):
            with open(new_exif_filename, 'wt') as an_exif_file:
                for key in sorted(metadata.exif_keys):
                    an_exif_file.write('{} = {}\n'
                                       .format(key, metadata[key].human_value))
    except:
        sys.exit('Unable to write exif data {}.'.format(new_exif_filename))


if __name__ == '__main__':
    import sys

    rename_photo_and_dump_exif(sys.argv[1])


# nice -n5 ufraw-batch --out-type=jpeg --overwrite */*.nef


# case `jpegexiforient -n "$i"` in
# 1) transform="";;
# 2) transform="-flip horizontal";;
# 3) transform="-rotate 180";;
# 4) transform="-flip vertical";;
# 5) transform="-transpose";;
# 6) transform="-rotate 90";;
# 7) transform="-transverse";;
# 8) transform="-rotate 270";;
# *) transform="";;
# esac
# jpegtran $transform
