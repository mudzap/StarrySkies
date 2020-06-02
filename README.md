# StarrySkies
By: Iván Peña, Universidad Anáhuac

Simple python script to generate random crops at a set resolution from a set of bigger images. Made for observatory and telescope photos.
By pulling random cropped images and downscaling these I can lazily make wallpapers for myself. AFAIK It doesn't handle non-integer downscaling factors because of personal preference, you're free to change that.

Requires: NumPy, glob, argparse, Pillow

TODO:
- Make several crops in a single pass, this will be done with the currently redundant argument N.
- Fix output naming for when any exception occurs.
- Adequate the script for proper output naming.

A x64 Python install is recommended because of high memory requirements with large images.

Original images pulled from: https://www.spacetelescope.org/

Have fun. Any questions just do: StarrySkies.py -h.

This script is under the GPL-3.0 License.
