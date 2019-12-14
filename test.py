from PIL import Image
import cv2

def getFrame(sec, video):
	video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
	hasFrames, cv2_im = video.read()
	if hasFrames:
		cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB) # is this necessary?
		pil_im = Image.fromarray(cv2_im)
		return pil_im
	return hasFrames

def getFrames(infile):
	print("Getting frames...")
	
	video = cv2.VideoCapture(infile)
	sec = 0
	sleep = 30 # how often an image is taken from the video, set to 1/60 for 60 fps animation
	count = 1
	frames = []

	while True:
		result = getFrame(sec, video)
		if result == False:
			return frames
		result.save("output images/" + str(sec) + ".png")
		frames.append(result)

		count = count + 1
		sec = sec + sleep
		sec = round(sec, 2)

frames = getFrames('inputs/never gonna give you up.mp4')
# print(frames)