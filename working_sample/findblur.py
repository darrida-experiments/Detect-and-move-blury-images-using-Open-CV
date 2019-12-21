# NOTE: last try before it somehow worked was pip3 install opencv-python
#
# Sorts pictures in current directory into two subdirs, blurred and ok
# Found original here: https://photo.stackexchange.com/questions/20432/is-there-photo-analysis-software-which-will-pre-sort-images-by-identifying-poten
# Modified for my own purposes.
#

# stock python libs
import os, shutil, re, sys
# additional libs
import cv2

# DEFAULTS
FOCUS_THRESHOLD = 20
DIRECTORY = '.'
EXT = '.jpg'

HELP_MESSAGE = f"""
This tool assists with blur dectection on images. The follow parameters are available:

FOCUS_THRESHOLD => --focus <int>   [0-100]
      DIRECTORY => --dir <path>    [i.e., ./dir1/dir2/dir3 or C:/dir1/dir2/dir3]
            EXT => --ext <ext>     [.jpg, jpeg, etc]
              
Defaults for each are the following => FOCUS_THRESHOLD: {FOCUS_THRESHOLD} | DIRECTORY: {DIRECTORY} | EXT: {EXT}
"""

arguments = len(sys.argv)
position = 1
while position < arguments:
   if sys.argv[position] == '--focus' and isinstance(sys.argv[position] + 1, int):
      FOCUS_THRESHOLD = sys.argv[position] + 1
   elif sys.argv[position] == '--ext':
      EXT = sys.argv[position] + 1
   elif sys.argv[position] == '--dir':
      DIRECTORY = sys.argv[position] + 1
   elif sys.argv[position] == '--help':
      print(HELP_MESSAGE)
      exit()
   elif sys.argv[position] == '--h':
      print(HELP_MESSAGE)
      exit()
   elif sys.argv[position] and sys.argv[position] != re.match('$--', sys.argv[position]):
      print('\nERROR: INVALID ARGUMENT. See the --help information below.\n' + HELP_MESSAGE)
      exit()
   position = position + 1

print(f"PARAMETERS => FOCUS_THRESHOLD: {FOCUS_THRESHOLD} | DIRECTORY: '{DIRECTORY}' | EXT: {EXT}. For options, use '--help'")

BLURRED_DIR = 'blurred'
OK_DIR = 'ok'

blur_count = 0
files = [f for f in os.listdir(DIRECTORY) if f.endswith(EXT)]

try:
   os.makedirs(BLURRED_DIR)
   os.makedirs(OK_DIR)
except:
   pass

for infile in files:

   print('Processing file %s ...' % (infile))
   cv_image = cv2.imread(infile)

   # Covert to grayscale
   gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

   # Compute the Laplacian of the image and then the focus
   #     measure is simply the variance of the Laplacian
   variance_of_laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

   # If below threshold, it's blurry
   if variance_of_laplacian < FOCUS_THRESHOLD:
      shutil.move(infile, BLURRED_DIR)
      blur_count += 1
   else:
      shutil.move(infile, OK_DIR)

print('Done.  Processed %d files into %d blurred, and %d ok.' % (len(files), blur_count, len(files)-blur_count))