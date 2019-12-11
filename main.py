import os
from PIL import Image
from PIL import GifImagePlugin

def print_char_blocks():
    chars_img = Image.open('chars.png')
    chars_pix = chars_img.load()

    width, height = chars_img.size  # Get the width and hight of the image for iterating over

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
        char_img = Image.new('RGB', char_size, color = 'black')
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

def save_brightness(name, fileType):
    if fileType == "jpeg":
        img = Image.open(name + "." + fileType)
        pix = img.load()

        width, height = img.size  # Get the width and hight of the image for iterating over

        result = [] # becomes a 2d list holding all brightness values
        for x in range(width):
            result.append([])
            for y in range(height):
                r, g, b = pix[x, y]
                brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
                brightness = round(brightness*1000)/1000
                result[x].append(brightness)

        # print(result)
        result_file = open(name + ".txt", "w")
        string = str(result)
        string = string.replace("[", "{")
        string = string.replace("]", "}")
        result_file.write(string)
        result_file.close()
    elif fileType == "gif":
        imageObject = Image.open(name + "." + img)


# print_char_blocks()
save_brightness("dogs 1 - 226x85", "jpeg")
# save_brightness("dogs 1 - 226x85", "gif")