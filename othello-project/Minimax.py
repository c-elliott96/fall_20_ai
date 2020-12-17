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

def print_utility_board(util):
	for row in util:
		print row


class Minimax:
	def __init__(self, board_size, board_state, turn, time_left=100000, opponent_time_left=100000):
		self.board_size = board_size
		self.board_state = board_state
		self.turn = turn
		self.time_left = time_left
		self.opponent_time_left = opponent_time_left


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
		for row in board_state:
			for col in row:
				if col == turn:
					my_piece_count += 1
				if col == other_player:
					opponent_piece_count += 1
		return my_piece_count - opponent_piece_count

	
	def utility_square(self, board_state, turn):
		n = len(board_state[0])
		CORNER = 50
		WALL = -10
		INNER = -20
		OTHER = 0

		utility_board = []
		for row in range(0, n):
			utility_board.append([ 0 for col in range(0, n) ])
		# build square board
		for i in range(n):
			for j in range(n):
				# corner pieces
				if ((i == 0 and j == 0) or (i == n - 1 and j == 0) or 
					(i == n - 1 and j == n - 1) or (i == 0 and j == n - 1)):
					utility_board[i][j] = CORNER

				elif ((i == 1 and j == 0) or (i == 0 and j == 1) or 
								 (i == n - 2 and j == 0) or (i == n - 1 and j == 1) or 
								 (i == n - 1 and j == n - 2) or (i == n - 2 and j == n - 1) or 
								 (i == 0 and j == n - 2) or (i == 1 and j == n - 1)):
					utility_board[i][j] = WALL

				elif ((i == 1 and j == 1) or (i == 1 and j == n - 2) or 
								 (i == n - 2 and j == 2) or (i == n - 2 and j == n - 2)):
					utility_board[i][j] = INNER

				else:
					utility_board[i][j] = OTHER

		sum = 0
		for i in range(n):
			for j in range(n):
				if board_state[i][j] == turn:
					sum += utility_board[i][j]

		return sum


	def minimax(self, board_state, move, depth, alpha, beta, 
							maximizingPlayer, turn):
		if depth == 0 or not self.get_valid_moves(board_state, turn):
			v = self.eval_by_num_pieces(board_state, turn)
			return v

		if maximizingPlayer:
			maxEval = -100000
			for child in self.get_valid_moves(board_state, turn='B'):
				new_board_state = self.result(child, board_state, 'B')
				sub_eval = self.minimax(new_board_state, child, depth - 1, 
					alpha=None, beta=None, maximizingPlayer=False, turn='W')
				maxEval = max(maxEval, sub_eval)
			return maxEval

		else:
			minEval = 100000
			for child in self.get_valid_moves(board_state, turn='W'):
				new_board_state = self.result(child, board_state, 'W')
				sub_eval = self.minimax(new_board_state, child, depth - 1, 
					alpha=None, beta=None, maximizingPlayer=True, turn='B')
				minEval = min(minEval, sub_eval)
			return minEval

	
	def minimax_ab(self, board_state, move, depth, alpha, beta, 
								 maximizingPlayer, turn):

		# print "Depth: ", depth

		if depth == 0 or not self.get_valid_moves(board_state, turn):
			# v = self.eval_by_num_pieces(board_state, turn)

			# print "Exiting recursion ... evaluating: "
			# print_board(board_state)

			v = self.utility_square(board_state, turn)

			# print "Which has an evaluation of: ", v

			return v

		if maximizingPlayer:
			maxEval = -100000

			# print "MAXIMIZING :"
			# print_board(board_state)

			for child in self.get_valid_moves(board_state, turn='B'):
				new_board_state = self.result(child, board_state, 'B')
				sub_eval = self.minimax_ab(new_board_state, child, depth - 1, alpha, beta, 
					maximizingPlayer=False, turn='W')

				maxEval = max(maxEval, sub_eval)
				alpha = max(alpha, sub_eval)
				if beta <= alpha:
					break;
			return maxEval

		else:
			minEval = 100000
			for child in self.get_valid_moves(board_state, turn='W'):
				new_board_state = self.result(child, board_state, 'W')
				sub_eval = self.minimax_ab(new_board_state, child, depth - 1, alpha, beta, 
					maximizingPlayer=True, turn='B')

				minEval = min(minEval, sub_eval)
				beta = min(sub_eval, beta)
				if beta <= alpha:
					break;
			return minEval


	def pick_move(self, possible_moves):
		best_move_list = []
		best_val = -100000

		# print "possible moves: "
		# print possible_moves

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
		# print "Num of possible moves: ", len(possible_moves)

		for move in possible_moves:
			print ("----- MOVE %d -----" % move_num)

			t1 = gettime()

			# move_evals.append((move, self.minimax(board_state, move, DEPTH, 
			# 	alpha=None, beta=None, maximizingPlayer=True, turn='B')))

			e = self.minimax_ab(board_state, move, DEPTH, alpha=-100000, beta=100000, 
													maximizingPlayer=True, turn=turn)
			# print "Move: %s evaluation: %d" % (str(move), e)
			move_evals.append((move, e))

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


	def get_move_2(self, board_size, board_state, turn, time_left=100000, opponent_time_left=100000):
		DEPTH = 14
		moves = self.get_valid_moves(board_state, turn)
		if not moves: return None

		move_evals = []
		for move in moves:
			new_board_state = self.result(move, board_state, turn)
			e = self.minimax_ab(new_board_state, move, DEPTH, alpha=-100000, beta=-100000, maximizingPlayer=True, turn=turn)
			move_evals.append((move, e))

		best_move_val = (None, -100000)

		print "Possible moves:"
		printstr = ""
		for move, val in move_evals:
			printstr += "\tMove: " + str(move) + ", Value: " + str(val) + '\n' 
		print printstr

		return self.pick_move(move_evals)


def end_game(board, games_results):
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
		games_results['B'] = games_results['B'] + 1
		
	if num_w > num_b: 
		print "White wins!"
		games_results['W'] = games_results['W'] + 1

	if num_b == num_w:
		print "It's a draw."
	return games_results


def play_games(board_size):
	games_results = { 'B': 0, 'W': 0 }

	for i in range(100):
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
		# print_board(board)

		turn = 'B'
		r_num = 0.0
		while True:
			print "=========== ROUND # %f =========" % r_num
			r_num += 0.5
			r.update_board(board) # since RandomOthelloPlayer maintains board state itself

			# t = raw_input("Continue? (Y/N) ")
			# if t == 'N' or t == 'n':
			# 	break

			if turn == 'W':
				white_move = r.make_random_move(turn)

				if not white_move:
					turn = 'B'
					if not m.get_move_2(n, board, turn):
						print "Game over"
						end_game(board, games_results)
						break
					continue
				
				else:
					board = m.result(white_move, board, 'W')
					print "WHITE MOVE: ", white_move
					print_board(board)
					turn = 'B'
					continue

			else:
				black_move = m.get_move_2(n, board, turn)

				if not black_move:
					turn = 'W'
					if not r.make_random_move(turn):
						print "Game over"
						end_game(board, games_results)
						break
					continue

				else:
					board = m.result(black_move, board, 'B')
					print "BLACK MOVE: ", black_move
					print_board(board)
					turn = 'W'
					continue
			
	print games_results


if __name__ == '__main__':
	play_games(6)