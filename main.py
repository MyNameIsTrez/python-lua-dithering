import os
import time
import sys
from math import floor
import cv2
from PIL import Image

sys.path.append('libs/')
import dithering

# from python-lua-dithering.libs import dithering
# import libs.dithering
# from libs.dithering import *


# FUNCTIONS #######################################


def process_frames(full_file_name, max_width, max_height, frame_skipping):
	extension = full_file_name.split('.')[1]  # get the extension after the '.'
	# get the name before the '.', and optionally add '_extended'
	file_name = full_file_name.split('.')[0] + (' extended' if extended_chars else '')
	input_path = 'inputs/' + full_file_name
	output_file_name = file_name.replace(' ', '_')

	print('Processing \'' + file_name + '\'')

	if extension == 'mp4':
		video = cv2.VideoCapture(input_path)
		old_image = None
	else:
		video = None
		old_image = Image.open(input_path)

	new_height = max_height
	new_width = get_new_width(extension, video, old_image, input_path, new_height, max_width)

	output_folder_size_name = 'outputs/' + 'size_' + str(new_width) + 'x' + str(new_height)
	if not os.path.exists(output_folder_size_name):
		os.mkdir(output_folder_size_name)

	output_folder_name = output_folder_size_name + '/' + output_file_name
	if not os.path.exists(output_folder_name):
		os.mkdir(output_folder_name)

	output_data_folder_name = output_folder_name + '/data'
	if not os.path.exists(output_data_folder_name):
		os.mkdir(output_data_folder_name)

	if extension == 'mp4':
		used_frame_count, data_frames_count = process_mp4_frames(output_data_folder_name, video, frame_skipping, new_width, new_height)
	elif extension == 'gif':
		used_frame_count, data_frames_count = process_gif_frames(output_data_folder_name, old_image, new_width, new_height)
	elif extension == 'jpeg' or extension == 'png' or extension == 'jpg':
		used_frame_count, data_frames_count = process_image_frame(output_data_folder_name, old_image, new_width, new_height)
	else:
		print('Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!')

	output_info_file = create_output_file(output_folder_name, 'info')
	string = '{frame_count=' + str(used_frame_count) + ',width=' + str(new_width) + ',height=' + str(new_height) + ',data_files=' + str(data_frames_count) + '}'
	output_info_file.write(string)
	output_info_file.close()


def get_new_width(extension, video, old_image, input_path, new_height, max_width):
	if extension == 'mp4':
		# get information about the video file
		old_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
		old_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
	elif extension == 'gif' or extension == 'jpeg' or extension == 'png' or extension == 'jpg':
		try:
			old_width = old_image.size[0]
			old_height = old_image.size[1]
		except IOError:
			print('Can\'t load!')
	else:
		print('Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!')

	if new_width_stretched:
		return max_width
	else:
		return int(new_height * old_width / old_height)


def create_output_file(folder, name):
	output_path = folder + '/' + str(name) + '.txt'
	return open(output_path, 'w')


def try_create_new_output_file(line_num, file_byte_count, output_file, output_data_folder_name, data_frames_count):
	line_num += 1

	if file_byte_count >= max_bytes_per_file:
		file_byte_count = 0

		if output_file:
			output_file.close()

		output_file = create_output_file(output_data_folder_name, data_frames_count)

		data_frames_count += 1

		line_num = 1
	
	return line_num, file_byte_count, output_file, data_frames_count


def process_mp4_frames(output_data_folder_name, video, frame_skipping, new_width, new_height):
	i = 0
	used_frame_count = 0

	actual_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	new_frame_count = floor(actual_frame_count / frame_skipping)

	file_byte_count = 0
	output_file = create_output_file(output_data_folder_name, 1)
	data_frames_count = 2
	line_num = 0

	while True:
		start_frame_time = time.time()

		hasFrames, cv2_frame = video.read()

		if hasFrames:
			if i % frame_skipping == 0:
				used_frame_count += 1

				line_num, file_byte_count, output_file, data_frames_count = try_create_new_output_file(line_num, file_byte_count, output_file, output_data_folder_name, data_frames_count)
				
				# cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)

				cv2_frame = cv2.resize(cv2_frame, (new_width, new_height))

				pil_frame = Image.fromarray(cv2_frame)  # pil pixels can be read faster than cv2 pixels, it seems

				get_frame_time = time.time() - start_frame_time  # 40 frames/s

				file_byte_count += process_frame(pil_frame, used_frame_count, line_num, new_width, new_height, output_file, new_frame_count, start_frame_time, get_frame_time)
			i += 1
		else:
			video.release()
			output_file.close()

			return used_frame_count, data_frames_count - 1


