from PIL import Image
from PIL import ImageFilter
#from IPython.display import Image as JubImage
import numpy

# NOTE: last try before it somehow worked was pip3 install opencv-python
#
# Sorts pictures in current directory into two subdirs, blurred and ok
# Found original here: https://photo.stackexchange.com/questions/20432/is-there-photo-analysis-software-which-will-pre-sort-images-by-identifying-poten
# Modified for my own purposes.
#

# stock python libs
import os, shutil, re, sys
# additional libs
#import cv2
from pathlib import Path

# DEFAULTS
FOCUS_THRESHOLD = 20
DIRECTORY = Path.cwd()
EXT = '.JPG'

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
   if sys.argv[position] == '--focus':
      FOCUS_THRESHOLD = sys.argv[position + 1]
      if isinstance(int(FOCUS_THRESHOLD), int):
         FOCUS_THRESHOLD = int(FOCUS_THRESHOLD)
      else:
         print('ERROR: --focus parameter did not meet int requirements. See "--help" for options.')
         exit()
   elif sys.argv[position] == '--ext':
      EXT = sys.argv[position + 1]
   elif sys.argv[position] == '--dir':
      DIRECTORY = Path(sys.argv[position + 1])
   elif sys.argv[position] == '--help':
      print(HELP_MESSAGE)
      exit()
   elif sys.argv[position] == '--h':
      print(HELP_MESSAGE)
      exit()
   position = position + 1
   #elif sys.argv[position] and sys.argv[position] != re.match('^--', sys.argv[position]):
   #   print('\nERROR: INVALID ARGUMENT. See the --help information below.\n' + HELP_MESSAGE)
   #   exit()
   position = position + 1

print(f"PARAMETERS => FOCUS_THRESHOLD: {FOCUS_THRESHOLD} | DIRECTORY: '{DIRECTORY}' | EXT: {EXT}. For options, use '--help'")

BLURRED_DIR = 'blurred'
OK_DIR = 'ok'

blur_count = 0

print(str(Path.cwd()) + '\\' + str(DIRECTORY))
files = [f for f in os.listdir(DIRECTORY) if f.endswith(EXT)]

try:
   os.makedirs(BLURRED_DIR)
   os.makedirs(OK_DIR)
except:
   pass

next = 'y'
for infile in files:
    if next == 'n':
       exit()
    else:
        print(f'Processing file {infile}... {DIRECTORY}\{infile}')
        print(str(Path.cwd()) + '\\' + str(DIRECTORY) + '\\' + infile)
        image = Image.open(infile)
        print(infile)
        h1 = image.histogram()
        zero = 0
        not_zero = 0
        for i in h1:
           if i < 150:
              zero = zero + i
           else:
              not_zero = not_zero + i
        print(f'Original: {zero} zeros vs {not_zero} not_zeros, median: {numpy.median(h1)}')
        #arr1 = numpy.array(image)
        #print(image.getdata())
        imageWithEdges = image.filter(ImageFilter.FIND_EDGES)
        h2 = imageWithEdges.histogram()
        #print(h2)
        zero = 0
        not_zero = 0
        for i in h2:
           if i < 150:
              zero = zero + i
           else:
              not_zero = not_zero + i
        print(f'Filtered: {zero} zeros vs {not_zero} not_zeros, median: {numpy.median(h2)}')
        #image_file = image_file.convert('1')
        

        bw = imageWithEdges.convert('L')
        bw.show()

        black = 0
        white = 0

        for pixel in bw.getdata():
           #print(pixel)
           if pixel == (0): # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
              black += 1
           elif pixel == (255):
              white += 1
        print(f'Black: {str(black)} | White: {str(white)} | B/W Ratio: {str(white/black)}')
        #imageWithEdges.show()
        #arr2 = numpy.array(imageWithEdges)
        #diff = arr1 - arr2
        #new_image = Image.fromarray(diff)
        #new_image.show()
        #print(arr1)
        #print(arr2)
        next = input('y for next, n for stop: ')