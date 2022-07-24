#!/usr/bin/python3
import sys, re, os, time

r_name = r"[a-zA-Z0-9_<>]+"
r_name_attr = r"[a-zA-Z0-9_<>\[\]]+"
rx_class = re.compile(fr"\bclass\s+({r_name})")
rx_method = re.compile(fr"\b{r_name_attr}\s+({r_name}\(.*\))")

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

  print("--- tags start ---")
  print("\n".join(tags))
  print("--- tags end ---")

  with open("tags", "w") as file:
    tags.sort()
    file.write("\n".join(tags))

  print(f"Done in {time.time() - start_time}")

def parse_class(line):
  match = rx_class.search(line)
  return match.group(1) if match else None

def parse_method(line):
  match = rx_method.search(line)
  if match:
    capture = match.group(1)
    for symbol in ["<", "("]:
      index = capture.find(symbol)
      if index > -1:
        return capture[:index]
    return capture
  return None

def add_class_tag(file_name, line, line_num, tags):
  tag = parse_class(line)
  if tag:
    tags.append("\t".join([tag, file_name, rf"/class\s\+{tag}/"]))

def add_method_tag(file_name, line, line_num, tags):
  tag = parse_method(line)
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
      line_num += 1
    return tags

if __name__ == "__main__":
  main()