def process_gif_frames(output_data_folder_name, old_image, new_width, new_height):
	i = 0
	used_frame_count = 0

	file_byte_count = 0
	output_file = create_output_file(output_data_folder_name, 1)
	data_frames_count = 2
	line_num = 0

	try:
		while True:
			start_frame_time = time.time()

			if i % frame_skipping == 0:
				used_frame_count += 1

				line_num, file_byte_count, output_file, data_frames_count = try_create_new_output_file(line_num, file_byte_count, output_file, output_data_folder_name, data_frames_count)
				
				new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)

				get_frame_time = time.time() - start_frame_time

				file_byte_count += process_frame(new_image, used_frame_count, line_num, new_width, new_height, output_file, None, start_frame_time, get_frame_time)

				old_image.seek(old_image.tell() + 1)  # gets the next frame
			i += 1
	except:
		# this part gets reached when the code tries to find the next frame, while it doesn't exist
		output_file.close()

		return used_frame_count, data_frames_count - 1


def process_image_frame(output_data_folder_name, old_image, new_width, new_height):
	data_frames_count = 1
	line_num = 0

	output_file = create_output_file(output_data_folder_name, 1)

	start_frame_time = time.time()

	new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
	# new_image = old_image.resize((new_width, new_height), Image.NEAREST)
	# new_image = old_image.resize((new_width, new_height), Image.BILINEAR)
	# new_image = old_image.resize((new_width, new_height), Image.BICUBIC)
	
	# new_image = new_image.convert('RGB')

	used_frame_count = 1

	get_frame_time = time.time() - start_frame_time

	process_frame(new_image, used_frame_count, line_num, new_width, new_height, output_file, 1, start_frame_time, get_frame_time)

	output_file.close()
	
	return used_frame_count, data_frames_count


def process_frame(frame, used_frame_count, line_num, new_width, new_height, output_file, frame_count, start_frame_time, get_frame_time):
	preparing_loop_start_time = time.time()

	# not sure if it is necessary to convert the frame into RGBA!
	frame = frame.convert('RGBA')
	# load the pixels of the frame
	frame_pixels = frame.load()

	# initializes empty variables for the coming 'for y, for x' loop
	prev_char = None
	prev_char_count = 0
	string = ''

	# the \n character at the end of every line needs to have one spot reserved
	# this should ideally be done at the resizing of the frame stage instead!
	modified_width = new_width - 1

	preparing_loop_end_time = time.time()

	# measure the time it takes for the coming 'for y, for x' loop to execute
	looping_start_time = time.time()

	for y in range(new_height):
		for x in range(modified_width):
			# the brightness of a pixel determines which character will be used in ComputerCraft for that pixel
			brightness = get_brightness(frame_pixels[x, y])
			if not extended_chars:
				char = dithering.get_closest_char_default(brightness)
			else:
				char = dithering.get_closest_char_extended(brightness)
			string += char

		# the last character in a frame doesn't need a return character after it
		if y < new_height - 1:
			# add a return character to the end of each horizontal line,
			# so ComputerCraft can draw the entire frame with one write() statement
			string += '\\n'

	looping_end_time = time.time()

	writing_start_time = time.time()

	# gives each frame its own line in the outputted file, so lines can easily be found and parsed
	if line_num > 1:
		final_string = '\n' + string
	else:
		final_string = string

	output_file.write(final_string)

	writing_end_time = time.time()

	preparing_loop_time = preparing_loop_end_time - preparing_loop_start_time
	looping_time = looping_end_time - looping_start_time
	writing_time = writing_end_time - writing_start_time

	if used_frame_count % frames_to_update_stats == 0 or used_frame_count == frame_count:
		print_stats(used_frame_count, frame_count, start_frame_time, get_frame_time, preparing_loop_time, looping_time, writing_time)
		
		if used_frame_count == frame_count:	
			print()

	string_byte_count = len(final_string.encode('utf8'))

	return string_byte_count


def get_brightness(tup):
	# red, green and blue values aren't equally bright to the human eye
	brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
	if len(tup) == 4:
		return brightness * tup[3] / 255
	else:
		return 0


