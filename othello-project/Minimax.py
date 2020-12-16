import copy
import random
import resource

import RandomOthelloPlayer

def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

def print_board(board):
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

class Minimax:
	def __init__(self, board_size, board_state, turn, time_left=100000, opponent_time_left=100000):
		self.board_size = board_size
		self.board_state = board_state
		self.turn = turn
		self.time_left = time_left
		self.opponent_time_left = opponent_time_left

	# def move_on_board(self, move):
	# 	return (move[0] >= 0 and move[0] < self.board_size and
  #               move[1] >= 0 and move[1] < self.board_size)

	def move_on_board(self, move, board_size):
		return (move[0] >= 0 and move[0] < board_size and 
				move[1] >= 0 and move[1] < board_size)


	def check_valid_move(self, move, board_state, turn):
		directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		board_size = len(board_state[0])
		if board_state[move[0]][move[1]] != ' ' or not self.move_on_board(move, board_size):
			return False

		if turn == 'B':
			other_player = 'W'
		else:
			other_player = 'B'

		spaces_to_flip = []
		for x_dir, y_dir in directions:
			x, y = move[0], move[1]
			x += x_dir
			y += y_dir

			if self.move_on_board([x, y], board_size) and board_state[x][y] == other_player:
				x += x_dir
				y += y_dir
				if not self.move_on_board([x, y], board_size):
					continue

				while board_state[x][y] == other_player:
					x += x_dir
					y += y_dir
					if not self.move_on_board([x, y], board_size):
						break

				if not self.move_on_board([x, y], board_size):
					continue

				if board_state[x][y] == turn:
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


	def get_valid_moves(self, board_state, turn):
		valid_moves = []
		board_size = len(board_state[0])
		for i in range(board_size):
			for j in range(board_size):
				if board_state[i][j] == ' ':
					is_move = self.check_valid_move([i, j], board_state, turn)
					if is_move: valid_moves.append([i, j])
		return valid_moves if len(valid_moves) > 0 else False


	def result(self, move, board_state, turn):
		new_state = copy.deepcopy(board_state)

		# print "calculating result for ... ", new_state
		# print "for move: ", move
		
		flips = self.check_valid_move(move, board_state, turn)
		if not flips: return None
		for flip in flips:
			new_state[flip[0]][flip[1]] = turn
		return new_state


	def eval_by_num_pieces(self, board_state, turn):
		my_piece_count = opponent_piece_count = 0
		if turn == 'B':
			other_player = 'W'
		else:
			other_player = 'B'

		# print "-EVALUATING:-"
		# print_board(board_state)

		for row in board_state:
			for col in row:
				if col == turn:
					my_piece_count += 1
				if col == other_player:
					opponent_piece_count += 1
				
		# print "Evaluation: ", (my_piece_count - opponent_piece_count)
		return my_piece_count - opponent_piece_count


	def minimax(self, board_state, move, depth, alpha, beta, 
							maximizingPlayer, turn):
		# print "Depth: ", depth
		# print "Call count: ", call_count
		if depth == 0 or not self.get_valid_moves(board_state, turn):
			v = self.eval_by_num_pieces(board_state, turn)
			print "Return evaluation value of ", v
			return v

		if maximizingPlayer:
			maxEval = -100000

			# print_board(board_state)
			# print "result of get_valid_moves ... "
			# print self.get_valid_moves(board_state, turn='B')

			for child in self.get_valid_moves(board_state, turn='B'):

				# print "child value in top ... ", child

				new_board_state = self.result(child, board_state, 'B')
				sub_eval = self.minimax(new_board_state, child, depth - 1, 
					alpha=None, beta=None, maximizingPlayer=False, turn='W')
				maxEval = max(maxEval, sub_eval)
			return maxEval

		else:
			minEval = 100000

			# print_board(board_state)
			# print "result of get_valid_moves ... "
			# print self.get_valid_moves(board_state, turn='W')

			for child in self.get_valid_moves(board_state, turn='W'):

				# print "child value on bottom ... ", child

				new_board_state = self.result(child, board_state, 'W')
				sub_eval = self.minimax(new_board_state, child, depth - 1, 
					alpha=None, beta=None, maximizingPlayer=True, turn='B')
				minEval = min(minEval, sub_eval)
			return minEval


	def pick_move(self, possible_moves):
		best_move_list = []
		best_val = -100000

		print "possible moves: "
		print possible_moves

		for move, val in possible_moves:
			best_val = max(best_val, val)

		for move, val in possible_moves:
			if val == best_val:
				best_move_list.append(move)

		if len(best_move_list) > 1:
			rand_choice = random.choice(best_move_list)
			# print "More than 1 best move... choosing randomly."
			# print "Chose ", rand_choice
			return rand_choice

		return best_move_list[0]


	def get_move(self, board_size, board_state, turn, time_left=100000, 
				 opponent_time_left=100000):

		DEPTH = 3

		# print_board(board_state)
		possible_moves = self.get_valid_moves(board_state, turn)
		if not possible_moves: 
			return None

		move_evals = []
		move_num = 1
		print "Num of possible moves: ", len(possible_moves)
		for move in possible_moves:
			print ("----- MOVE %d -----" % move_num)

			t1 = gettime()

			move_evals.append((move, self.minimax(board_state, move, DEPTH, 
				alpha=None, beta=None, maximizingPlayer=True, turn='B')))

			t2 = gettime()
			# print "Iteration time: ", (t2 - t1)

			move_num += 1

		best_move_val = (None, -100000)

		print "Possible moves:"
		printstr = ""
		for move, val in move_evals:
			printstr += "\tMove: " + str(move) + ", Value: " + str(val) + '\n'

		print printstr

		return self.pick_move(move_evals)


