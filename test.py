# from pytube import YouTube
# YouTube('http://youtube.com/watch?v=9bZkp7q19f0').streams.first().download()

from distutils.core import setup
from Cython.Build import cythonize

setup(name='Hello world app',
      ext_modules=cythonize("main.pyx"))