import os

sizes = os.listdir('outputs')
for size in sizes:
	if size != '.empty': # '.empty' prevents the folder from being removed on GitHub
		string = '    ' + size + ' = {'

		names = os.listdir('outputs/' + size)
		for name in names:
			if name != '.empty': # '.empty' prevents the folder from being removed on GitHub
				string += '\n        ' + name + ','

		string += '\n    },'

		print(string)