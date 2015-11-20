#!/usr/bin/python
from sys import stdin
from sys import argv

keep = {}

for line in stdin:
  inline = line.strip("\r").strip("\n")
  outline = None
  """
    If we got more than one parameter, treat each argument as a line in a 
    program. If we got a single parameter eval it directly into the outline
  """
  if (len(argv) > 2):
     exec("\n".join(argv[1:]))
  elif len(argv) == 1:
     pass
  else:
     outline = eval(argv[1])
  if (outline != None):
    print outline
