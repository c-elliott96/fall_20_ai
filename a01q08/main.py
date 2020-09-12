# File: main.py
# Author: Christian Elliott

# given two arrays:
# a = [1,2,3,4,5,6] and b = [6,5,4,3,2,1]
# calling crossover(a, b, 3, 5)
# returns us = [1,2,3,3,2,6] and vs = [6,5,4,4,5,1] 
# in other words, swap values from argv[3] : argv[4] - 1
# AND RETURN BOTH OF THOSE NEW STRINGS/ARRAYS as a tuple

def crossover(xs=None, ys=None, index0=0, index1=0):
  # To be completed
  if isinstance(xs, str) and isinstance(ys, str):
    pass
  elif isinstance(xs, list) and isinstance(ys, list):
    pass
  else:
    raise ValueError("ERROR in crossover: xs=%s, ys=%s" % (xs, ys))

xs = 'abcdefghi'
ys = 'ABCDEFGHI'
crossover(xs, ys, 3, 5)

# if __name__ == '__main__':
#   i = input() # Enter 0 for string xs and 1 for int list xs

#   if i == 0:
#     xs = raw_input()  # for instance enter "abcdefghi" (w/o quotes)
#     ys = raw_input()  # for instance enter "ABCDEFGHI" (w/o quotes)
#   else:
#     xs = raw_input()    # for instance enter "5,3,1,2,6,5"
#     xs = xs.split(",")  # xs becomes ['5','3','1','2','6','5']
#     xs = [int(x) for x in xs] # xs becomes [5,3,1,2,6,5]

#     ys = raw_input()
#     ys = ys.split(",")
#     ys = [int(y) for y in ys] 

#   index0 = input()
#   index1 = input()
#   us, vs = crossover(xs, yes, index0, index1)
#   print us
#   print vs
