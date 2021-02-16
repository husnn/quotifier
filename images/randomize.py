import os
import random, string

directory = os.path.dirname(os.path.realpath(__file__))

for root, dirs, files in os.walk(directory):
  for file in files:
    filename, ext = os.path.splitext(file)
    if (ext != '.jpg'): continue

    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

    filepath = os.path.join(root, file)
    new_filepath = os.path.join(root, x + ext)
    
    os.rename(filepath, new_filepath)