from PIL import Image

char_size = 8 # all characters are 8x8 in chars.png (default.png)
row_count = 16
chars_in_row = 16

chars_img = Image.open('chars split/chars.png')
chars_pix = chars_img.load()

for row in range(row_count):
	y_offset = row * char_size
	
	for col in range(chars_in_row):
		# char_img = Image.new('RGB', char_img_dimensions, color = 'black')
		char_img = Image.new('RGBA', (char_size, char_size))
		char_pix = char_img.load()
		x_offset = col * char_size

		for y1 in range(char_size):
			for x1 in range(char_size):
				x2 = x1 + x_offset
				y2 = y1 + y_offset
				char_pix[x1, y1] = chars_pix[x2, y2]
		
		char_img.save('chars split/chars/char_' + str(col + row * chars_in_row) + '.png')