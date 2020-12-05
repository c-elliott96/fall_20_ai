# File: main.py
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

# f function here
def f(xs):
  # xs is a list of chars
  f_list = []  
  for i in range(len(xs) - 1):
    window = [xs[i], xs[i + 1]]
    f_list.append(window)
  return f_list

# g function here
def g(xs):
  g_list = []
  for inner in xs:
    g_list.append(inner[0])
  g_list.append(xs[len(xs)-1][1])
  return g_list

if __name__ == '__main__':
  option = input()
  if option == 1: # test f
    s = raw_input() # enter "a,b,c,d,e" without quotes
    xs = s.split(",") # xs is ["a","b","c","d","e"]
    print f(xs)
  else: # test g
    s = raw_input() # enter "a,b,b,c,c,d,d,e" without double quotes
    xs = matrix(2, s) # xs is [["a","b"],["b","c"],["c","d"],["d","e"]]
    print g(xs)