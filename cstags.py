#!/usr/bin/python3
import sys, re, os, time, glob

r_name = r"[a-zA-Z0-9_<>]+"
r_name_attr = r"[a-zA-Z0-9_<>\[\]]+"
rx_class = re.compile(fr"^\s*(?:{r_name_attr}\s+)*class\s+({r_name})")
rx_interface = re.compile(fr"^\s*(?:{r_name}\s+)*interface\s+({r_name})")
rx_method = re.compile(fr"^\s*({r_name_attr}\s+)+({r_name}\(.*\))")

def main():
  tags = []
  start_time = time.time()
  args = sys.argv[1:]
  if len(args) == 0:
    tags += get_tags_for_directory()
  else:
    for file_name in args:
      if file_name.endswith(".cs"):
        tags += get_tags_for_file(file_name)
      else:
        print(f"Warning: Skipping file '{file_name}'. Not '.cs' file type")

  print("--- tags start ---")
  print("\n".join(tags))
  print("--- tags end ---")

  with open("tags", "w") as file:
    tags.sort()
    file.write("\n".join(tags))

  print(f"Done in {time.time() - start_time}")

def get_tags_for_directory(directory=None):
  if not directory:
    directory = os.getcwd()
  tags = []
  for item in os.listdir(directory):
    abs_path = os.path.join(directory, item)
    print(abs_path)
    if os.path.isfile(abs_path) and item.endswith(".cs"):
      tags += get_tags_for_file(abs_path)
    elif os.path.isdir(abs_path):
      tags += get_tags_for_directory(abs_path)
  return tags

def parse_class(line):
  match = rx_class.search(line)
  if match:
    return sanitize_capture(match.group(1))

def parse_interface(line):
  match = rx_interface.search(line)
  if match:
    return sanitize_capture(match.group(1))

def parse_method(line):
  match = rx_method.search(line)
  if match:
    return sanitize_capture(match.group(2))

def sanitize_capture(capture):
  if not capture:
    return None
  for symbol in ["<", "("]:
    index = capture.find(symbol)
    if index > -1:
      return capture[:index]
  return capture

def add_class_tag(file_name, line, line_num, tags):
  add_tag(parse_class(line), file_name, line_num, tags)

def add_method_tag(file_name, line, line_num, tags):
  add_tag(parse_method(line), file_name, line_num, tags)

def add_interface_tag(file_name, line, line_num, tags):
  add_tag(parse_interface(line), file_name, line_num, tags)

def add_tag(tag, file_name, line_num, tags):
  if tag:
    tags.append("\t".join([tag, file_name, str(line_num)]))

def get_tags_for_file(file_name):
  try:
    file = open(file_name, "r")
  except:
    sys.stderr.write(f"Cannot open {file_name}")
  with file:
    line_num, tags = 1, []
    while True:
      line = file.readline()
      if not line:
        break
      add_class_tag(file_name, line, line_num, tags)
      add_method_tag(file_name, line, line_num, tags)
      add_interface_tag(file_name, line, line_num, tags)
      line_num += 1
    return tags

if __name__ == "__main__":
  main()
