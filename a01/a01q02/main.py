def move(direction = None, m = None):
    space_val = m.index(" ")
    n = m[:]
    if direction == 'right':
        if space_val == len(n) - 1:
            return n
        else:
            temp = n[space_val + 1]
            n[space_val + 1] = n[space_val]
            n[space_val] = temp
            return n
    elif direction == 'left':
        if space_val == 0:
            return n
        else:
            temp = n[space_val - 1]
            n[space_val - 1] = n[space_val]
            n[space_val] = temp
            return n
    else:
        raise ValueError("ERROR in move: invald direction %s" % direction)

if __name__ == '__main__':
    direction = raw_input()
    s = raw_input()
    m = list(s)
    print move(direction = direction, m = m)