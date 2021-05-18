# NOTICE
This is an old repo for a script that was only meant to be used once so I have no reason to update it.
If I were to reimplement it, instead of reading the entire image (which are huge, btw), I would have first started with an identity matrix, on which I would make all the desired transforms (rescale, rotation, etc...) and then I would pull only the required image data and mapped it.

# StarrySkies

Simple python script to generate random crops at a set resolution from a set of bigger images. Made for observatory and telescope photos.
By pulling random cropped images and downscaling these I can lazily make wallpapers for myself. AFAIK It doesn't handle non-integer downscaling factors because of personal preference, you're free to change that.

Requires: NumPy, glob, argparse, Pillow

A x64 Python install is recommended because of high memory requirements with large images.

Original images pulled from: https://www.spacetelescope.org/

Have fun. Any questions just do: StarrySkies.py -h.

This script is under the GPL-3.0 License.
