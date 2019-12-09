import os
from PIL import Image

os.mkdir('output-chars')

chars_img = Image.open('chars.png')
chars_pix = chars_img.load()

width, height = chars_img.size  # Get the width and hight of the image for iterating over

char_width = 18
char_height = 24
char_count = int((width) / char_width)
pixel_block_size = 3

chars_blocks = []

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

for char_num in range(char_count):
    char_size = (18, 24)
    char_img = Image.new('RGB', char_size, color = 'black')
    char_pix = char_img.load()
    char_colored_blocks = 0

    for x in range(int(char_width / pixel_block_size)):
        for y in range(int(char_height / pixel_block_size)):
            pixel_block_rgb = chars_pix[char_num * char_width + x * pixel_block_size, y * pixel_block_size]
            if pixel_block_rgb != (0, 0, 0):
                char_colored_blocks += 1
            for bx in range (pixel_block_size):
                for by in range (pixel_block_size):
                    char_pix[x * pixel_block_size + bx, y * pixel_block_size + by] = pixel_block_rgb
    
    char = chars[char_num]
    chars_blocks.append([char, char_colored_blocks])

    char_img.save('output-chars/' + ' ' + str(char_num) + '-' + str(char_colored_blocks) + '.png')


chars_blocks_sorted = chars_blocks.copy()
chars_blocks_sorted.sort(key = lambda x: x[1])

print("\nchars_blocks: ")
print(chars_blocks)
print("\nchars_blocks_sorted: ")
print(chars_blocks_sorted)