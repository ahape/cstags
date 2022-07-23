#!/usr/bin/python3
"""
V1:
- Go through each file
- Create a tag for each CLASS

Example entry:
  [name_of_the_tag] [path/to/file] /public <match_expression>/
"""

import sys, re, os, time

rx_class = re.compile(r"\s+class\s+(\w+)")

def main():
  tags = []
  start_time = time.time()
  args = sys.argv[1:]
  if len(args) == 0:
    print("Not implemented: recursive tags")
    raise SystemExit

  for file_name in args:
    if file_name.endswith(".cs"):
      tags += get_tags_for_file(file_name)
    else:
      print(f"Warning: Skipping file '{file_name}'. Not '.cs' file type")

  print("\n".join(tags))

  with open("tags", "w") as file:
    tags.sort()
    file.write("\n".join(tags))

  print(f"Done in {time.time() - start_time}")

def add_class_tag(file_name, line, tags):
  match = rx_class.search(line)
  if match:
    tag = match.group(1)
    tags.append("\t".join([tag, file_name, rf"/class\s\+{tag}/"]))

def get_tags_for_file(file_name):
  try:
    file = open(file_name, "r")
  except:
    sys.stderr.write(f"Cannot open {file_name}")
  with file:
    tags = []
    while True:
      line = file.readline()
      if not line:
        break
      add_class_tag(file_name, line, tags)
    return tags

if __name__ == "__main__":
  main()
