#!/usr/bin/python

import os, sys, getopt
from wand.image import Image

SIZES = (
    ('xhdpi',1.0),
    ('hdpi',0.75),
    ('mdpi',0.5),
    ('ldpi',0.375)
)

DEFAULT_EXT = '.png'
REF_DPI = 320.0

def showHelp():
    print """Android Image Resizer: Automatically generate resized images

Usage: air.py [-hq] [-o <output_root>] [-n <filename>[.<ext>]]
              [-d <dpi>|--hsize=<x>|--vsize=<y>] <inputfile>


-h,--help           Show this information

-d <d>,--dpi=<d>    Pixel density of source image.  Default is 320dpi.
                    NOTE: dpi, hsize and vsize are mutually exclusive.

-n <x>,--name=<x>   Save resized files with this filename.  Extension optional.
                    ***NOTE***: If you DO provide an extension, this will also
                    change the FORMAT of the output file.

-o <x>,--out=<x>    Set root output directory.  Files will be copied to
                    <x>/res/drawable-xyz.  Default is CWD

-q,--quiet          Suppress output

--hsize=<h>,        Width or height, in inches, of the source image.  Default
--vsize=<v>         assumes source image is 320dpi. NOTE: dpi, hsize and vsize
                    are mutually exclusive.

inputfile           xhdpi image file to resize and copy to
                    appropriate locations.

    Input files should be appropriately sized 24-bit PNG images.  Unless
--hsize or --vsize are specified, a 320x320 image will be a one-inch
square.
"""

    sys.exit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,
                'd:hn:o:q',
                ['dpi=','help','name=','out=','quiet','hsize=','vsize='])
    except getopt.GetoptError:
        showHelp()

    if len(args) != 1:
        showHelp()

    # Defaults
    quietMode = False
    rootDir = os.path.curdir
    inputFile = os.path.abspath(args[0])
    filename = os.path.basename(inputFile).replace('-','_')
    ext = os.path.splitext(filename)[1]
    correction = 1.0
    sWidth = sHeight = sDPI = None

    for opt, arg in opts:
        if opt in ('-h','--help'):
            showHelp()
        elif opt in ('-o','--out'):
            rootDir = os.path.abspath(arg)
            if os.path.exists(rootDir) and not os.path.isdir(rootDir):
                sys.stderr.write('ERROR: %s exists and is not a directory!\n' % (rootDir,))
                sys.exit(-1)
        elif opt in ('-n','--name'):
            filename = arg.replace('-','_')
            if not os.path.splitext(filename)[1]:
                filename = filename + DEFAULT_EXT
        elif opt in ('-q','--quiet'):
            quietMode = True
        elif opt in ('-d','--dpi'):
            if sHeight or sWidth:
                sys.stderr.write('ERROR: Can only specify one of dpi, hsize or vsize!\n')
            try:
                sDPI = int(arg)
            except ValueError:
                sys.stderr.write('ERROR: DPI must be a positive integer!\n')
                sys.exit(-1)
        elif opt == '--hsize':
            if sHeight or sDPI:
                sys.stderr.write('ERROR: Can only specify one of dpi, hsize or vsize!\n')
                sys.exit(-1)
            try:
                sWidth = float(arg)
            except ValueError:
                sys.stderr.write('ERROR: Width must be a positive decimal number\n')
                sys.exit(-1)
        elif opt == '--vsize':
            if sWidth or sDPI:
                sys.stderr.write('ERROR: Can only specify one of dpi, hsize or vsize!\n')
                sys.exit(-1)
            try:
                sHeight = float(arg)
            except ValueError:
                sys.stderr.write('ERROR: Height must be a positive decimal number\n')
                sys.exit(-1)
        else:
            showHelp()

    if not os.path.isfile(inputFile):
        sys.stderr.write('ERROR: %s is not a file!\n' % (inputFile,))
        sys.exit(-1)

    # Check image properties
    with Image(filename=inputFile) as img:
        if not (img.width / 8.0).is_integer() or not (img.height / 8.0).is_integer():
            sys.stderr.write('ERROR: One or both dimensions are NOT multiples of 8\n')
            sys.exit(-1)

        # Adjust factors if source image width or height is specified
        if sDPI:
            correction = REF_DPI / sDPI
        elif sWidth:
            correction = sWidth * REF_DPI / img.width
        elif sHeight:
            correction = sHeight * REF_DPI / img.height

    # Build output directory, if needed
    resDir = '%s/res/' % (rootDir,)
    if not os.path.exists(resDir):
        if not os.path.exists(rootDir):
            os.mkdir(rootDir)
        os.mkdir(resDir)

    with Image(filename=inputFile) as img:
        for suffix,factor in SIZES:
            targetDir = '%s/res/drawable-%s' % (rootDir, suffix)
            if not os.path.exists(targetDir):
                os.mkdir(targetDir)
            targetFile = '%s/%s' % (targetDir, filename)
            realFactor = factor * correction
            with img.clone() as workingImg:
                workingImg.resize(int(img.width * realFactor), int(img.height * realFactor))
                workingImg.save(filename=targetFile)
            if not quietMode:
                print os.path.abspath(targetFile)

if __name__ == '__main__':
    main(sys.argv[1:])
