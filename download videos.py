import requests # Used for downloading any file type.

videos_info = [
	# NEWGROUNDS
	[
		'https://uploads.ungrounded.net/alternate/1448000/1448414_alternate_96550.720p.mp4',
		'ten years later',
		'mp4'
	],
	[
		'https://uploads.ungrounded.net/alternate/1443000/1443835_alternate_95750.720p.mp4',
		'takeout',
		'mp4'
	],
	[
		'http://uimg.ngfiles.com/icons/7349/7349981_large.png?f1578283262',
		'wavetro logo',
		'png'
	],
]

# Function I stole from StackOverflow:
# https://stackoverflow.com/a/35844551
def download_file(url, name, extension):
    r = requests.get(url, stream=True)
    with open('inputs/' + name + '.' + extension, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
		f.close() # Necessary?

for video_info in videos_info:
	url = video_info[0]
	name = video_info[1]
	extension = video_info[2]
	download_file(url, name, extension)