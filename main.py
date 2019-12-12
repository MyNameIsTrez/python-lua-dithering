## IMPORTING ####################

import os
import sys
import time
from PIL import Image
from copy import copy, deepcopy

import dithering # should be placed in the same folder as this program

## EDITABLE VARIABLES ####################

## FUNCTIONS ####################

def getImagesArray(name):
    infile = "input/" + name
    extension = name.split(".",1)[1] # get the extension after the "."

    if extension == "gif":
        try:
            im = Image.open(infile)
        except IOError:
            print("Cant load"), infile
            sys.exit(1)

        # the next line possibly helps, but it breaks the output right now, see the next comment
        # mypalette = im.getpalette()

        new_imgs = []

        try:
            i = 0
            while 1:
                # the next line possibly helps, but it breaks the output right now
                # im.putpalette(mypalette)

                new_im = Image.new("RGBA", im.size)
                new_im.paste(im)
                new_imgs.append(new_im)

                i += 1
                im.seek(im.tell() + 1) # not sure what this does

        except EOFError:
            return new_imgs # return array
    elif extension == "jpeg":
        return [Image.open(infile)] # return the image output in an array

def get_brightness(tup):
    # not all rgb colors are equally bright. multipliers gotten from a stackoverflow comment.
    brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
    if len(tup) == 4:
        return brightness * tup[3] / 255
    else:
        return 0

def media_convert_to_chars(fullname, imgs):
    real_frames = [] # holds the actual brightness values
    optimized_frames = [] # holds the brightness values, but with "t" if the (x, y)'s brightness is the same as the last frame

    width, height = imgs[0].size

    frameCount = len(imgs)
    for f in range(frameCount):
        img = imgs[f]
        pix = img.load()

        real_frames.append([])
        optimized_frames.append([])
        for x in range(width):
            real_frames[f].append([])
            optimized_frames[f].append([])

            for y in range(height):
                brightness = get_brightness(pix[x, y])
                brightness = round(brightness * 100) / 100

                real_frames[f][x].append(brightness)
                
                if f > 0:
                    # save the brightness if it isn't equal to the brightness of the last frame, else save "t" to indicate it shouldn't draw here
                    diff = brightness - real_frames[f - 1][x][y]
                    if diff:
                        char = dithering.getClosestChar(brightness)
                    else:
                        char = "t" # signifies repetition of a previous frame's character; this character should never get drawn
                    optimized_frames[f][x].append(char)
                else:
                    char = dithering.getClosestChar(brightness)
                    optimized_frames[f][x].append(char) # necessary to create initial_frame, and for the 2nd frame
    
    # get the initiallly drawn frame, that doesn't get drawn after each loop
    initial_frame = deepcopy(optimized_frames)[0]

    # I SUSPECT THIS CODE CAUSES THE LAST FRAME TO NOT BE CLEARED COMPLETELY FOR SOME REASON!!!
    for x in range(width):
        for y in range(height):
            # sets the first frame character position to "t", if the last frame's equal character position is the same character
            if real_frames[-1][x][y] == real_frames[0][x][y]:
                real_frames[0][x][y] = "t" # signifies repetition of a previous frame's character; this character should never get drawn

    saveString(fullname, width, height, initial_frame, optimized_frames, frameCount)

def saveString(fullname, width, height, initial_frame, optimized_frames, frameCount):
    name = fullname.split(".",1)[0] # get the name before the "."
    result_file = open("output/" + name + ".txt", "w")
    
    initial_frame_list = []
    # add all strings in initial_frame to stringList
    for x in range(width):
        for y in range(height):
            s = initial_frame[x][y]
            initial_frame_list.append(s)
    
    optimized_frames_list = []
    # add all strings in optimized_frames to stringList
    for f in range(frameCount):
        for x in range(width):
            for y in range(height):
                s = optimized_frames[f][x][y]
                optimized_frames_list.append(s)
    
    string_initial_frame = "".join(initial_frame_list)
    string_optimized_frames = "".join(optimized_frames_list)

    data = {
        "width": width,
        "height": height,
        "frame_count": frameCount,
        "initial_frame": string_initial_frame,
        "optimized_frames": string_optimized_frames
    }

    string = str(data)

    string = string.replace("'width': ", "width=")
    string = string.replace(", 'height': ", ",height=")
    string = string.replace(", 'frame_count': ", ",frame_count=")
    string = string.replace(", 'initial_frame': ", ",initial_frame=")
    string = string.replace(", 'optimized_frames': ", ",optimized_frames=")
    
    result_file.write(string)

    result_file.close()

## CODE EXECUTION ####################

startTime = time.time()

names = os.listdir("input")
for name in names:
    media_convert_to_chars(name, getImagesArray(name))

precision = 10 ** 3
elapsedTime = int((time.time() - startTime) * precision) / precision

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
print(bcolors.OKGREEN + "Elapsed time:", bcolors.WARNING + str(elapsedTime) + " seconds." + bcolors.ENDC)