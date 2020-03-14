from PIL import Image

char_size = 8 # all characters are 8x8 in default.png
char_count = 95 # there are 95 characters in ComputerCraft, but note the 64th character ` can't be used later on!
row_count = 6
chars_in_row_max = 16

colors = [
	"#2c1522", "#201942", "#142730", "#4f1b27", "#3d1e63", "#50224a", "#25391e", "#38238c", "#473521", "#68231f",
	"#3c3e57", "#7f2054", "#2b5453", "#732e8e", "#5533c5", "#375e1b", "#704d50", "#2a613e", "#9e3021", "#5f581d",
	"#824923", "#3a5991", "#6f5182", "#5054a9", "#a33e4a", "#43657e", "#a228ac", "#c02449", "#b33984", "#9e5476",
	"#5b7258", "#af46a9", "#c24b18", "#6b60e3", "#a541e2", "#897055", "#a66b26", "#e13629", "#658228", "#3d8755",
	"#a263a4", "#e03876", "#3e8f2b", "#867b96", "#ea3e58", "#e439aa", "#a668d6", "#488f95", "#95852c", "#6a81e5",
	"#dd4de0", "#e16a53", "#e26599", "#b7838b", "#5895d3", "#ee6c29", "#cd836b", "#9b9864", "#e27a86", "#4db16e",
	"#dd8c4f", "#e578d6", "#8ba696", "#e08d24", "#83ac73", "#48b838", "#92af50", "#a89fd6", "#c294e5", "#8ab725",
	"#56ba9d", "#afae2c", "#72c15b", "#e49ac9", "#daad43", "#95bad7", "#d8af77", "#5bc7dc", "#d8b9a5", "#dac1d8",
	"#55e64d", "#eeca29", "#56e79d", "#8ee93e", "#73eb7b", "#59ebd3", "#dedc81", "#a8e89e", "#e1de56", "#bee841",
	"#b9e86b", "#d6deab", "#b3e4d5", "#e1ec2c"
]

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

	char_img.save('fonts/color/row ' + str(row + 1) + '.png')
