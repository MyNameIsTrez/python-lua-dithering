import os
import time
from math import floor
import cv2
from PIL import Image
import dithering


def process_frames(full_file_name, computer_type):
	extension = full_file_name.split('.', 1)[1]  # get the extension after the '.'
	file_name = full_file_name.split('.', 1)[0]  # get the name before the '.'
	input_path = 'inputs/' + full_file_name
	output_path = computer_type + ' outputs/' + file_name

	with open(output_path, 'w') as output_file:
		print('Processing \'' + file_name + '\'')

		if extension == 'mp4':
			# get information about the video file
			video = cv2.VideoCapture(input_path)
			old_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
			old_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
		elif extension == 'gif' or extension == 'jpeg' or extension == 'png' or extension == 'jpg':
			try:
				old_image = Image.open(input_path)
				old_width = old_image.size[0]
				old_height = old_image.size[1]
			except IOError:
				print('Can\'t load \'' + file_name + '\'!')
		else:
			print('Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!')

		new_height = max_height
		if new_width_stretched:
			new_width = max_width
		else:
			new_width = int(new_height * old_width / old_height)

		i = 0
		used_frame_count = 0
		if extension == 'mp4':
			# inaccurate, but fast
			actual_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
			frame_count = floor(actual_frame_count / frame_skipping)

			while True:
				start_frame_time = time.time()

				hasFrames, cv2_frame = video.read()
				if hasFrames:
					if i % frame_skipping == 0:
						cv2_frame = cv2.cvtColor(
							cv2_frame, cv2.COLOR_BGR2RGB)  # is this necessary?
						pil_frame = Image.fromarray(cv2_frame)
						pil_frame = pil_frame.convert('RGBA')

						used_frame_count += 1

						# resize the image to the desired width and height
						pil_frame = pil_frame.resize((new_width, new_height), Image.ANTIALIAS)

						process_frame(pil_frame, used_frame_count, new_width,
						              new_height, output_file, frame_count, start_frame_time)
					i += 1
				else:
					video.release()
					break
		elif extension == 'gif':
			# mypalette = old_image.getpalette() # possibly helps
			try:
				while True:
					start_frame_time = time.time()

					if i % frame_skipping == 0:
						# old_image.putpalette(mypalette) # possibly helps
						new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)

						used_frame_count += 1

						process_frame(new_image, used_frame_count, new_width,
						              new_height, output_file, None, start_frame_time)
						old_image.seek(old_image.tell() + 1)  # gets the next frame
					i += 1
			except:
				frame_count = i  # continue
		elif extension == 'jpeg' or extension == 'png' or extension == 'jpg':
			start_frame_time = time.time()

			new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
			# new_image = new_image.convert('RGB')

			used_frame_count += 1

			process_frame(new_image, used_frame_count,
			              new_width, new_height, output_file, 1, start_frame_time)
		else:
			print('Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!')

		# prepare output file for writing data
		compressed_output_str = 'true' if compressed_output else 'false'
		string = '\nframe_count=' + str(used_frame_count) + ',width=' + str(
			new_width) + ',height=' + str(new_height) + ',compressed=' + compressed_output_str + ','
		output_file.write(string)
		print()

		output_file.close()
		renamed_output_path = output_path + \
			' [' + str(used_frame_count) + ']' + '.txt'
		os.rename(output_path, renamed_output_path)


