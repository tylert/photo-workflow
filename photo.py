import pyexiv2
import sys
#import datetime

try:
  metadata = pyexiv2.ImageMetadata(sys.argv[1])
  metadata.read()
except:
  sys.exit('No valid exif header found.')

try:
  name = metadata['Exif.Photo.DateTimeDigitized'].value.strftime('%Y-%m-%d-%H-%M-%S')
except:
  try:
    name = metadata['Exif.Image.DateTime'].value.strftime('%Y-%m-%d-%H-%M-%S')
  except:
    sys.exit('No valid date time found.')

try:
  with open(name + '.exif', 'w') as exiffile:
    exiffile.write('{}\n'.format(metadata.mime_type))

    for key in sorted(metadata.exif_keys):
      exiffile.write('{} = \'{}\'\n'.format(key, metadata[key].human_value))
except:
  sys.exit('Unable to open exif text file for writing.')


#if __name__ == '__main__':


#jhead -autorot *.jpg
#jhead -nf%Y%m%d-%H%M%S *.jpg
#nice -n5 ufraw-batch --out-type=jpeg --overwrite */*.nef
