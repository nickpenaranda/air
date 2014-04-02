Android Image Resizer
---------------------

Super simple python script to quickly make resized versions and copy them to the correct locations.

Installation
------------

Requires python2.7, ImageMagick, MagickWand.

Usage
-----

See:

    ./air.py --help

Example:

    # Makes resized copies of my_icon.png in ./my_app/res/drawable-xyz/ic_launcher.png

    $ ./air.py -o my_app -n ic_launcher my_icon.png
    /home/nick/my_app/res/drawable-xhdpi/ic_launcher.png
    /home/nick/my_app/res/drawable-hdpi/ic_launcher.png
    /home/nick/my_app/res/drawable-mdpi/ic_launcher.png
    /home/nick/my_app/res/drawable-ldpi/ic_launcher.png


License
-------

MIT License.  For my own personal use, YMMV.

--np
