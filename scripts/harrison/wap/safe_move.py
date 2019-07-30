import os
import time

# moves regular files and renames them if necessary. Undefined behavior if directories are passed.
def safe_move(old_path, new_path):
	try:
		os.rename(old_path, new_path)
	except WindowsError as e:
		ext = new_path.rfind('.')
		timestring = str(time.time()).replace(".", "_")
		if(ext != -1):
			new_path = new_path[0:ext] + '(' + timestring + ')' + new_path[ext:len(new_path)]
			os.rename(old_path, new_path)
		else:
			new_path = new_path + '(' + timestring + ')'
			os.rename(old_path, new_path)
