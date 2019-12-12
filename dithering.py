# -- README --------------------------------------------------------

# -- This file contains two public tables, which contain each character in Tekkit Classic's 1.33 ComputerCraft character set. The tables also contain the number of cyan 3x3 pixels they are drawn with, which I dubbed 'blocks', for each character.

# -- Artifact removal inspiration: https://news.ycombinator.com/item?id=15546769

# -- UNEDITABLE VARIABLES --------------------------------------------------------

# local charsSortedTables = {
#     [0] = {' '},
#     [2] = {'.'},
#     [3] = {"'", ','},
#     [4] = {':'},
#     [5] = {'-', ';', '^', '_'},
#     [6] = {'!', '"', '*', 'i', '|', '~'},
#     [7] = {'/', '<', '>', '\\', 'l'},
#     [9] = {'(', ')', '+', '?', 'Y', '?', 'r', 't', 'v', 'x', '{', '}'},
#     [10] = {'=', 'J'},
#     [11] = {'%', 'I', 'L', 'T', '[', ']', 'c', 'f', 'j'},
#     [12] = {'1', '7', 'k', 'n', 'o', 'u'},
#     [13] = {'C', 'F', 'V', 'X', 'm', 's', 'z'},
#     [14] = {'3', 'P', 'a', 'h', 'p', 'q', 'w'},
#     [15] = {'$', '&', '4', '6', '9', 'K', 'S', 'U', 'Z', 'e', 'y'},
#     [16] = {'2', 'O', 'Q', 'b', 'd'},
#     [17] = {'5', '8', 'E', 'G', 'H', 'M', 'N', 'W', 'g'},
#     [18] = {'A', 'D', 'R'},
#     [19] = {'0'},
#     [20] = {'#', 'B'},
#     [24] = {'@'}
# }

# local indices = {}
# local highestIndex

# -- FUNCTIONS --------------------------------------------------------

# local function getIndices()
# 	-- Can't use ipairs() here, because the indices in charsSortedTables are hardcoded.
# 	for index, value in pairs(charsSortedTables) do
# 		indices[#indices + 1] = index
# 	end
# 	table.sort(indices) -- pairs() doesn't retain the order, so we have to sort.
# end
# getIndices() -- Can't call functions before they're initialized.

# local function getHighestIndex()
# 	local highestIndex = 1
# 	for _, index in ipairs(indices) do
# 		if index > highestIndex then
# 			highestIndex = index
# 		end
# 	end
# 	return highestIndex
# end

# local function getClosestIndex(floatIndex)
# 	local previousIndex
# 	for _, index in ipairs(indices) do
# 		if index < floatIndex then
# 			previousIndex = index
# 		else
# 			-- previousIndex doesn't exist when floatIndex is 0, so return index.
# 			if not previousIndex then
# 				return index
# 			end
			
# 			-- The closest index is previousIndex or index, depending on which of the two floatIndex is closer to.
# 			local previousIndexDiff = math.abs(floatIndex - previousIndex)
# 			local indexDiff = math.abs(floatIndex - index)
# 			if previousIndexDiff < indexDiff then
# 				return previousIndex
# 			else
# 				return index
# 			end
# 		end
# 	end
# end

# -- n is between 0 and 1, both inclusive.
# function getClosestChar(n)
# 	if n < 0 or n > 1 then
# 		error("getClosestChar expected a float between 0 and 1, both inclusive", 2)
# 	end
	
# 	local floatIndex = n * getHighestIndex()
# 	local closestCharTable = charsSortedTables[getClosestIndex(floatIndex)]
# 	return closestCharTable[1] -- For now, we always give the first character of the index its table.
# end