from bisect import bisect_left


## README ####################

# The purpose of this library is to create a dithering effect using only uncolored ComputerCraft (Minecraft) characters.
# This library's get_closest_char() function takes a number between 0 and 1 inclusively, and returns a ComputerCraft character.
# 0 is ' ' and 1 is '@', and numbers between there get other ComputerCraft characters.
# The characters in the chars table are ordered by the number of cyan 3x3 pixels they are drawn with to accomplish this task.

# This file contains a table with characters in it from Tekkit Classic's ComputerCraft (1.33) character set.
# The ordering of this table was done with another python script that has since been deleted.


## UNEDITABLE VARIABLES ####################


chars = [
	' ', '.', "'", ':', '-', '!', '/', '(', '=', '%',
	'1', 'C', '3', '$', '2', '5', 'A', '0', '#', '@'
]

char_indices = [
	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
	11, 12, 13, 14, 15, 16, 17, 18, 19
]


## FUNCTIONS ####################


def take_closest(my_number):
	"""
	Assumes myList is sorted. Returns closest value to my_number.

	If two numbers are equally close, return the smallest number.
	"""
	pos = bisect_left(char_indices, my_number)
	if pos == 0:
		return char_indices[0]
	if pos == len(char_indices):
		return char_indices[-1]
	before = char_indices[pos - 1]
	after = char_indices[pos]
	if after - my_number < my_number - before:
	   return after
	else:
	   return before

# The given n should be between 0 and 1, both inclusive.
def get_closest_char(n):
	if n < 0 or n > 1:
		raise invalidInput("getClosestChar expected a float between 0 and 1, both inclusive")
	
	float_index = n * 20 # there are 20 chars that can be picked
	closest_index = take_closest(float_index)
	return chars[closest_index]