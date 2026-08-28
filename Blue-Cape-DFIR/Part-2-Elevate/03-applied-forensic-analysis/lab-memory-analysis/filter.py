import subprocess
import argparse

def filter_file(file, filter):
  """Filters the file using grep"""
  
  new_file = subprocess.run(["cat", file, "grep", "-i", filter], capture_output=True, stdout=f, timeout=30)
  return new_file 

def save_file(file, output):
  import os

  if not os.path.exists(f'output'):
    with open('example.txt', 'w') as file:
        file.write('Content')
  else:
    choice = input('File already exists, Overwrite?(by default, yes) (y/n) ')   

  if choice.split() in ["Y", "y"]:
    with open(output
