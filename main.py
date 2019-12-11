## IMPORTING ####################

import os
import sys
import time
from PIL import Image
import zlib

## EDITABLE VARIABLES ####################

compression = False

## FUNCTIONS ####################

def print_char_blocks():
    chars_img = PILImage.open('chars.png')
    chars_pix = chars_img.load()

    width, height = chars_img.size  # Get the width and hight of the PILImage for iterating over

    char_width = 18
    char_height = 27
    char_count = int((width) / char_width)
    pixel_block_size = 3

    chars_blocks = []
    char_blocks_sorted_dict = {}

    chars = [
        ' ',
        '!',
        '"',
        '#',
        '$',
        '%',
        '&',
        "'",
        '(',
        ')',
        '*',
        '+',
        ',',
        '-',
        '.',
        '/',
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        ':',
        ';',
        '<',
        '=',
        '>',
        '?',
        '@',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        '[',
        '\\',
        ']',
        '^',
        '_',
        '?',
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z',
        '{',
        '|',
        '}',
        '~'
    ]

    for char_index in range(char_count):
        char_size = (18, 24)
        char_img = PILImage.new('RGB', char_size, color = 'black')
        char_pix = char_img.load()
        char_colored_blocks = 0

        for x in range(int(char_width / pixel_block_size)):
            for y in range(int(char_height / pixel_block_size)):
                pixel_block_rgb = chars_pix[char_index * char_width + x * pixel_block_size, y * pixel_block_size]
                if pixel_block_rgb != (0, 0, 0):
                    char_colored_blocks += 1
                for bx in range (pixel_block_size):
                    for by in range (pixel_block_size):
                        char_pix[x * pixel_block_size + bx, y * pixel_block_size + by] = pixel_block_rgb
        
        char = chars[char_index]
        chars_blocks.append([char, char_colored_blocks])

        if not char_colored_blocks in char_blocks_sorted_dict:
            char_blocks_sorted_dict[char_colored_blocks] = []
        char_blocks_sorted_dict[char_colored_blocks].append(char)

    char_blocks_sorted = chars_blocks.copy()
    char_blocks_sorted.sort(key = lambda x: x[1])

    print("\nchar_blocks_sorted: ")
    print(char_blocks_sorted)
    print("\nchar_blocks_sorted_dict: ")
    print(char_blocks_sorted_dict)

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

def get_brightness(tup, x, y):
    if x == 0 and y == 0:
        print(tup)

    brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
    if len(tup) == 4:
        return brightness * tup[3] / 255
    else:
        return 0

def save_brightness(fullname, imgs):
    prev_frame = []
    frames = []

    width, height = imgs[0].size  # Get the width and hight of the PILImage for iterating over
    print("width: " + str(width) + ", " + "height: " + str(height))

    print("len(imgs): " + str(len(imgs)))
    for i in range(len(imgs)):
        img = imgs[i]

        pix = img.load()

        frame = [] # becomes a 2d list holding all brightness values
        for x in range(width):
            frame.append([])
            for y in range(height):
                brightness = get_brightness(pix[x, y], x, y)
                # brightness = int(brightness > 0.5)
                brightness = round(brightness*100)/100
                if i > 0:
                    diff = brightness - prev_frame[x][y]
                    frame[x].append(brightness if diff else -1)
                else:
                    frame[x].append(brightness)
        prev_frame = frame
        frames.append(frame)
    
    name = fullname.split(".",1)[0] # get the name before the "."
    result_file = open("output/" + name + ".txt", "w")
    string = str(frames)

    string = string.replace("[", "{")
    string = string.replace("]", "}")
    string = string.replace(" ", "")
    string = string.replace("0.0", "0") # don't know why 0.0 even occurs
    string = string.replace("1.0", "1") # don't know why 1.0 even occurs

    if compression:
        a = zlib.compress(string.encode("utf-8"))
        b = str(a)
        result_file.write(b)
    else:
        result_file.write(string)
    result_file.close()

## CODE EXECUTION ####################

# print_char_blocks()
# save_brightness("dogs 1 - 226x85", "jpeg")

startTime = time.time()

names = os.listdir("input")
for name in names:
    save_brightness(name, getPixels(name))

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