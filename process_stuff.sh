#!/usr/bin/env bash

# Fix permissions
find . -type d -print0 | xargs -0 chmod 0755
find . -type f -print0 | xargs -0 chmod 0644

# Fix filenames
# perl-rename 's/IMG_(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)/$1-$2-$3-$4-$5-$6/g' *.jpg
perl-rename 's/VID_(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)/$1-$2-$3-$4-$5-$6/g' *.mp4
# find . -name '*.jpg' | xargs exiv2 -r '%Y-%m-%d-%H-%M-%S' -F -v rename
jhead -n%Y-%m-%d-%H-%M-%S *.jpg

# Create directory structure and move stuff under it
# (e.g.:  "2020/2020-12-25/2020-12-25-12-34-56.jpg")
for photo in *.jpg; do
    mkdir -p ${photo:0:4}/${photo:0:10}
    mv -v ${photo} ${photo:0:4}/${photo:0:10}
done
