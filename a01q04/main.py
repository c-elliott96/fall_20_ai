# File: main.py
# Author: Christian Elliott

# bring in matrix function
def matrix(n, s, separator = ','):
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

def queen_locations (m):
  location_list = []
  enum_m = enumerate(m)
  for row, val in enum_m:
    col = enumerate(val)
    for item in col:
      if item[1] == 'Q':
        location_list.append((row, item[0]))
  return location_list

def attacking_pairs(m):
  queens = queen_locations(m)
  attacking_queens = 0
  for i in range(len(queens)):
    for j in range(i + 1, len(queens)):
      if queens[i][0] == queens[j][0]:
        attacking_queens += 1
        continue
      elif abs(queens[i][0] - queens[j][0]) == abs(queens[i][1] - queens[j][1]):
        attacking_queens += 1
  return attacking_queens
  

if __name__ == '__main__':
  # For this:
  # +-+-+-+
  # |Q|Q| |
  # +-+-+-+
  # | | |Q|
  # +-+-+-+
  # | | | |
  # +-+-+-+
  s = raw_input()     # enter: "Q,Q, , , ,Q, , , " (w/o quotes)
  n = input()         # enter 3
  m = matrix(n, s,)   # m is a 3-by-3 2D array
  print attacking_pairs(m)