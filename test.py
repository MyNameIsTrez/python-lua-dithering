import time
import random
import cv2
from PIL import Image
from random import random # temporary
from memory_profiler import profile
import dithering

@profile
def process_frames():
	i = 0
	while True:
		t1 = time.time()
		hasFrames, cv2_frame = video.read()
		if hasFrames:
			cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB) # is this necessary?
			pil_frame = Image.fromarray(cv2_frame)
			pil_frame = pil_frame.convert('RGBA')
			
			# resize the image to the desired width and height
			pil_frame = pil_frame.resize((new_width, new_height), Image.ANTIALIAS)
			# process_frame(pil_frame, i)
			
			progress = 'frame '+str(i)+'/5301'
			speed = str(round(time.time()-t1, 2)) + 's/frame'
			print(progress+', '+speed, end='\r', flush=True)
			
			i = i + 1
		else:
			video.release()
			break

last_string = None
def process_frame(frame, i):
	global last_string
	t1 = time.time()
	string = ''
	# frame_pixels = frame.load()
	for x in range(new_width):
		for y in range(new_height):
			# brightness = get_brightness(frame_pixels[x, y])
			# char = dithering.getClosestChar(brightness)
			char = dithering.getClosestChar(random())
			# if last_string == None or char != last_string[y + x * 160]:
			string = string+char
			# else:
			# 	string = string+'t'
	last_string = string
	# open('random.txt', 'a').write(string)
	progress = 'frame '+str(i)+'/5301'
	speed = str(round(time.time()-t1, 2)) + 's/frame'
	print(progress+', '+speed, end='\r', flush=True)

# def get_brightness(tup):
# 	# red green and blue aren't equally bright
# 	brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
# 	if len(tup) == 4:
# 		return brightness * tup[3] / 255
# 	else:
# 		return 0

new_width_stretched = True
max_width = 426
max_height = 160
video = cv2.VideoCapture('inputs/never gonna give you up.mp4')

old_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
old_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

# get the new image width
new_height = max_height
if new_width_stretched:
	new_width = max_width - 1 # the CC config's terminal_width variable has to be subtracted by 1
else:
	new_width = int(new_height * old_width / old_height)	

t0 = time.time()
process_frames()
d = time.time() - t0
print ('duration: %.2fs.' % d)