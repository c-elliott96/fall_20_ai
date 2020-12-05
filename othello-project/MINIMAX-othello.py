################################################################################
# Bitstring class - designed to do all the heavy work behind the scenes, so
# that (in theory) we can write minimax as minimally as possible.
################################################################################

class Bitstring:
    def __init__(self, board):
        self.char_board = board
        self.bin_board = self.to_bin_board(board)
        self.board_size = len(board[0])

    def get_bv(self, char):
        if char == ' ':
            return 0b11
        elif char == 'W':
            return 0b10
        else:
            return 0b01

    def get_cv(self, bit):
        if bit == 0b11:
            return ' '
        elif bit == 0b10:
            return 'W'
        else:
            return 'B'
        
    def to_bin_board(self, board):
        bin_board = []
        for row in board:
            # bin_row = []
            tmp = 0b00
            for col in row:
                tmp <<= 2
                tmp |= self.get_bv(col)
                # bin_row.append(self.get_bv(col))
            bin_board.append(tmp)
        return bin_board
    
    def slice_bits(self, row):
        l = []
        n = self.board_size
        for i in range(1, n + 1):
            num = (row >> 2 * (n - i)) % 4 
            l.append(num)
        return l

    def get_bits_at(self, move):
        row = move[0]
        n = self.board_size
        col = move[1] + 1
        return (self.bin_board[row] >> 2 * (n - col)) % 4

    def move_on_board(self, move):
        return (move[0] >= 0 and move[0] < self.board_size and
                move[1] >= 0 and move[1] < self.board_size)

    def check_valid_move(self, move, player):
        directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]

        # Check that the val of move is ' ' = 0b11 = 3
        # AND that the move is actually a tile on the board
        if self.get_bits_at(move) != 0b11 or not self.move_on_board(move):
            return False

        if player == 'B':
            other_player = 0b10 # other player is 'W' == 0b10
        else:
            other_player = 0b01 # other player is 'B' == 0b01

        spaces_to_flip = []
        
    
    # TODO:
    # calculation functions that MINIMAX will need for checking possible
    # state paths.
    #
    # For example, we'll want to be able to determine possible next-move
    # locations, which will involve all the directional checks we wrote in
    # the RandomOthelloPlayer class.

    # Another TODO:
    # Right now, Bitstring.bin_board is a 2D list.
    # We need that to be 1D, where each row is a 0b number.
    # This is so we can do simple, fast calculations for the above todo.

    # Comparing two piece values using XOR:
    #
    # Suppose it is BLACK's turn. Let TURN = 0b01
    # Let VAL = the tile we're comparing our potential move location to
    # Then, if TURN ^ VAL == 0b11, VAL is 'W'
    # Else if TURN ^ VAL == 0b00, VAL is 'B'
    # Finally, if TURN ^ VAL == 0b10, VAL is ' '.

        
################################################################################
# Basic functions - to be converted to class methods later
################################################################################

# BOARD EXAMPLE (N = 4)
# ---------
# | | | | |
# ---------
# | |W|B| |
# ---------
# | |B|W| |
# ---------
# | | | | |
# ---------
# White locations at start: [1, 1], [2, 2]
# Black locations at start: [1, 2], [2, 1]
# White formulae: [N/2 - 1, N/2 - 1], [N/2, N/2]
# Black formulae: [N/2 - 1, N/2], [N/2, N/2 - 1]

def print_board(board):
    n = len(board[0])
    dashes = ''
    for i in range(2 * n + 1):
        dashes += '-'
    print dashes
    for i in range(n):
        line = '|'
        for j in range(n):
            line += board[i][j]
            line += '|'
        print line
        print dashes
            
################################################################################
# global stuff for testing
################################################################################

# N = 4
# BOARD = []

# for i in range(N):
#     BOARD.append([ ' ' for j in range(N) ])

# for i in range(N):
#     for j in range(N):
#         if ((i, j) == (N / 2 - 1, N / 2 - 1) or
#             (i, j) == (N / 2, N / 2)):
#             BOARD[i][j] = 'W'
#         if ((i, j) == (N / 2 - 1, N / 2) or
#             (i, j) == (N / 2, N / 2 - 1)):
#             BOARD[i][j] = 'B'

# def get_bv(char):
#     if char == ' ':
#         return 0b11
#     elif char == 'W':
#         return 0b10
#     else:
#         return 0b01

# def get_cv(bit):
#     if bit == 0b11:
#         return ' '
#     elif bit == 0b10:
#         return 'W'
#     else:
#         return 'B'

# ### gets num bits in bitstring
# def get_cardinality_bits(bs):
#     c = 0
#     while bs:
#         c += 1
#         bs >>= 1
#     return c
# ### probably don't need


# ### get individual values from bitstring in the form of a list. 
# def slice_bits(bs, n):
#     l = []
#     for i in range(1, n + 1):
#         num = (bs >> 2 * (n - i)) % 4 
#         l.append(num)
#     return l


# ### get char values from bits; expects a list of 0b values; returns list of
# ### chars. Probably won't use except for testing. 
# def get_chars(bs):
#     l = []
#     for val in bs:
#         l.append(get_cv(val))
#     return l

################################################################################
# end global testing region
################################################################################

# Is there a way we can use a 0b value to represent the board?
# What if we used 11, 10, 01 to represent the values? Then, we only might
# ever have to worry about the leading 0, which can be checked by seeing the
# magnitude of the value.

# EXAMPLE: ' ' = 11, 'W' = 10, 'B' = 01

# BOARD EXAMPLE (N = 4)
# ---------
# | | |W| | => 0b 11 11 10 11
# ---------
# |B|B|W| | => 0b 01 01 10 11
# ---------
# | |B|W| | => 0b 11 01 10 11
# ---------
# | | |B|W| => 0b 11 11 01 10
# ---------

# To build our bitstring for each row:
#  - Start with value 0b00

#  1) OR with "bit value" of character in [row][col]
#  2) shift acc left by 2 `acc << 2`
#  3) return to step 1 if we don't need to start a new row

if __name__ == '__main__':
    test_board = [[ 'W', 'B', ' ', ' '],
                  [ 'B', 'B', 'W', 'W'],
                  [ ' ', 'W', ' ', ' '],
                  [ 'B', ' ', ' ', 'W']]

    bin_board = Bitstring(test_board)

    for row in bin_board.bin_board:
        # print str(bin(row))
        print bin_board.slice_bits(row)

    print "Bin val of board at [1, 2]: ", bin_board.get_bits_at([1, 2])
    # Should equal 'W' = 0b10 = 2
    print "Bin val of board at [3, 3]: ", bin_board.get_bits_at([3, 3])
    # Should equal 'W' = 0b10 = 2

    for i in range(4):
        acc = []
        for j in range(4):
            acc.append(bin_board.get_bits_at([i, j]))
        print acc
