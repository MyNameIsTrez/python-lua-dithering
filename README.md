# python-lua-dithering

Python program to transform video and image files into a dithered format, that can be displayed using the ComputerCraft mod for Minecraft.

## Getting Started

* Put video and/or image files in the *inputs* folder.
* Run main.py to convert the files to a dithered format.
* The resulting files are found in the *outputs* folder.

### Dependencies

Run `pip install -r requirements.txt` to install all the dependencies automatically.

* [opencv-python](https://pypi.org/project/opencv-python/) - Converts .mp4 files to an array of frames.
* [Pillow](https://pypi.org/project/Pillow/) - Converts frames to pixels with RGBA values.