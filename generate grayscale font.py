from PIL import Image

char_size = 8 # all characters are 8x8 in default.png
char_count = 95 # there are 95 characters in ComputerCraft, but note the 64th character ` can't be used later on!
row_count = 6
chars_in_row_max = 16

def get_grayscale(char_val):
	brightness = round(char_val * 255 / (char_count - 1))
	return (brightness, brightness, brightness)

for row in range(row_count):
	offset = row * chars_in_row_max
	chars_in_row = chars_in_row_max if row < row_count - 1 else chars_in_row_max - 1
	char_img_dimensions = (char_size * chars_in_row, char_size)
	char_img = Image.new('RGB', char_img_dimensions, color = 'black')
	char_pix = char_img.load()

	for char_val in range(chars_in_row):
		for bx in range (char_size):
			for by in range (char_size):
				x = char_val * char_size + bx
				y = by
				char_pix[x, y] = get_grayscale(char_val + offset)

	char_img.save('fonts/grayscale/row ' + str(row + 1) + '.png')
