import os
import time
import cv2
from PIL import Image
import dithering

def process_frames(full_file_name, computer_type):
	extension = full_file_name.split('.', 1)[1] # get the extension after the '.'
	file_name = full_file_name.split('.', 1)[0] # get the name before the '.'
	output_path = computer_type+' outputs/'+file_name+'.txt'
	
	if not os.path.isfile(output_path): # COMMENT THIS BACK IN WHEN DONE WITH TESTING
		print('processing '+file_name)

		# get information about the file
		video = cv2.VideoCapture('inputs/'+full_file_name)

		old_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
		old_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

		# get the new image width
		new_height = max_height
		if new_width_stretched:
			new_width = max_width - 1 # the CC config's terminal_width variable has to be subtracted by 1
		else:
			new_width = int(new_height * old_width / old_height)

		frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) # inaccurate, but fast

		# prepare output file for writing data
		string = '{width=' + '{},height={},frame_count={},optimized_frames=\''.format(
			new_width, new_height, frame_count)
		open(output_path, 'w').write(string)
		
		if extension == 'mp4':
			last_string = None
			i = 0
			while True:
				hasFrames, cv2_frame = video.read()
				if hasFrames:
					cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB) # is this necessary?
					pil_frame = Image.fromarray(cv2_frame)
					pil_frame = pil_frame.convert('RGBA')
					
					# resize the image to the desired width and height
					pil_frame = pil_frame.resize((new_width, new_height), Image.ANTIALIAS)
					
					last_string = process_frame(pil_frame, i, last_string, new_width, new_height, output_path)
					
					i = i + 1
				else:
					video.release()
					break
			
			string = '\',initial_frame=\''
			open(output_path, 'a').write(string)
			
			string = '\'}'
			open(output_path, 'a').write(string)
		elif extension == 'gif':
			1
	else:
		print('skipping \''+file_name+'\', as it has already been outputted')

def process_frame(frame, i, last_string, new_width, new_height, output_path):
	t1 = time.time()
	frame_pixels = frame.load()
	
	string = ''
	for x in range(new_width):
		for y in range(new_height):
			brightness = get_brightness(frame_pixels[x, y])
			char = dithering.getClosestChar(brightness)
			if last_string == None or char != last_string[y + x * 160]:
				string = string+char
			else:
				string = string+'t'
	
	last_string = string
	open(output_path, 'a').write(string)
	progress = 'frame '+str(i)+'/5301'
	i = i + 1
	speed = str(round(time.time()-t1, 2)) + 's/frame'
	print('    '+progress+', '+speed, end='\r', flush=True)
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
computer_type = 'desktop'
new_width_stretched = True
max_width = 426
max_height = 160

names = os.listdir('inputs')
for name in names:
	process_frames(name, computer_type)

d = time.time() - t0
print ('duration: %.2fs.' % d)