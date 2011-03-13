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

def merge(target, source):
	stack = [(target, source)]
	while stack:
		current_target, current_source = stack.pop()
		for key in current_source:
			if key not in current_target:
				current_target[key] = current_source[key]
			else:
				if isinstance(current_source[key], dict) and isinstance(current_target[key], dict) :
					stack.append((current_target[key], current_source[key]))
				else:
					current_target[key] = current_source[key]
	return target

