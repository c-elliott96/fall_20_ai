# File: a01q01.py
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

if __name__ == '__main__':
    n = input()
    s = raw_input()

    separator = raw_input()

    if separator == '':
        print matrix(n = n, s = s)
    else:
        print matrix(n = n, s = s, separator = separator)