# File: main.py
# Author: Christian Elliott

import requests
import string

def chars(url):
  s = requests.get(url).text

  d1 = dict.fromkeys(string.ascii_letters, 0)
  d2 = dict.fromkeys(string.digits, 0)
  d3 = d1.copy() # d3 has d1's items
  d3.update(d2)

  for char in s:
    if char in d3:
      d3.update({char : d3.get(char) + 1})
  
  total_chars = 0
  for val in d3.items():
    total_chars += val[1]
  
  list_dict = []
  for key, val in d3.items():
    list_dict.append((key, val))

  sorted_by_char = []
  for key, val in sorted (list_dict):
    sorted_by_char.append((key, val, float(val) / float(total_chars)))

  sorted_by_freq = sorted_by_char[:]
  sorted_by_freq.sort(key = lambda x: x[2], reverse=True)

  for i in sorted_by_char:
    print i[0], i[1], i[2]

  print ""

  for i in sorted_by_freq:
    print i[0], i[1], i[2]

if __name__ == '__main__':
  chars('http://news.yahoo.com')