def print_stats(used_frame_count, frame_count, start_frame_time, get_frame_time, preparing_loop_time, looping_time, writing_time):
	# progress
	progress = 'Frame ' + str(used_frame_count) + '/'
	if frame_count:
		progress = progress + str(frame_count)
	else:
		progress = progress + '?'

	# speed of processing the frame
	elapsed = time.time() - start_frame_time
	if elapsed > 0:
		processed_fps = floor(1 / elapsed)
	else:
		processed_fps = '1000+'
	speed = ', speed: {} frames/s'.format(processed_fps)

	# speed of getting the frame
	if get_frame_time > 0:
		processed_fps = floor(1 / get_frame_time)
	else:
		processed_fps = '1000+'
	speed_2 = ', get frame: {} frames/s'.format(processed_fps)

	# preparing for the 'for y, for x' loop
	if preparing_loop_time > 0:
		processed_fps = floor(1 / preparing_loop_time)
	else:
		processed_fps = '1000+'
	speed_3 = ', preparing loop: {} frames/s'.format(processed_fps)

	# speed of the 'for y, for x' loop
	if looping_time > 0:
		processed_fps = floor(1 / looping_time)
	else:
		processed_fps = '1000+'
	speed_4 = ', pixel loop: {} frames/s'.format(processed_fps)

	# writing speed
	if writing_time > 0:
		processed_fps = floor(1 / writing_time)
	else:
		processed_fps = '1000+'
	speed_5 = ', writing: {} frames/s'.format(processed_fps)

	# calculate how long it should take for the program to finish
	if frame_count:
		frames_left = frame_count - used_frame_count
		seconds_left = elapsed * frames_left

		eta_hours = floor(seconds_left / 3600)
		eta_minutes = floor(seconds_left / 60) % 60
		eta_seconds = floor(seconds_left) % 60

		# makes sure each value is always 2 characters wide when printed
		if eta_hours < 10:
			eta_hours = '0' + str(eta_hours)
		if eta_minutes < 10:
			eta_minutes = '0' + str(eta_minutes)
		if eta_seconds < 10:
			eta_seconds = '0' + str(eta_seconds)

		eta = ', {}:{}:{} left'.format(eta_hours, eta_minutes, eta_seconds)
	else:
		eta = ', ? left'

	# clears the line that will be printed on of any straggling characters
	tab = '    '

	print(tab + progress + speed + eta, end='\r', flush=True)

	# sys.stdout.write("\033[F") # Cursor up one line
	# sys.stdout.write("\033[K") # Clear to the end of line

	# print(tab + progress + speed + eta, end='\r', flush=True)
	# print(tab + progress + speed + speed_2 + speed_3 + speed_4 + speed_5 + eta, end='\r', flush=True)


# USER SETTINGS #######################################


# default is False
# if true, the program assumes 94 characters are available, instead of the usual 20
# 94 are available by replacing Tekkit's default characters in default.png, see the instructions below
extended_chars = False

# how to get the extended character set (characters are replaced with grayscale blocks):
# 1. go to %appdata%/.technic/modpacks/tekkit/bin
# 2. remove the minecraft.jar file and replace it with 'minecraft.jar versions/new/minecraft.jar',
#    which can be found inside the same folder of this program
# 3. tekkit's characters should now all be replaced with 94 grayscale colors, instead of the default 19
# 4. when you want to go back to the default font,
# 	 replace the new minecraft.jar file with 'minecraft.jar versions/old/minecraft.jar'

# if true, the original aspect ratio won't be kept so the width can be stretched to max_width 
new_width_stretched = True

# normally, files that have been put in the 'inputs' folder will be moved to 'temp inputs' once they've been processed
# they'll remain in the 'inputs' folder after being processed when this is set to False
move_processed_files = False

# a file compression method
# 1 means every frame of the video is kept, 3 means every third frame of the video is kept
frame_skipping = 1

# 100 MB GitHub file limit. 9.5e7 is 95 million.
max_bytes_per_file = 9.5e7

# how many frames have to be processed before the stats in the console are updated
frames_to_update_stats = 100


# this determines the width and height of the output frames
# see tekkit/config/mod_ComputerCraft.cfg to set your own max_width and max_height values

# (max_width, max_height)
output_dimensions = (
	# (30, 30),
	# (77, 31), # max 8x5 monitor size in ComputerCraft, used because 8x6 doesn't always work
	# (77, 38), # max 8x6 monitor size in ComputerCraft
	# (227, 85), # 1080p
	(426, 160), # 1440p
	(640, 240), # 4k
)


# EXECUTION OF THE PROGRAM #######################################


print()

t0 = time.time()

for dimension in output_dimensions:
	max_width, max_height = dimension

	# get all filenames that will be processed
	names = os.listdir('inputs')
	for name in names:
		if name != '.empty': # '.empty' prevents the folder from being removed on GitHub
			process_frames(name, max_width, max_height, frame_skipping)
			# moving file to the temp inputs folder so it doesn't get processed again the next time
			if move_processed_files:
				os.rename('inputs/' + name, 'temp inputs/' + name)
	
	print()

# print the time it took to run the program
time_elapsed = time.time() - t0
minutes = floor(time_elapsed / 60)
seconds = time_elapsed % 60

print('Done! Duration: {}m, {:.2f}s'.format(minutes, seconds))

# sys.stdout.write("\033[F") # Cursor up one line
# sys.stdout.write("\033[K") # Clear to the end of line
# print('Done! Duration: {}m, {:.2f}s'.format(minutes, seconds), end='\r', flush=True)