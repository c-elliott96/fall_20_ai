# RandomOthelloPayer
#
# Makes random, valid move. Returns [row, col] move or None if it cannot make
#   a move. 

import random
import resource

def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

class RandomOthelloPlayer:
    def __init__(self, board_size, board_state, turn, time_left=9999,
                 opponent_time_left=9999):
        # @param board_size : int N
        # @param board_state : [['B', 'W', ' ', ...]
        #                       [' ', 'W', 'B', ...]
        #                       [' ', ' ', ' ', ...]]
        # @param turn : 'W' or 'B'
        # @param time_left : int in milliseconds of OUR move
        # @param opponent_time_left : same as above but OPPONENT move

        self.board_size = board_size
        self.board_state = board_state
        self.turn = turn
        self.time_left = time_left
        self.opponent_time_left = opponent_time_left

    def update_board(self, board_state):
        self.board_state = board_state
        return 

    def move_on_board(self, move):
        return (move[0] >= 0 and move[0] < self.board_size and
                move[1] >= 0 and move[1] < self.board_size)
    
    def check_valid_move(self, move, player):
        # @param move : [row, col]
        # @param player : 'W' or 'B'

        directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
        # the above represents moves in the following order respectively:
        #   E, SE, S, SW, W, NW, N, NE
        
        if self.board_state[move[0]][move[1]] != ' ' or not self.move_on_board(move):
            return False

        if player == 'B':
            other_player = 'W'
        else:
            other_player = 'B'

        spaces_to_flip = []
        for x_dir, y_dir in directions:
            x, y = move[0], move[1]
            x += x_dir
            y += y_dir
            
            if self.move_on_board([x, y]) and self.board_state[x][y] == other_player:
                # There is a piece belonging to the other player
                # next to ours
                x += x_dir
                y += y_dir
                if not self.move_on_board([x, y]):
                    continue
                
                while self.board_state[x][y] == other_player:
                    x += x_dir
                    y += y_dir
                    if not self.move_on_board([x, y]):
                        break

                if not self.move_on_board([x, y]):
                    continue

                if self.board_state[x][y] == player:
                    # There are pieces to flip. Reverse until we hit move,
                    # adding each to spaces_to_flip
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
        n = len(self.board_state[0])
        x_choice = random.randrange(n)
        y_choice = random.randrange(n)
        
        move = self.check_valid_move([x_choice, y_choice], player)
        bad_moves = []
        while not move:            
            bad_moves.append([x_choice, y_choice])
            if len(bad_moves) >= n * n:
                return None

            while ([x_choice, y_choice] in bad_moves):
                x_choice = random.randrange(n)
                y_choice = random.randrange(n)
            move = self.check_valid_move([x_choice, y_choice], player)
        move.append([x_choice, y_choice])
        # return move
        return [x_choice, y_choice]
    

def pretty_print_board(board):
    n = len(board[0])
    board_string = ''
    dashes = ''
    for i in range(2 * n + 1):
        dashes += '-'

    for row in board:
        board_string += dashes + '\n'
        for col in row:
            board_string += '|'
            board_string += col
        board_string += '|' + '\n'
    board_string += dashes + '\n'
    print board_string            

def is_game_over(board, players, rand_bot):
    # returns true if both player_1 and player_2 cannot make a play
    player_1 = players[0]
    player_2 = players[1]
    if not (rand_bot.make_random_move(player_1) and
            rand_bot.make_random_move(player_2)):
        return True
    return False

def run_game():
    board = []

    ###############################################
    # Set up new board
    ###############################################
    for row in range(0, n):
        board.append([ ' ' for col in range(0, n)])
    for row in range(n):
        for col in range(n):
            if ((row == n / 2 and col == n / 2) or
                (row == n / 2 - 1 and col == n / 2 - 1)):
                # bottom right or top left start value
                board[row][col] = 'W'
            elif ((row == n / 2 and col == n / 2 - 1) or
                  (row == n / 2 - 1 and col == n / 2)):
                board[row][col] = 'B'
    ###############################################

    pretty_print_board(board)

    ###############################################
    # Game loop - to be moved to main later
    ###############################################
    player_1 = 'W'
    player_2 = 'B'
    player = player_2
    
    rand_bot = RandomOthelloPlayer(n, board, player)
    while not is_game_over(board, (player_1, player_2), rand_bot):
        # t = raw_input("Y to continue, Q to quit: ")
        # if t == 'Q':
        #     break

        t0 = gettime()
        
        if player == player_1:
            move = rand_bot.make_random_move(player_1)
            if not move:
                player = player_2
                continue
            else:
                # update board with move
                for val in move:
                    board[val[0]][val[1]] = player
        else:
            move = rand_bot.make_random_move(player_2)
            if not move:
                player = player_1
                continue
            else:
                for val in move:
                    board[val[0]][val[1]] = player
        player = player_2 if player == player_1 else player_1
        pretty_print_board(board)

        t1 = gettime()
        print "Round time:", t1 - t0
    ###############################################

    white_total = 0
    black_total = 0
    for row in board:
        for col in row:
             if col == 'W':
                 white_total += 1
             if col == 'B':
                 black_total += 1
            
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
        print "ERROR: Give me an even n: "
        n = input()

    times = []
    for i in range(100):
        times.append(run_game())

    avg_time = 0.0
    for val in times:
        avg_time += val

    print "Average runtime over 100 games: ", avg_time / 100
