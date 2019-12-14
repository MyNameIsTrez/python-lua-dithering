## IMPORTING ####################

import os
import sys
import time
from PIL import Image
from copy import copy, deepcopy

import dithering # should be placed in the same folder as this program

## COLORING TERMINAL OUTPUT TEXT ####################

class bcolors:
	HEADER = "\033[95m"
	OKBLUE = "\033[94m"
	OKGREEN = "\033[92m"
	WARNING = "\033[93m"
	FAIL = "\033[91m"
	ENDC = "\033[0m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"

## EDITABLE VARIABLES ####################

computer_type = "desktop" # "laptop" or "desktop".
new_width_stretched = True
output_images = False

# see tekkit/config/mod_ComputerCraft.cfg
if computer_type == "laptop":
	max_width = 227
	max_height = 85
elif computer_type == "desktop":
	max_width = 426
	max_height = 160
else:
	print(bcolors.FAIL + "You didn't enter a valid 'computer_type' name!" + bcolors.ENDC)

## FUNCTIONS ####################

def get_images_array(full_name):
	infile = "inputs/" + full_name
	extension = full_name.split(".", 1)[1] # get the extension after the "."
	name = full_name.split(".", 1)[0] # get the name before the "." by taking the first element
	print(bcolors.OKBLUE + "Name: " + bcolors.HEADER + name + bcolors.ENDC)

	try:
		old_image = Image.open(infile) # image holds all frames, but can be treated as frame 0 at the start

		old_width = old_image.size[0]
		old_height = old_image.size[1]

		new_height = max_height
		
		# get the new image width
		if new_width_stretched:
			new_width = max_width - 1 # the CC config's terminal_width variable has to be subtracted by 1
		else:
			new_width = int(new_height * old_width / old_height)

		print(bcolors.OKGREEN + "	Old size: " + bcolors.WARNING + str(old_width) + " x " + str(old_height) + bcolors.ENDC)
		print(bcolors.OKGREEN + "	New size: " + bcolors.WARNING + str(new_width) + " x " + str(new_height) + bcolors.ENDC)
	except IOError:
		print("Cant load"), infile
		sys.exit(1)

	if extension == "gif":
		# the next line possibly helps, but it breaks the output right now, see the next comment
		# mypalette = image.getpalette()

		new_images = []

		try:
			i = 0
			while 1:
				# the next line possibly helps, but it breaks the output right now
				# image.putpalette(mypalette)

				new_image = old_image.convert("RGBA")
				new_image = new_image.resize((new_width, new_height), Image.ANTIALIAS)
				if output_images:
					new_image.save("output-images/" + str(i) + ".png")

				new_images.append(new_image)

				i += 1
				old_image.seek(old_image.tell() + 1) # image now holds the next frame

		except EOFError:
			return new_images # return array
	elif extension == "jpeg":
		new_image = old_image.convert("RGB")
		new_image.save("output-images/" + name + ".jpeg")
		return [non_transparent] # return the image output in an array

def get_brightness(tup):
	# not all rgb colors are equally bright. multipliers gotten from a stackoverflow comment.
	brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
	if len(tup) == 4:
		return brightness * tup[3] / 255
	else:
		return 0

def media_convert_to_chars(full_name, imgs):
	real_frames = [] # holds the actual brightness values
	optimized_frames = [] # holds the brightness values, but with "t" if the (x, y)'s brightness is the same as the last frame

	width, height = imgs[0].size

	frameCount = len(imgs)
	for f in range(frameCount):
		img = imgs[f]
		pix = img.load()

		real_frames.append([])
		optimized_frames.append([])
		for x in range(width):
			real_frames[f].append([])
			optimized_frames[f].append([])

			for y in range(height):
				brightness = get_brightness(pix[x, y])
				brightness = round(brightness * 100) / 100

				real_frames[f][x].append(brightness)
				
				if f > 0:
					# save the brightness if it isn't equal to the brightness of the last frame, else save "t" to indicate it shouldn't draw here
					diff = brightness - real_frames[f - 1][x][y]
					if diff:
						char = dithering.getClosestChar(brightness)
					else:
						char = "t" # signifies repetition of a previous frame's character; this character should never get drawn
					optimized_frames[f][x].append(char)
				else:
					char = dithering.getClosestChar(brightness)
					optimized_frames[f][x].append(char) # necessary to create initial_frame, and for the 2nd frame
	
	# get the initiallly drawn frame, that doesn't get drawn after each loop
	initial_frame = deepcopy(optimized_frames)[0]

	# I SUSPECT THIS CODE CAUSES THE LAST FRAME TO NOT BE CLEARED COMPLETELY FOR SOME REASON!!!
	for x in range(width):
		for y in range(height):
			# sets the first frame character position to "t", if the last frame's equal character position is the same character
			if real_frames[-1][x][y] == real_frames[0][x][y]:
				real_frames[0][x][y] = "t" # signifies repetition of a previous frame's character; this character should never get drawn

	save_string(full_name, width, height, initial_frame, optimized_frames, frameCount)

def save_string(full_name, width, height, initial_frame, optimized_frames, frameCount):
	name = full_name.split(".",1)[0] # get the name before the "."
	result_file = open(computer_type + " outputs/" + name + ".txt", "w")
	
	initial_frame_list = []
	# add all strings in initial_frame to stringList
	for x in range(width):
		for y in range(height):
			s = initial_frame[x][y]
			initial_frame_list.append(s)
	
	optimized_frames_list = []
	# add all strings in optimized_frames to stringList
	for f in range(frameCount):
		for x in range(width):
			for y in range(height):
				s = optimized_frames[f][x][y]
				optimized_frames_list.append(s)
	
	string_initial_frame = "".join(initial_frame_list)
	string_optimized_frames = "".join(optimized_frames_list)

	data = {
		"width": width,
		"height": height,
		"frame_count": frameCount,
		"initial_frame": string_initial_frame,
		"optimized_frames": string_optimized_frames
	}

	string = str(data)

	string = string.replace("'width': ", "width=")
	string = string.replace(", 'height': ", ",height=")
	string = string.replace(", 'frame_count': ", ",frame_count=")
	string = string.replace(", 'initial_frame': ", ",initial_frame=")
	string = string.replace(", 'optimized_frames': ", ",optimized_frames=")
	
	result_file.write(string)

	result_file.close()

## MAIN FUNCTION ####################

def main():
	startTime = time.time()

	print(bcolors.OKBLUE + "Computer type: " + bcolors.HEADER + computer_type)

	names = os.listdir("inputs")
	for name in names:
		media_convert_to_chars(name, get_images_array(name))

	precision = 10 ** 3
	elapsedTime = int((time.time() - startTime) * precision) / precision

	print(bcolors.OKBLUE + "Elapsed time: " + bcolors.HEADER + str(elapsedTime) + " seconds." + bcolors.ENDC)

## CODE EXECUTION ####################

main()