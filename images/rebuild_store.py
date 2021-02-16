import os
import json
import random
import string
from glob import glob

base_path = os.path.dirname(os.path.realpath(__file__))

STORE_FILE = os.path.join(base_path, 'store.json')

dirs = glob(base_path + '/*/')

store = {}

def generate_id():
  return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(3))

try:
  if not os.path.isfile(STORE_FILE):
    open(STORE_FILE, 'w').close()

  with open(STORE_FILE, 'r') as file:
    store = json.load(file)
except ValueError as e:
  print(f'Could not read JSON file. {e}')

for dir in dirs:
  dir_name = os.path.basename(os.path.dirname(dir))
  file_paths = set()

  for file in os.listdir(dir):
    file_paths.add(os.path.join(dir_name, file))

  kind = store.get(dir_name, { "files": [] })

  stored_paths = set([x['path'] for x in kind.get('files')])
  common_paths = set(file_paths) & set(stored_paths)
  new_paths = set([x for x in file_paths if x not in stored_paths])

  # Keep unchanged files
  kind['files'] = [x for x in kind.get('files') if x['path'] in common_paths]

  # Create and save files with new paths
  for path in new_paths:
    kind.get('files').append({
      "id": generate_id(),
      "path": path
    })

  store[dir_name] = kind

with open(STORE_FILE, 'w+') as file:
  json.dump(store, file, sort_keys=True, indent=2)