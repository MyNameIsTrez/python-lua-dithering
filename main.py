## IMPORTING ####################

import os
import sys
import time
from PIL import Image
import zlib
from copy import copy, deepcopy

import dithering

## EDITABLE VARIABLES ####################

compression = False

## FUNCTIONS ####################

def getPixels(name):
    infile = "input/" + name
    extension = name.split(".",1)[1] # get the extension after the "."

    if extension == "gif":
        try:
            im = Image.open(infile)
        except IOError:
            print("Cant load"), infile
            sys.exit(1)
        i = 0

        # sometimes helps, other times it does not, see the next comment
        # mypalette = im.getpalette()

        new_imgs = []

        try:
            while 1:
                # sometimes helps, other times it does not
                # im.putpalette(mypalette)

                new_im = Image.new("RGBA", im.size)
                new_im.paste(im)
                # new_im.save('police/'+str(i)+'.png')
                new_imgs.append(new_im)

                i += 1
                im.seek(im.tell() + 1)

        except EOFError:
            return new_imgs
    elif extension == "jpeg":
        return [Image.open(infile)]

def get_brightness(tup):
    brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
    if len(tup) == 4:
        return brightness * tup[3] / 255
    else:
        return 0

def media_convert_to_chars(fullname, imgs):
    prev_frame = [] # holds the actual brightness values
    frames = [] # holds the brightness values, but with -1 if the (x, y)'s brightness is the same as the last frame

    width, height = imgs[0].size  # Get the width and hight of the Image for iterating over

    for i in range(len(imgs)):
        img = imgs[i]
        pix = img.load()

        prev_frame.append([])
        frames.append([]) # becomes a 2d list holding all brightness values
        for x in range(width):
            prev_frame[i].append([])
            frames[i].append([])

            for y in range(height):
                brightness = get_brightness(pix[x, y])
                brightness = round(brightness * 100) / 100

                # if x == 15 and y == 23:
                #     print("brightness: ", brightness)
                prev_frame[i][x].append(brightness)
                
                if i > 0:
                    diff = brightness - prev_frame[i - 1][x][y]
                    frames[i][x].append(brightness if diff else -1)
                else:
                    frames[i][x].append(brightness)
                
                # if x == 15 and y == 23:
                #     print("prev_frame[i][x][y]:", prev_frame[i][x][y], "frames[i][x][y]:", frames[i][x][y])
    
    # get the initiallly drawn frame, that doesn't get drawn after each loop
    initial_frame = deepcopy(frames)[0]

    for x in range(width):
        for y in range(height):
            # set the first frame's position to -1 if the last frame is -1
            if frames[-1][x][y] == -1:
                frames[0][x][y] = -1

    name = fullname.split(".",1)[0] # get the name before the "."
    result_file = open("output/" + name + ".txt", "w")
    
    final_frames = { "initial_frame": initial_frame, "frames": frames }
    string = str(final_frames)

    string = string.replace(":", "=")
    string = string.replace("'", "")

    string = string.replace("[", "{")
    string = string.replace("]", "}")
    string = string.replace(" ", "")
    
    string = string.replace("0.0,", "0,")
    string = string.replace("1.0", "1")

    if compression:
        a = zlib.compress(string.encode("utf-8"))
        b = str(a)
        result_file.write(b)
    else:
        result_file.write(string)
    result_file.close()

## CODE EXECUTION ####################

# media_convert_to_chars("dogs 1 - 226x85", "jpeg")

# startTime = time.time()

# names = os.listdir("input")
# for name in names:
#     media_convert_to_chars(name, getPixels(name))

# precision = 10 ** 3
# elapsedTime = int((time.time() - startTime) * precision) / precision

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
# print(bcolors.OKGREEN + "Elapsed time:", bcolors.WARNING + str(elapsedTime) + " seconds." + bcolors.ENDC)