# ```
# MINIMAX ALGO:

# minimax(move, depth, alpha, beta, maximizingPlayer):
# 	if depth == 0 or game over in position:
# 		return static evalutation of position

# 	if maximizingPlayer:
# 		maxEval = -INF
# 		for each child of position:
# 			eval = minimax(child, depth - 1, false)
# 			maxEval = max(maxEval, eval)
# 		return maxEval

# 	else:
# 		minEval = +INF
# 		for each child of position:
# 			eval = minimax(child, depth - 1, true)
# 			minEval = min(minEval, eval)
# 		return minEval
# ```

# Functions to consider/will be useful:
# - result(state, action): resulting state after applying action a to state s
# - terminal_test(state): tests if game has terminated
# - utility(state, player): numeric value that determines win, loss, or draw 
# 							given state and player. 



# def get_move(board_size, board_state, turn, time_left, opponent_time_left):
# 	pass


def end_game(board):
	n = len(board[0])

	num_b = num_w = 0
	for i in range(n):
		for j in range(n):
			if board[i][j] == 'W':
				num_w += 1
			if board[i][j] == 'B':
				num_b += 1

	print "Score: Black: %d, White: %d" % (num_b, num_w)
	if num_b > num_w:
		print "Black wins!"
	if num_w > num_b: 
		print "White wins!"
	if num_b == num_w:
		print "It's a draw."
		



if __name__ == '__main__':


	###############################################
	# Set up new board
	###############################################
	n = 6
	board = []
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
	# Minimax(board_size, board_state, turn, time_left, opponent_time_left)
	m = Minimax(n, board, 'B')
	r = RandomOthelloPlayer.RandomOthelloPlayer(n, board, 'W')
	print "STARTING GAME"
	print_board(board)

	turn = 'B'
	while True:
		r.update_board(board) # since RandomOthelloPlayer maintains board state itself
		t = raw_input("Continue? (Y/N) ")
		if t == 'N' or t == 'n':
			break
		if turn == 'W':
			white_move = r.make_random_move(turn)

			if not white_move:
				turn = 'B'
				if not m.get_move(n, board, turn):
					print "Game over"
					end_game(board)
					break
				continue
			
			else:
				board = m.result(white_move, board, 'W')
				print "WHITE MOVE: ", white_move
				print_board(board)
				turn = 'B'
				continue

		else:
			black_move = m.get_move(n, board, turn)

			if not black_move:
				turn = 'W'
				if not r.make_random_move(turn):
					print "Game over"
					end_game(board)
					break
				continue

			else:
				board = m.result(black_move, board, 'B')
				print "BLACK MOVE: ", black_move
				print_board(board)
				turn = 'W'
				continue