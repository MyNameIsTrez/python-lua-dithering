import os
import time
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
				new_width = max_width - 1 # the CC config's terminal_width variable has to be subtracted by 1
			else:
				new_width = int(new_height * old_width / old_height)
			
			# prepare output file for writing data
			string = '{width='+'{},height={},optimized_frames="'.format(new_width, new_height)
			output_file.write(string)

			last_string = None
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
						
						last_string = process_frame(pil_frame, i, last_string, new_width, new_height, output_file, frame_count)
						
						i = i + 1
					else:
						video.release()
						break
				
				string = '",initial_frame="'
				output_file.write(string)
				
				string = '",frame_count={}}}'.format(frame_count) # '}}' necessary, because you get a 'ValueError' with '}'
				output_file.write(string)
				print()
			elif extension == 'gif' or extension == 'jpeg':
				if extension == 'gif':
					# mypalette = image.getpalette() # possibly helps
					try:
						while 1:
							# image.putpalette(mypalette) # possibly helps
							new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
							last_string = process_frame(new_image, i, last_string, new_width, new_height, output_file, None)
							old_image.seek(old_image.tell() + 1) # gets the next frame
							i = i + 1
					except:
						1 # continue
				elif extension == 'jpeg':
					new_image = old_image.resize((new_width, new_height), Image.ANTIALIAS)
					new_image = new_image.convert('RGB')
					process_frame(new_image, i, last_string, new_width, new_height, output_file, 1)
				
				string = '",initial_frame="'
				output_file.write(string)
				
				frame_count = i # check if this doesn't cause an off-by-one error
				string = '",frame_count={}}}'.format(frame_count) # '}}' necessary, because you get a 'ValueError' with '}'
				output_file.write(string)
				print()
				# print(('It took {} frames to process this '+extension+'.').format(frame_count))
			else:
				print('Entered an invalid file type; only mp4, gif and jpeg are allowed!')
			output_file.close()
	else:
		print('Skipping \''+file_name+'\'.')

def process_frame(frame, i, last_string, new_width, new_height, output_file, frame_count):
	t1 = time.time()
	frame = frame.convert('RGBA')
	frame_pixels = frame.load()
	
	string = ''
	for x in range(new_width):
		for y in range(new_height):
			brightness = get_brightness(frame_pixels[x, y])
			char = dithering.getClosestChar(brightness)
			if last_string == None or char != last_string[y + x * new_height]:
				string = string+char
			else:
				string = string+'t'
	
	last_string = string
	output_file.write(string)
	progress = 'Frame '+str(i+1)+'/'
	if frame_count:
		progress = progress+str(frame_count)
	else:
		progress = progress+'?'
	i = i + 1
	speed = str(round(time.time()-t1, 2)) + 's/frame'
	print('    '+progress+', '+speed, end='\r', flush=True)
	# print()
	return last_string

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
print ('Duration: %.2fs.' % d)