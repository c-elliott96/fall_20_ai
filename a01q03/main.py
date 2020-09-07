# File: main.my
# Author: Christian Elliott

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

def find_target(m, target = ' '):
  target_val = None
  for (i, v) in enumerate(m):
    try:
      target_val = v.index(' ')
      row = i
    except ValueError:
      None
  if target_val is not None:
    return (row, target_val)
  else:
    return None

def move2(direction, m, target = ' '):
  n = len(m[0])
  space_val = find_target(m, target)
  
  if direction == 'N':
    if space_val[0] == 0:
      return m
    else:
      temp = m[space_val[0] - 1][space_val[1]]
      m[space_val[0] - 1][space_val[1]] = m[space_val[0]][space_val[1]]
      m[space_val[0]][space_val[1]] = temp
      return m
  if direction == 'S':
    if space_val[0] == n - 1:
      return m
    else:
      temp = m[space_val[0] + 1][space_val[1]]
      m[space_val[0] + 1][space_val[1]] = m[space_val[0]][space_val[1]]
      m[space_val[0]][space_val[1]] = temp
      return m
  if direction == 'E':
    if space_val[1] == n - 1:
      return m
    else:
      temp = m[space_val[0]][space_val[1] + 1]
      m[space_val[0]][space_val[1] + 1] = m[space_val[0]][space_val[1]]
      m[space_val[0]][space_val[1]] = temp
      return m
  if direction == 'W':
    if space_val[1] == 0:
      return m
    else:
      temp = m[space_val[0]][space_val[1] - 1]
      m[space_val[0]][space_val[1] - 1] = m[space_val[0]][space_val[1]]
      m[space_val[0]][space_val[1]] = temp
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