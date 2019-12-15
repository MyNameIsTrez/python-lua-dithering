## README ####################

# This file contains a public table, which contains every character in Tekkit Classic's 1.33 ComputerCraft character set.
# For every character in this table, it contains the number of cyan 3x3 pixels they are drawn with, which I dubbed 'blocks'.

# This is an unused artifact removal technique, that I can probably employ to improve the effectiveness of the dithering:
# https://news.ycombinator.com/item?id=15546769

## UNEDITABLE VARIABLES ####################

brightnessChars = {
	0: [' '],
	2: ['.'],
	3: ["'", ','],
	4: [':'],
	5: ['-', ';', '^', '_'],
	6: ['!', '"', '*', 'i', '|', '~'],
	7: ['/', '<', '>', '\\', 'l'],
	9: ['(', ')', '+', '?', 'Y', '?', 'r', 'v', 'x', '{', '}'], # 't' used to be here, between 'r' and 'v'. It is a reserved character to indicate not having to draw.
	10: ['=', 'J'],
	11: ['%', 'I', 'L', 'T', '[', ']', 'c', 'f', 'j'],
	12: ['1', '7', 'k', 'n', 'o', 'u'],
	13: ['C', 'F', 'V', 'X', 'm', 's', 'z'],
	14: ['3', 'P', 'a', 'h', 'p', 'q', 'w'],
	15: ['$', '&', '4', '6', '9', 'K', 'S', 'U', 'Z', 'e', 'y'],
	16: ['2', 'O', 'Q', 'b', 'd'],
	17: ['5', '8', 'E', 'G', 'H', 'M', 'N', 'W', 'g'],
	18: ['A', 'D', 'R'],
	19: ['0'],
	20: ['#', 'B'],
	24: ['@']
}

## FUNCTIONS ####################

def getHighestIndex():
	highestIndex = 1
	for index in list(brightnessChars):
		if index > highestIndex:
			highestIndex = index
	return highestIndex

highestIndex = getHighestIndex()

def getClosestIndex(floatIndex):
	keys = list(brightnessChars)
	firstIndex = keys[0]
	
	for index in list(brightnessChars):
		if index < floatIndex:
			previousIndex = index
		else:
			# previousIndex doesn't exist when floatIndex is 0, so return the first index.
			if index == firstIndex:
				return index
			
			# The closest index is previousIndex or index.
			# It's the one which is tne closest to floatIndex.
			previousIndexDiff = abs(floatIndex - previousIndex)
			indexDiff = abs(floatIndex - index)

			# If they are equal to each other, return index.
			# I treated this as an arbitrary decision, but maybe it isn't an arbitrary choice to make.
			if previousIndexDiff < indexDiff:
				return previousIndex
			else:
				return index

# The given n should be between 0 and 1, both inclusive.
def getClosestChar(n):
	if n < 0 or n > 1:
		raise invalidInput("getClosestChar expected a float between 0 and 1, both inclusive")
	
	floatIndex = n * highestIndex
	closestIndex = getClosestIndex(floatIndex)
	closestCharTable = brightnessChars[closestIndex]
	return closestCharTable[0] # For now, we always give the first character of the index its table.