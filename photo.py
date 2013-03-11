import pyexiv2
import sys
import os
#import datetime

oldfilename = sys.argv[1]
oldextension = os.path.splitext(oldfilename)[-1]

# Try to find the exif header.
try:
  metadata = pyexiv2.ImageMetadata(oldfilename)
  metadata.read()
except:
  sys.exit('Unable to find a valid exif header.')

# Extract the timestamp to use as a filename.
try:
  newbasename = metadata['Exif.Photo.DateTimeDigitized'].value.strftime('%Y-%m-%d-%H-%M-%S')
except:
  try:
    newbasename = metadata['Exif.Image.DateTime'].value.strftime('%Y-%m-%d-%H-%M-%S')
  except:
    sys.exit('Unable to find a valid exif timestamp.')

try:
  if metadata.mime_type == 'image/x-nikon-nef':
    newextension = 'nef'
  #else if metadata.mime_type == 'image/jpeg':
  else:
    newextension = 'jpg'
except:
  sys.exit('Unable to determine image type from header.')

# Output all the exif fields as text.
try:
  newfilename = newbasename + '.' + newextension

  with open(newfilename + '.exif', 'w') as exiffile:
    for key in sorted(metadata.exif_keys):
      exiffile.write('{} = \'{}\'\n'.format(key, metadata[key].human_value))
except:
  sys.exit('Unable to open text file for writing.')


#if __name__ == '__main__':


#jhead -autorot *.jpg
#jhead -nf%Y%m%d-%H%M%S *.jpg
#nice -n5 ufraw-batch --out-type=jpeg --overwrite */*.nef
