import json
import os

default_paths = {
  "input_path": "./input",
  "output_path": "./output.csv"
}

json_file_path = 'path.json'

def load_paths():
  """
  Load the input and output paths from the JSON file.
  If the file or the values don't exist, create the file with default paths.
  """
  if not os.path.exists(json_file_path):
    _create_default_file()
  else:
    _check_and_update_paths()

  with open(json_file_path, 'r') as file:
    paths = json.load(file)
    input_path = paths.get("input_path", default_paths["input_path"])
    output_path = paths.get("output_path", default_paths["output_path"])
  return input_path, output_path

def _create_default_file():
  """
  Create the JSON file with default input and output paths.
  """
  with open(json_file_path, 'w') as file:
      json.dump(default_paths, file, indent=4)
  print(f"{json_file_path} created with default paths.")

def _check_and_update_paths():
  """
  Check if the paths exist in the JSON file, update if they are missing.
  """
  with open(json_file_path, 'r') as file:
    try:
      paths = json.load(file)
    except json.JSONDecodeError:
      paths = {}

  updated = False
  for key, value in default_paths.items():
    if key not in paths:
      paths[key] = value
      updated = True

  if updated:
    with open(json_file_path, 'w') as file:
      json.dump(paths, file, indent=4)
    print(f"{json_file_path} updated with missing paths.")