def process_frame(frame, used_frame_count, new_width, new_height, output_file, frame_count, start_frame_time):
	frame = frame.convert('RGBA')
	frame_pixels = frame.load()

	prev_char = None
	prev_char_count = 0
	string = ''

	modified_width = new_width - 1

	looping_start_time = time.time()

	for y in range(new_height):
		for x in range(modified_width):
			brightness = get_brightness(frame_pixels[x, y])
			char = dithering.getClosestChar(brightness)

			if compressed_output:
				final_line_char = (x == modified_width - 1)

				final_frame_char = (y == new_height - 1 and x == new_width - 1 - 0)

				if char == prev_char and not final_frame_char and not final_line_char:
					prev_char_count += 1
				else:
					# if the final char is equal to the previous char
					if (final_frame_char or final_line_char) and char == prev_char:
						prev_char_count += 1

					# add the previous chars
					if prev_char_count > 5:
						string += '[' + str(prev_char_count) + ';' + prev_char + ']'
					else:
						string += str(prev_char) * prev_char_count

					# if the final char isn't equal to the previous char
					if (final_frame_char or final_line_char) and char != prev_char:
						# concatenate the final char
						string += char

					if not final_line_char:
						prev_char_count = 1
					else:
						prev_char_count = 0

					prev_char = char
			else:
				string += char

		if y < new_height - 1:
			string += '\\n'

	looping_end_time = time.time()

	# gives each frame its own line in the outputted file, so lines can easily be found and parsed
	if used_frame_count > 1:
		final_string = '\n' + string
	else:
		final_string = string

	output_file.write(final_string)

	# progress
	progress = 'Frame ' + str(used_frame_count) + '/'
	if frame_count:
		progress = progress + str(frame_count)
	else:
		progress = progress + '?'

	# speed
	elapsed = time.time() - start_frame_time
	if elapsed > 0:
		processed_fps = floor(1 / elapsed)
	else:
		processed_fps = '1000+'
	speed = '{} frames/s'.format(processed_fps)

	# speed 2
	elapsed_2 = looping_end_time - looping_start_time
	if elapsed_2 > 0:
		processed_fps = floor(1 / elapsed_2)
	else:
		processed_fps = '1000+'
	speed_2 = '{} frames/s'.format(processed_fps)

	# eta
	if frame_count:
		frames_left = frame_count - used_frame_count
		seconds_left = elapsed * frames_left

		eta_hours = floor(seconds_left / 3600)
		eta_minutes = floor(seconds_left / 60) % 60
		eta_seconds = floor(seconds_left) % 60

		# Makes sure each value is always 2 characters wide when printed.
		if eta_hours < 10:
			eta_hours = '0' + str(eta_hours)
		if eta_minutes < 10:
			eta_minutes = '0' + str(eta_minutes)
		if eta_seconds < 10:
			eta_seconds = '0' + str(eta_seconds)

		eta = '{}:{}:{} left'.format(eta_hours, eta_minutes, eta_seconds)
	else:
		eta = '? left'

	clear = '		'

	print('    ' + progress + ', total speed: ' + speed + ', pixel loop speed: ' + speed_2 +
	      ', ' + eta + clear, end='\r', flush=True)


def get_brightness(tup):
	# red, green and blue values aren't equally bright to the human eye
	brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
	if len(tup) == 4:
		return brightness * tup[3] / 255
	else:
		return 0


t0 = time.time()

# user settings
computer_type = 'desktop'
compressed_output = False
new_width_stretched = True

# a file compression method
# 1 means every frame is kept, 3 means every third frame is kept
frame_skipping = 1

# see tekkit/config/mod_ComputerCraft.cfg to set your own max_width and max_height values
if computer_type == 'laptop':
	max_width = 227
	max_height = 85
elif computer_type == 'desktop':
	# 426 on my desktop computer
	max_width = 426
	# 160 on my desktop computer
	max_height = 160
else:
	print('You didn\'t enter a valid \'computer_type\' name!')

print('Saving every ' + str(frame_skipping) + ' frame(s)')

names = os.listdir('inputs')
for name in names:
	process_frames(name, computer_type)
	# moving file
	os.rename('inputs/' + name, 'temp inputs/' + name)

time_elapsed = time.time() - t0

minutes = floor(time_elapsed / 60)
seconds = time_elapsed % 60

print('Done! Duration: {}m, {:.2f}s'.format(minutes, seconds))
