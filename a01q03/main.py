# File: main.my
# Author: Christian Elliott

def matrix(n, s, separator=','):
    s_split = s.split(separator)
    i = 0
    inner = []
    outer = []
    if s == "": return []
    for item in s_split:
        if i < n:
            try: inner.append(item)
            except IndexError:
                None
            i += 1
        if i == n:
            outer.append(inner)
            i = 0
            inner = []
    if len(s_split) % n != 0:
        outer.append(inner)
    return outer

def find_target(m, target = ' '):
  # m is a 2d array, which means we have to do 
  # array.index(' ') for each inner array
  # and also must catch ValueError that's thrown when 
  # ' ' is not present in a given sub-array. 
  m_iter = iter(m)
  for i in m_iter:
    for j in i:
      try location = j.index(' ')
      except ValueError: 
        None
  if location:
    return location
  else: 
    return None

def move2(direction, m, target = ' '):
  # m = some matrix of n x n structure, where one position is a space (' '). 
  # we must move the space in the direction of direction, either North, South, 
  # East, or West. 
  # If the space cannot move in that direction, the input matrix is returned. 
  # We must return m, and not a copy of it. 

  # Our matrix is created using a string of values to populate the matrix, and 
  # some n for n x n size matrix. We must use our matrix function from 
  # problem 1, which returns a 2d array to represent the matrix. 

  n = len(m[0]) # gets n by taking length of any 1 row in matrix  
  
  print "m:", m
  print "Find target:"
  find_target(m)
  # print "Space location:", space_location
  # First, we need to create cases for the different directions:
  # if direction == 'N':      # Direction is North: check to see if we can swap north
  #   if space_location < n:
  #     return m
  #   else:                   # here, we CAN make a swap. 
  #     temp = 

  return m

if __name__ == '__main__':
  direction = raw_input() # for instance enter "N" (w/o quotes)
  s = raw_input()         # for instance enter "1,2,3,4,5,6,7, ,8" 
                          # w/o quotes
  n = input()             # for instance enter 3
  m = matrix(n, s)
  target = raw_input()    # for instance enter " " (w/o quotes)
                          # Enter "" (w/o quotes) for default case.
  
  if target == '':
    print move2(direction = direction, m = m)
  else:
    print move2(direction = direction, m = m, target = target)