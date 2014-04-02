#!/usr/bin/python

import os, sys, getopt
from wand.image import Image

sizes = (
    ('xhdpi',1.0),
    ('hdpi',0.75),
    ('mdpi',0.5),
    ('ldpi',0.375)
)

def showHelp():
    print """Android Image Resizer: Automatically generate resized images

    Usage: air.py [-h] [-o <outputfile>] <inputfile>

    -h,--help           Show this information
    -o,--out            Set root output directory.  Files will be copied to
                        <root>/res/drawable-xxx.  Default is CWD
    inputfile           xhdpi image file to resize and copy to
                        appropriate locations.

    Input files should be appropriately sized 24-bit PNG images.  A 320x320
    image will be exactly a one-inch square.  Image dimensions MUST be a multiple
    of 8.  For reference:

    res/drawable-xhdpi  --> 1/1 (Source)
    res/drawable-hdpi   --> 3/4
    res/drawable-mdpi   --> 1/2
    res/drawable-ldpi   --> 3/8
    """

    sys.exit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'ho:',['help','out='])
    except getopt.GetoptError:
        showHelp()

    rootDir = os.path.curdir
    for opt, arg in opts:
        if opt in ('-h','--help'):
            showHelp()
        if opt in ('-o','--out'):
            rootDir = os.path.abspath(arg)
            if os.path.exists(rootDir) and not os.path.isdir(rootDir):
                sys.stderr.write('ERROR: %s exists and is not a directory!\n' % (rootDir,))
                sys.exit(-1)

    if len(args) != 1:
        showHelp()

    inputFile = os.path.abspath(args[0])
    filename = os.path.split(inputFile)[1]
    filename = filename.replace('-','_')

    if not os.path.isfile(inputFile):
        sys.stderr.write('ERROR: %s is not a file!\n' % (inputFile,))
        sys.exit(-1)

    # Check image properties
    with Image(filename=inputFile) as img:
        if not (img.width / 8).is_integer() or (img.height / 8).is_integer():
            sys.stderr.write('ERROR: One or both dimensions are NOT multiples of 8\n')
            sys.exit(-1)

    # Build output directory, if needed
    resDir = '%s/res/' % (rootDir,)
    if not os.path.exists(resDir):
        if not os.path.exists(rootDir):
            os.mkdir(rootDir)
        os.mkdir(resDir)

    with Image(filename=inputFile) as img:
        for suffix,factor in sizes:
            targetDir = '%s/res/drawable-%s' % (rootDir, suffix)
            if not os.path.exists(targetDir):
                os.mkdir(targetDir)
            targetFile = '%s/%s' % (targetDir, filename)
            with img.clone() as workingImg:
                workingImg.resize(int(img.width * factor), int(img.height * factor))
                workingImg.save(filename=targetFile)
            print os.path.abspath(targetFile)

if __name__ == '__main__':
    main(sys.argv[1:])
