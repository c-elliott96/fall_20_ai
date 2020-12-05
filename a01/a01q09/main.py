# File: main.py
# Author: Christian Elliott

def floatrange(a, b=None, c=1):
  float_range = []
  if b == None:
    aa = float(0)
    while aa < a:
      float_range.append(float(aa))
      aa += c
    return float_range
  else:
    aa = float(a)
    bb = float(b)
    while aa < bb:
      float_range.append(aa)
      aa += c
    return float_range

if __name__ == '__main__':
  a = input()
  b = raw_input() # Enter "" w/o quotes for default b and c
  c = raw_input() # Enter "" w/o quotes for default c

  if b == '':
    print floatrange(a)
  else:
    b = float(b)
    if c == '':
      print floatrange(a, b)
    else:
      c = float(c)
      print floatrange(a, b, c)