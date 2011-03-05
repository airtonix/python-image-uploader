import os

def assure_path (path):
	""" checks if it exists and makes it if it doesnt """
	if not os.path.exists(path):
		os.makedirs(path)
	return path

def assure_file (path):
	""" checks if it exists and makes it if it doesnt """
	if not os.path.exists(path):
		assured_file = open(path)
		assured_file.close()
	return path

