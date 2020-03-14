import os

width = 30
height = 30

names = os.listdir('outputs')

string = '    size_' + str(width) + 'x' + str(height) + ' = {'

for name in names:
	if name != '.empty': # '.empty' prevents the folder from being removed on GitHub
		string += '\n        ' + name + ','

string += '\n    }'

print(string)