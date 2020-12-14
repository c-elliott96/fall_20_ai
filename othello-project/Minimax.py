class Minimax:
	def __init__(self, board_size, board_state, turn, time_left, 
				 opponent_time_left):
		self.board_size = board_size
		self.board_state = board_state
		self.turn = turn
		self.time_left = time_left
		self.opponent_time_left = opponent_time_left



# Functions to consider/will be useful:
# - result(state, action): resulting state after applying action a to state s
# - terminal_test(state): tests if game has terminated
# - utility(state, player): numeric value that determines win, loss, or draw 
# 							given state and player. 



def get_move(board_size, board_state, turn, time_left, opponent_time_left):
	
	ai = Minimax(board_size, board_state, turn, time_left, opponent_time_left)
