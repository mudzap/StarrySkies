from PIL import Image
import argparse
import glob
import numpy
from numpy import random

Image.MAX_IMAGE_PIXELS = None

#Checks if image should be transposed
def shouldTranspose(outputSize, inputSize):
    
    #Get aspect ratios
    outputAspectRatio = outputSize[0]/outputSize[1]
    inputAspectRatio = inputSize[0]/inputSize[1]
    
    #Make aspect ratios integer
    outputAspectRatio = int(outputAspectRatio)
    inputAspectRatio = int(inputAspectRatio)
    
    #Check if one is vertical and the other one horizontal to see if you should transpose
    transposeFlag = False    
    if (inputAspectRatio != outputAspectRatio):
        transposeFlag = True
    
    return transposeFlag
    

#Gets scaling factor
def getScalingFactor(outputSize, inputSize):
    #Get scaling factor for x and y axes.
    scaleFactor = []
    for n in range(len(inputSize)):
        scaleFactor.append(inputSize[n]/outputSize[n])
    
    #Get minimum  scaling factor
    minimumFactor = min(scaleFactor)
    
    #Make scaling factor integer
    factor = int(minimumFactor)
    
    return factor
    

#Get max box
def getBoundingBoxCropRegion(factor, outputSize, inputSize):
    difference   = [inputSize[0] - factor*outputSize[0], inputSize[1] - factor*outputSize[1]]
    randomOffset = [random.randint(difference[0]), random.randint(difference[1])]
    boundingBox  = [randomOffset[0]                       , randomOffset[1],
                    factor*outputSize[0] + randomOffset[0], factor*outputSize[1] + randomOffset[1]]
    return boundingBox

#Argument handler
parser = argparse.ArgumentParser(description='Create random wallpapers from large images, made for nebulae')
parser.add_argument('dim', type=int, help='Horizontal and vertical resolution of output image', nargs=2)
parser.add_argument('n', type=int, help='Number of images per input image')
parser.add_argument('-i', metavar='input', help='Source image filename.', nargs='+', required=True)
parser.add_argument('-o', metavar='output', help='Output image filename. Defaults to oX.FORMAT', default='o')
parser.add_argument('-r', '--rotate90', type=int, choices=[-1,0,1], help='Rotates the original image before proccesing it, useful for going from aspect ratios less than 1 to bigger than 1 and viceversa. Defaults to Auto (-1).', default=-1)
parser.add_argument('-s', '--scaling', metavar='factor', type=int, help='Determines if the downscaling factor of the original image, if -1, then downscale it automatically.', default=-1)
parser.add_argument('-f', '--format', metavar='format', choices={'jpeg','png'}, help='Sets output format. Defaults to png', default='png')
group = parser.add_mutually_exclusive_group()
group.add_argument('-png-c', '--png-compression', metavar='level', type=int, help='Defines png compression level (1-9). Defaults to 6.', default=6)
group.add_argument('-jpeg-q', '--jpeg-quality', metavar='quality', type=int, help='Defines jpeg quality level (0-100). Defaults to 95.', default=95)
args = parser.parse_args()

#Build set of files to process
inputFiles = set()
for n in range(len(args.i)):
    inputFiles.update(glob.glob(args.i[n]))

#Process and save images
index = 0
for n in inputFiles:
    outfile = args.o + str(index) +  '.' + args.format
    index += 1
    if n != outfile:
        try:
            with Image.open(n) as image:
                #Image processing
                #Transpose image
                if  args.rotate90 == 1 or (args.rotate90 == -1 and shouldTranspose(args.dim, image.size)):
                    image = image.transpose(method=Image.ROTATE_90)
                
                #Get scaling factor
                downscaleFactor = 0
                if args.scaling == -1:
                    downscaleFactor = getScalingFactor(args.dim, image.size)
                else:
                    downscaleFactor = args.scaling
                
                #Crop image
                try:
                    boundingBox = getBoundingBoxCropRegion(downscaleFactor, args.dim, image.size)
                    image = image.crop(boundingBox)
                except:
                    print("Couldn't crop", n, ", skipping to next image (scaleFactor too big?)")
                    continue
                    
                #Downscale image
                if downscaleFactor > 0:
                    try:
                        newSize = [int(image.size[0]/downscaleFactor), int(image.size[1]/downscaleFactor)]
                        image = image.resize(newSize, resample=1)
                    except:
                        print("Couldn't downscale", n, ", skipping to next image")
                #Save File
                image.save(outfile, format=args.format, compression_level=args.png_compression, quality=args.jpeg_quality, icc_profile=image.info.get('icc_profile'))
        except IOError:
            print("Cannot convert ", n)
            
