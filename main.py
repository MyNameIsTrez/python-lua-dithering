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

		# get the new image width
		new_height = max_height
		if new_width_stretched:
			new_width = max_width
		else:
			new_width = int(new_height * old_width / old_height)

		i = 0
		used_frame_count = 1
		if extension == 'mp4':
			# inaccurate, but fast
			actual_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
			frame_count = floor(actual_frame_count / frame_skipping)

			while True:
				hasFrames, cv2_frame = video.read()
				if hasFrames:
					if i % frame_skipping == 0:
						cv2_frame = cv2.cvtColor(
							cv2_frame, cv2.COLOR_BGR2RGB)  # is this necessary?
						pil_frame = Image.fromarray(cv2_frame)
						pil_frame = pil_frame.convert('RGBA')

						# resize the image to the desired width and height
						pil_frame = pil_frame.resize((new_width, new_height), Image.ANTIALIAS)
						process_frame(pil_frame, used_frame_count, new_width, new_height,
						              output_file, frame_count)

						used_frame_count += 1
					i += 1
				else:
					video.release()
					break
		elif extension == 'gif':
			# mypalette = old_image.getpalette() # possibly helps
			try:
				while True:
					if i % frame_skipping == 0:
						# old_image.putpalette(mypalette) # possibly helps
						new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
						process_frame(new_image, used_frame_count, new_width,
						              new_height, output_file, None)
						old_image.seek(old_image.tell() + 1)  # gets the next frame

						used_frame_count += 1
					i += 1
			except:
				frame_count = i  # continue
		elif extension == 'jpeg' or extension == 'png' or extension == 'jpg':
			new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
			# new_image = new_image.convert('RGB')
			process_frame(new_image, used_frame_count,
			              new_width, new_height, output_file, 1)

			used_frame_count = 1
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


def process_frame(frame, used_frame_count, new_width, new_height, output_file, frame_count):
	t1 = time.time()

	frame = frame.convert('RGBA')
	frame_pixels = frame.load()

	prev_char = None
	prev_char_count = 0
	string = ''

	modified_width = new_width - 1

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

	# gives each frame its own line, so it can be easily found and parsed
	output_file.write('\n' + string)

	# progress
	current_frame = used_frame_count + 1
	progress = 'Frame ' + str(current_frame) + '/'
	if frame_count:
		progress = progress + str(frame_count)
	else:
		progress = progress + '?'

	# speed
	elapsed = time.time() - t1
	processed_fps = floor(1 / elapsed)
	speed = '{} frames/s'.format(processed_fps)

	# eta
	if frame_count:
		frames_left = frame_count - current_frame
		seconds_left = elapsed * frames_left
		eta_minutes = floor(seconds_left / 60)
		eta_seconds = floor(seconds_left) % 60
		eta = '{}m, {}s left'.format(eta_minutes, eta_seconds)
	else:
		eta = '? left'

	clear = '		'

	print('    ' + progress + ', ' + speed +
	      ', ' + eta + clear, end='\r', flush=True)


def get_brightness(tup):
	# red, green and blue aren't equally bright
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

# 1 means every frame is kept, 3 means every third frame is kept.
# this is a file compression method
frame_skipping = 1

# see tekkit/config/mod_ComputerCraft.cfg
if computer_type == 'laptop':
	max_width = 227
	max_height = 85
elif computer_type == 'desktop':
	max_width = 426
	max_height = 160
else:
	print('You didn\'t enter a valid \'computer_type\' name!')

print('Saving every ' + str(frame_skipping) + ' frame(s)')

names = os.listdir('inputs')
for name in names:
	process_frames(name, computer_type)
	# moving file
	os.rename('inputs/' + name, 'temp inputs/' + name)

d = time.time() - t0

minutes = floor(d / 60)
seconds = d % 60

print('Done! Duration: {}m, {:.2f}s'.format(minutes, seconds))
