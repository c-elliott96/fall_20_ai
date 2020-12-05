# File: main.py
# Author: Christian Elliott
import Queue

def crossover(xs=None, ys=None, index0=0, index1=0):
  if isinstance(xs, str) and isinstance(ys, str):
    us = []
    vs = []
    queue_us = Queue.Queue()
    queue_vs = Queue.Queue()
    for i, char in enumerate(xs):
      if i >= index0 and i < index1: 
        queue_us.put(ys[i])
        queue_vs.put(char)
    for i, char in enumerate(xs):
      if i >= index0 and i < index1:
        us.append(queue_us.get())
      else:
        us.append(char)
    for i, char in enumerate(ys):
      if i >= index0 and i < index1:
        us.append(queue_vs.get())
      else:
        us.append(char)
    us_str = ""
    vs_str = ""
    for element in us:
      us_str += element
    for element in vs:
      vs_str += element

    return us_str, vs_str

  elif isinstance(xs, list) and isinstance(ys, list):
    for i, val in enumerate(xs):
      if i >= index0 and i < index1:
        temp = val
        xs[i] = ys[i]
        ys[i] = temp

    return xs, ys
  else:
    raise ValueError("ERROR in crossover: xs=%s, ys=%s" % (xs, ys))

if __name__ == '__main__':
  i = input() # Enter 0 for string xs and 1 for int list xs

  if i == 0:
    xs = raw_input()  # for instance enter "abcdefghi" (w/o quotes)
    ys = raw_input()  # for instance enter "ABCDEFGHI" (w/o quotes)
  else:
    xs = raw_input()    # for instance enter "5,3,1,2,6,5"
    xs = xs.split(",")  # xs becomes ['5','3','1','2','6','5']
    xs = [int(x) for x in xs] # xs becomes [5,3,1,2,6,5]

    ys = raw_input()
    ys = ys.split(",")
    ys = [int(y) for y in ys] 

  index0 = input()
  index1 = input()
  us, vs = crossover(xs, ys, index0, index1)
  print us
  print vs
