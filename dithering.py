from bisect import bisect_left


## README ####################

# The purpose of this library is to create a dithering effect using only uncolored ComputerCraft (Minecraft) characters.
# This library's get_closest_char() function takes a number between 0 and 1 inclusively, and returns a ComputerCraft character.
# 0 is ' ' and 1 is '@', and numbers between there get other ComputerCraft characters.
# The characters in the chars table are ordered by the number of cyan 3x3 pixels they are drawn with to accomplish this task.

# This file contains a table with characters in it from Tekkit Classic's ComputerCraft (1.33) character set.
# The ordering of this table was done with another python script that has since been deleted.


## UNEDITABLE VARIABLES ####################

## VANILLA TEKKIT CHARACTER SET

chars_default = [
	' ', '.', "'", ':', '-', '!', '/', '(', '=', '%',
	'1', 'C', '3', '$', '2', '5', 'A', '0', '#', '@'
]

char_indices_default = [
	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
	11, 12, 13, 14, 15, 16, 17, 18, 19
]

## GRAYSCALE TEKKIT CHARACTER SET, BY REPLACING ALL 94 AVAILABLE CHARACTERS WITH GRAYSCALE COLORS

chars_extended = [
    ' ', '!', '\\"', '#', '$', '%', '&', "\\'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'
]

# need this, because 64 is removed, because the ` character can't be inserted into a computer
char_indices_extended = [
	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93
]


## FUNCTIONS ####################


def take_closest_default(my_number):
	"""
	Assumes myList is sorted. Returns closest value to my_number.

	If two numbers are equally close, return the smallest number.
	"""
	pos = bisect_left(char_indices_default, my_number)
	if pos == 0:
		return char_indices_default[0]
	if pos == len(char_indices_default):
		return char_indices_default[-1]
	before = char_indices_default[pos - 1]
	after = char_indices_default[pos]
	if after - my_number < my_number - before:
	   return after
	else:
	   return before

# The given n should be between 0 and 1, both inclusive.
def get_closest_char_default(n):
	if n < 0 or n > 1:
		raise invalidInput("get_closest_char expected a float between 0 and 1, both inclusive")
	
	float_index = n * 20 # there are 20 chars that can be picked
	closest_index = take_closest_default(float_index)
	return chars_default[closest_index]





def take_closest_extended(my_number):
	"""
	Assumes myList is sorted. Returns closest value to my_number.

	If two numbers are equally close, return the smallest number.
	"""
	pos = bisect_left(char_indices_extended, my_number)
	if pos == 0:
		return char_indices_extended[0]
	if pos == len(char_indices_extended):
		return char_indices_extended[-1]
	before = char_indices_extended[pos - 1]
	after = char_indices_extended[pos]
	if after - my_number < my_number - before:
	   return after
	else:
	   return before

# The given n should be between 0 and 1, both inclusive.
def get_closest_char_extended(n):
	if n < 0 or n > 1:
		raise invalidInput("get_closest_char_extended expected a float between 0 and 1, both inclusive")
	
	float_index = n * 94 # there are 94 chars that can be picked
	closest_index = take_closest_extended(float_index)
	return chars_extended[closest_index]