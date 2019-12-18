import os
import time
from math import floor
import cv2
from PIL import Image
import dithering

def process_frames(full_file_name, computer_type):
	extension = full_file_name.split('.', 1)[1] # get the extension after the '.'
	file_name = full_file_name.split('.', 1)[0] # get the name before the '.'
	input_path = 'inputs/'+full_file_name
	output_path = computer_type+' outputs/'+file_name+'.txt'
	
	if not os.path.isfile(output_path): # COMMENT THIS BACK IN WHEN DONE WITH TESTING
		with open(output_path, 'a') as output_file:
			print('Processing \''+file_name+'\'.')

			if extension == 'mp4':
				# get information about the video file
				video = cv2.VideoCapture(input_path)
				old_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
				old_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
			elif extension == 'gif' or extension == 'jpeg':
				try:
					old_image = Image.open(input_path)
					old_width = old_image.size[0]
					old_height = old_image.size[1]
				except IOError:
					print('Can\'t load \''+file_name+'\'.'), infile
					sys.exit(1)
			else:
				print('Entered an invalid file type; only mp4, gif and jpeg are allowed!')

			# get the new image width
			new_height = max_height
			if new_width_stretched:
				new_width = max_width
			else:
				new_width = int(new_height * old_width / old_height)
			
			# prepare output file for writing data
			string = '{width='+'{},height={},optimized_frames="'.format(new_width, new_height)
			output_file.write(string)

			i = 0
			
			if extension == 'mp4':
				while True:
					hasFrames, cv2_frame = video.read()
					frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) # inaccurate, but fast
					if hasFrames:
						cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB) # is this necessary?
						pil_frame = Image.fromarray(cv2_frame)
						pil_frame = pil_frame.convert('RGBA')
						
						# resize the image to the desired width and height
						pil_frame = pil_frame.resize((new_width, new_height), Image.ANTIALIAS)
						
						process_frame(pil_frame, i, new_width, new_height, output_file, frame_count)
						
						i = i + 1
					else:
						video.release()
						break
			elif extension == 'gif' or extension == 'jpeg':
				if extension == 'gif':
					# mypalette = image.getpalette() # possibly helps
					try:
						while 1:
							# image.putpalette(mypalette) # possibly helps
							new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
							process_frame(new_image, i, new_width, new_height, output_file, None)
							old_image.seek(old_image.tell() + 1) # gets the next frame
							i = i + 1
					except:
						frame_count = i # continue
				elif extension == 'jpeg':
					new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
					new_image = new_image.convert('RGB')
					process_frame(new_image, i, new_width, new_height, output_file, 1)
					frame_count = 1
			else:
				print('Entered an invalid file type; only mp4, gif and jpeg are allowed!')
			
			string = '",frame_sleep=' + str(frame_sleep) # -1 is no sleeping
			output_file.write(string)
			
			string = ',frame_count={}}}'.format(frame_count) # '}}' necessary, because you get a 'ValueError' with '}'
			output_file.write(string)
			print()

			output_file.close()
	else:
		print('Skipping \''+file_name+'\'.')

def process_frame(frame, i, new_width, new_height, output_file, frame_count):
	t1 = time.time()
	
	# return to skip this frame
	if i % frame_skipping != 0:
		return
	
	frame = frame.convert('RGBA')
	frame_pixels = frame.load()
	
	string = ''
	for y in range(new_height):
		# string=string+"|" # probably wanted when you include spaces, but I couldn't get this to work
		for x in range(new_width):
			brightness = get_brightness(frame_pixels[x, y])
			char = dithering.getClosestChar(brightness)

			# I'd love to use spaces, but it messes ComputerCraft's terminal up for some reason
			if (char == " "):
				char = "."
			
			string = string+char
		# string=string+"|"
	
	output_file.write(string)
	current_frame = i+1
	progress = 'Frame '+str(i+1)+'/'
	if frame_count:
		progress = progress+str(frame_count)
	else:
		progress = progress+'?'
	i = i + 1
	elapsed = time.time()-t1
	speed = '{:.2f}s/frame'.format(elapsed)
	frames_left = (frame_count - current_frame) / frame_skipping
	eta_minutes = floor(elapsed * frames_left / 60)
	eta_seconds = floor(elapsed * frames_left) % 60
	eta = '{}m, {}s left'.format(eta_minutes, eta_seconds)
	print('    '+progress+', '+speed+', '+eta, end='\r', flush=True)

def get_brightness(tup):
	# red, green and blue aren't equally bright
	brightness = (0.2126*tup[0] + 0.7152*tup[1] + 0.0722*tup[2]) / 255
	if len(tup) == 4:
		return brightness * tup[3] / 255
	else:
		return 0

t0 = time.time()

# user settings
computer_type = 'laptop'
new_width_stretched = True

# 1 means every frame is kept, 3 means every third frame is kept.
# this is a file compression method
frame_skipping = 2

frame_sleep = 0.1 # seconds of sleeping between frames, -1 is no sleeping

# see tekkit/config/mod_ComputerCraft.cfg
if computer_type == 'laptop':
	max_width = 227
	max_height = 85
elif computer_type == 'desktop':
	max_width = 426
	max_height = 160
else:
	print(bcolors.FAIL + 'You didn\'t enter a valid \'computer_type\' name!' + bcolors.ENDC)

names = os.listdir('inputs')
for name in names:
	process_frames(name, computer_type)

d = time.time() - t0

minutes = floor(d / 60)
seconds = d % 60

print('Duration: {}m, {:.2f}s.'.format(minutes, seconds))