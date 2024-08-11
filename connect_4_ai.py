import copy
import math
import random
# we'll reverse array depending upon if its proper or no lol
# def drop_piece (cancelled)
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

def print_board(board) :
    for i in board[::-1] :
        print(i)
    print()

def get_next_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0
def get_valid_locations(board) : 
	valid_locations = []
	for col in range(COLUMN_COUNT) : 
		if is_valid_location(board,col) : 
			valid_locations.append(col)
	return valid_locations

def is_terminal_node(board) : 
	return winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or (len(get_valid_locations(board)) == 0)


def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def eval_window(window,piece) : 
	score = 0
	opp_piece = PLAYER_PIECE
	if 	piece == PLAYER_PIECE : 
		opp_piece = AI_PIECE
	if window.count(piece) == 4 : 
		score +=  100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1 : 
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2 : 
		score+=2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1 : 
		score -= 4
	return score 

def score_position(board,piece) : 
	score = 0

	## center preference 
	center_array = [i[COLUMN_COUNT//2] for i in board]
	center_count = center_array.count(piece)
	score += center_count*3


	## score horizontal
	for r in range(ROW_COUNT) : 
		row_array = [i for i in board[r]]
		for c in range(COLUMN_COUNT-3) : 
			window = row_array[c:c+WINDOW_LENGTH]
			score+=eval_window(window,piece)
	
	## score vertical
	for c in range(COLUMN_COUNT) : 
		col_array = [i[c] for i in board]
		for r in range(ROW_COUNT - 3) : 
			window = col_array[r:r+WINDOW_LENGTH]
			score+=eval_window(window,piece)

	## score +ve diag 
	for r in range(ROW_COUNT-3) : 
		for c in range(COLUMN_COUNT-3) : 
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score+=eval_window(window,piece)
	
	for r in range(ROW_COUNT-3) : 
		for c in range(COLUMN_COUNT-3) : 
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score+=eval_window(window,piece)

	
	return score
def minimax(board, depth, alpha, beta, maximizingPlayer):
  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)
  if depth == 0 or is_terminal:
    if is_terminal:
      if winning_move(board, AI_PIECE):
        return (None, 1000000000000000000)
      elif winning_move(board, AI_PIECE):
        return (None, -100000000000000000)
      else:
        ## game over
        return (None, 0)
    else:
      return (None, score_position(board, AI_PIECE))
  if maximizingPlayer:
    value = -math.inf
    column = valid_locations[0]
    for col in valid_locations:
      row = get_next_row(board, col)
      b_copy = copy.deepcopy(board[:])
      b_copy[row][col] = AI_PIECE
      new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
      if new_score > value:
        value = new_score
        column = col
      alpha = max(alpha, value)
      if alpha >= beta:
        break
    return column, value

  else:  #minimizing player
    value = math.inf
    column = valid_locations[0]
    for col in valid_locations:
      row = get_next_row(board, col)
      b_copy = copy.deepcopy(board[:])
      b_copy[row][col] = PLAYER_PIECE
      new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
      if new_score < value:
        value = new_score
        column = col
      beta = min(beta, value)
      if alpha >= beta:
        break
    return column, value
board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
turn = AI
game_over = False
print_board(board)
while not game_over:
    if turn == 0 : 
        col = int(input("Enter column : "))-1

        if is_valid_location(board, col):
            row = get_next_row(board, col)
            board[row][col] = PLAYER_PIECE
            if winning_move(board, PLAYER_PIECE):
                print("Player 1 wins!!")
                game_over = True
            turn+=1
            turn = turn % 2
            print_board(board)
    
    if turn == AI :
        col,minimax_score = minimax(board,6,-math.inf,math.inf,True)
        if is_valid_location(board, col):
            row = get_next_row(board, col)
            board[row][col] = AI_PIECE
            if winning_move(board, AI_PIECE):
                print("Player 2 wins!!")
                game_over = True
            turn += 1
            turn = turn % 2
            print_board(board)
