from bisect import bisect_left


## README ####################


# This file contains a table with characters in it from Tekkit Classic's ComputerCraft (1.33) character set.
# The characters in the chars table are ordered by the number of cyan 3x3 pixels they are drawn with.
# The ordering of this table was done with another python script that has since been deleted.


## UNEDITABLE VARIABLES ####################


chars = [
	' ', '.', "'", ':', '-', '!', '/', '(', '=', '%',
	'1', 'C', '3', '$', '2', '5', 'A', '0', '#', '@'
]

charIndices = [
	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
	11, 12, 13, 14, 15, 16, 17, 18, 19
]


## FUNCTIONS ####################


def take_closest(myNumber):
	"""
	Assumes myList is sorted. Returns closest value to myNumber.

	If two numbers are equally close, return the smallest number.
	"""
	pos = bisect_left(charIndices, myNumber)
	if pos == 0:
		return charIndices[0]
	if pos == len(charIndices):
		return charIndices[-1]
	before = charIndices[pos - 1]
	after = charIndices[pos]
	if after - myNumber < myNumber - before:
	   return after
	else:
	   return before

# The given n should be between 0 and 1, both inclusive.
def getClosestChar(n):
	if n < 0 or n > 1:
		raise invalidInput("getClosestChar expected a float between 0 and 1, both inclusive")
	
	floatIndex = n * 20 # there are 20 chars that can be picked
	closestIndex = take_closest(floatIndex)
	return chars[closestIndex]