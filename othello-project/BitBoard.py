################################################################################
# Bitstring class - designed to do all the heavy work behind the scenes, so
# that (in theory) we can write minimax as minimally as possible.
################################################################################

import random
import resource
import RandomOthelloPlayer

def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

class BitBoard:
    def __init__(self, board):
        self.char_board = board
        self.bin_board = self.to_bin_board(board)
        self.board_size = len(board[0])

    def update_boards(self, board):
        self.char_board = board
        self.bin_board = self.to_bin_board(board)

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
            other_player = 0b10 # other player is 'W' == 0b10 == 2
        else:
            other_player = 0b01 # other player is 'B' == 0b01 == 1

        spaces_to_flip = []
        for x_dir, y_dir in directions:
            x, y = move[0], move[1]
            x += x_dir
            y += y_dir

            if self.move_on_board([x, y]) and (self.get_bits_at([x, y])
                                               == other_player):
                x += x_dir
                y += y_dir
                if not self.move_on_board([x, y]):
                    continue

                while self.get_bits_at([x, y]) == other_player:
                    x += x_dir
                    y += y_dir
                    if not self.move_on_board([x, y]):
                        break

                if not self.move_on_board([x, y]):
                    continue

                if self.get_bits_at([x, y]) == self.get_bv(player):
                    while True:
                        x -= x_dir
                        y -= y_dir
                        if x == move[0] and y == move[1]:
                            break
                        spaces_to_flip.append([x, y])

        if len(spaces_to_flip) == 0:
            return False
        
        spaces_to_flip.append(move)
        return spaces_to_flip

    
    def make_random_move(self, player):
        n = self.board_size
        x_choice = random.randrange(n)
        y_choice = random.randrange(n)

        move = self.check_valid_move([x_choice, y_choice], player)

        bad_moves = []
        while not move:
            bad_moves.append([x_choice, y_choice])
            if len(bad_moves) >= n * n:
                return False

            while ([x_choice, y_choice] in bad_moves):
                x_choice = random.randrange(n)
                y_choice = random.randrange(n)

            move = self.check_valid_move([x_choice, y_choice], player)
        move.append([x_choice, y_choice])
        return move    
        
        
    
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

def is_game_over(board, players, bot_1, bot_2):
    player_1 = players[0]
    player_2 = players[1]
    if not (bot_1.make_random_move(player_1) and
            bot_2.make_random_move(player_2)):
        return True
    return False

def run_game():
    ##############################################
    # Set up new board
    ##############################################
    board = []
    for row in range(n):
        board.append([' ' for col in range(n)])
    for row in range(n):
        for col in range(n):
            if ((row == n / 2 and col == n / 2) or
                (row == n / 2 - 1 and col == n / 2 - 1)):
                board[row][col] = 'W'
            elif ((row == n / 2 and col == n / 2 - 1) or
                  (row == n / 2 - 1 and col == n / 2)):
                board[row][col] = 'B'

    print_board(board)

    player_1 = 'W'
    player_2 = 'B'
    player = player_2

    # rand_bot = RandomOthelloPlayer(n, board, player_2)
    bot_1 = BitBoard(board)
    bot_2 = BitBoard(board)

    while not is_game_over(board, (player_1, player_2), bot_1, bot_2):
        # t = raw_input('Y to continue, Q to quit: ')
        # if t == 'Q' or t == 'q':
        #     break

        t0 = gettime()

        if player == player_1:
            move = bot_1.make_random_move(player_1)
            if not move:
                player = player_2
                continue
            else:
                for val in move:
                    board[val[0]][val[1]] = player
        else:
            move = bot_2.make_random_move(player_2)
            if not move:
                player = player_1
                continue
            else:
                for val in move:
                    board[val[0]][val[1]] = player
        player = player_2 if player == player_1 else player_1
        print_board(board)
        bot_1.update_boards(board)
        bot_2.update_boards(board)

        t1 = gettime()
        print "Round time:", t1 - t0

    white_total = 0
    black_total = 0
    for row in board:
        for col in row:
            if col == 'W': white_total += 1
            if col == 'B': black_total += 1

    print "White total: ", white_total
    print "Black total: ", black_total
    print "~~~~~~~~~~ GAME OVER ~~~~~~~~~~"
    if white_total > black_total:
        print "~~~~~ WHITE IS THE WINNER ~~~~~"
    elif black_total > white_total:
        print "~~~~~ BLACK IS THE WINNER ~~~~~"
    else:
        print "~~~~~~~~~ IT IS A TIE ~~~~~~~~~"

    return t1 - t0
            


if __name__ == '__main__':
    n = input("Give me n: ")
    while n % 2 != 0:
        n = input("ERROR: Give me an even n: ")

    times = []
    for i in range(100):
        times.append(run_game())

    avg_time = 0.0
    for val in times:
        avg_time += val

    print "Average runtime over 100 games: ", avg_time / 100
