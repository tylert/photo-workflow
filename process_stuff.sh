#!/usr/bin/env bash

# Fix permissions
find . -type d -print0 | xargs -0 chmod 0755
find . -type f -print0 | xargs -0 chmod 0644

# Fix filenames
jhead -autorot -exonly -n%Y-%m-%d-%H-%M-%S *.jpg

# Create directory structure and move stuff under it
# (e.g.:  "2020/2020-12-25/2020-12-25-12-34-56.jpg")
for photo in *.jpg; do
    mkdir -pv ${photo:0:4}/${photo:0:10}
    mv -iv ${photo} ${photo:0:4}/${photo:0:10}
done
