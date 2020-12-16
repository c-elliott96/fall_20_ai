import copy

class Minimax:
	def __init__(self, board_size, board_state, turn, time_left=100000, opponent_time_left=100000):
		self.board_size = board_size
		self.board_state = board_state
		self.turn = turn
		self.time_left = time_left
		self.opponent_time_left = opponent_time_left

	def move_on_board(self, move):
		return (move[0] >= 0 and move[0] < self.board_size and
                move[1] >= 0 and move[1] < self.board_size)

	def z_move_on_board(self, move, board_size):
		return (move[0] >= 0 and move[0] < board_size and 
				move[1] >= 0 and move[1] < board_size)

	def check_valid_move(self, move):
		directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]

		if self.board_state[move[0]][move[1]] != ' ' or not self.move_on_board(move):
			return False

		if self.turn == 'B':
			other_player = 'W'
		else:
			other_player = 'B'

		spaces_to_flip = []
		for x_dir, y_dir in directions:
			x, y = move[0], move[1]
			x += x_dir
			y += y_dir

			if self.move_on_board([x, y]) and self.board_state[x][y] == other_player:
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

				if self.board_state[x][y] == self.turn:
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


	def z_check_valid_move(self, move, board_state, turn):
		directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		board_size = len(board_state[0])
		if board_state[move[0]][move[1]] != ' ' or not self.z_move_on_board(move, board_size):
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

			if self.z_move_on_board([x, y], board_size) and board_state[x][y] == other_player:
				x += x_dir
				y += y_dir
				if not self.z_move_on_board([x, y], board_size):
					continue

				while board_state[x][y] == other_player:
					x += x_dir
					y += y_dir
					if not self.z_move_on_board([x, y], board_size):
						break

				if not self.z_move_on_board([x, y], board_size):
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


	def get_valid_moves(self):
		valid_moves = []
		for i in range(self.board_size):
			for j in range(self.board_size):
				if self.board_state[i][j] == ' ':
					is_move = self.check_valid_move([i, j])
					if is_move: valid_moves.append([i, j])
		return valid_moves if len(valid_moves) > 0 else False


	def z_get_valid_moves(self, board_state, turn):
		valid_moves = []
		board_size = len(board_state[0])
		for i in range(board_size):
			for j in range(board_size):
				if board_state[i][j] == ' ':
					is_move = self.z_check_valid_move([i, j], board_state, turn)
					if is_move: valid_moves.append([i, j])
		return valid_moves if len(valid_moves) > 0 else False


	def result(self, move):
		flips = self.check_valid_move(move) 
		# new_board will be False (if invalid move) OR 
		# will be a list of pieces to flip after the move
		# So, set each value in flips to self.turn
		# Then return the whole board
		board = self.board_state
		for flip in flips:
			board[flip[0]][flip[1]] = self.turn

		return board

	def z_result(self, move, board_state, turn):
		new_state = copy.deepcopy(board_state)
		print id(board_state)
		print id(new_state)
		flips = self.z_check_valid_move(move, board_state, turn)
		if not flips: return False
		for flip in flips:
			new_state[flip[0]][flip[1]] = turn
		return new_state


	def eval_by_num_pieces(self, board_after_result):
		num_pieces = 0
		print "----- EVALUATING: -----"
		print_board(board_after_result)
		for row in board_after_result:
			for col in row:
				if col == self.turn:
					num_pieces += 1
		return num_pieces


	def minimax(self, call_count, board_state, move, depth, alpha, beta, maximizingPlayer, turn):
		print "Depth: ", depth
		print "Call count: ", call_count
		if depth == 0 or not self.z_get_valid_moves(board_state, turn):
			return self.eval_by_num_pieces(board_state)

		if maximizingPlayer:
			maxEval = -100000

			print_board(board_state)
			print "result of get_valid_moves ... "
			print self.z_get_valid_moves(board_state, turn='B')

			for child in self.z_get_valid_moves(board_state, turn='B'):

				print "child value in top ... ", child

				new_board_state = self.z_result(child, board_state, 'B')
				sub_eval = self.minimax(call_count + 1, new_board_state, child, depth - 1, 
					alpha=None, beta=None, maximizingPlayer=False, turn='W')
				maxEval = max(maxEval, sub_eval)
			return maxEval

		else:
			minEval = 100000

			print_board(board_state)
			print "result of get_valid_moves ... "
			print self.z_get_valid_moves(board_state, turn='W')

			for child in self.z_get_valid_moves(board_state, turn='W'):

				print "child value on bottom ... ", child

				new_board_state = self.z_result(child, board_state, 'W')
				sub_eval = self.minimax(call_count + 1, new_board_state, child, depth - 1, 
					alpha=None, beta=None, maximizingPlayer=True, turn='B')
				minEval = min(minEval, sub_eval)
			return minEval


	def get_move(self, board_size, board_state, turn, time_left=100000, 
				 opponent_time_left=100000):
		# self.board_size = board_size
		# self.board_state = board_state
		# self.turn = turn
		# self.time_left = time_left
		# self.opponent_time_left = opponent_time_left

		DEPTH = 5

		possible_moves = self.z_get_valid_moves(board_state, turn)
		if not possible_moves: 
			print ("No possible moves for player %s" % turn)
			return None

		move_evals = []
		move_num = 1
		for move in possible_moves:
			print ("----- MOVE %d -----" % move_num)
			move_evals.append((move, self.minimax(0, board_state, move, DEPTH, 
				alpha=None, beta=None, maximizingPlayer=True, turn='B')))
			move_num += 1

		best_move_val = -100000

		print "Possible moves:"
		printstr = ""
		for move, val in move_evals:
			printstr += "\tMove: " + str(move) + "Value: " + str(val) + '\n'

		print printstr


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

    print_board(board)
    m.get_move(n, board, 'B')