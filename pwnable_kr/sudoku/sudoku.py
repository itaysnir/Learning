import struct
import socket
import json
import ast


IP = 'pwnable.kr'
PORT = 9016
CHUNK = 2048


def setData (data):
	gameBoard = []
	ruledNumbers = []
	ruledSum = 0
	ruledOperation = ''
	data = data.split('\n')
	
	for i in range (len(data)):
		if data[i]=='':
			continue
		elif data[i][0] == '[':
			gameBoard.append (ast.literal_eval(data[i]))
		elif data[i][0] == '(':
			ruledNumbers.append (ast.literal_eval(data[i].split(':')[1][1:]))
		elif data[i].startswith('sum'):
			ruledSum = int(data[i].split(' ')[-1])
			ruledOperation = data[i].split(' ')[-3]

	return gameBoard, ruledNumbers, ruledSum, ruledOperation

# For backtracking, need to first find a candidate location
def findEmpty (board):

	# Remember- dimension is bigger than index by 1
	dimension = len(board)
	for i in range (dimension):
		for j in range (dimension):
			if board[i][j] == 0:
				return (i,j)
	# Finished board
	return ('X','X')

# Need to check validity of trial move. requiered in backtracking.
def checkValidity (board, num, pos, ruledNumbers, ruledSum, ruledOperation):

	dimension = len(board)
	i_index = pos[0]
	j_index = pos[1]

	# Check row
	for index in range (dimension):
		if (board[i_index][index] == num and index != j_index):
			return False
	# Check col
	for index in range (dimension):
		if (board[index][j_index] == num and index != i_index):
			return False
	# Check square
	box_x = pos[1]//3
	box_y = pos[0]//3
	for i in range(box_y*3, box_y*3 + 3):
		for j in range(box_x * 3, box_x*3 + 3):
			if board[i][j] == num and (i,j) != pos:
				return False

	# Enters here only if legitimate
	totalSum = 0
	for num_pos in ruledNumbers:
		num_i = num_pos[0] - 1
		num_j = num_pos[1] - 1
		curNum = board[num_i][num_j]

		# Numbers werent valiated yet. cannot decide about current element
		if (num_i, num_j) != pos and curNum == 0: 
			return True
		# Incase pos is rule'd, treat it as an assigned value
		elif (num_i, num_j) == pos:
			totalSum += num
		else:
			totalSum += curNum
		
	if ruledOperation == 'smaller':
		if totalSum < ruledSum:
			return True
		else:
			return False

	if ruledOperation == 'bigger':
		if totalSum > ruledSum:
			return True
		else:
			return False

	return True

# The main backtrace algorithm
def solve (board, ruledNumbers, ruledSum, ruledOperation):

	pos = findEmpty (board)
	i_index = pos[0]
	j_index = pos[1]
	# Base recursion case
	if pos == ('X','X'):
		return True
	for num in range (1,10):
		Possible = checkValidity (board, num, pos, ruledNumbers, ruledSum, ruledOperation)
		if not Possible:
			continue
		# Update and call recursively
		else:
			board[i_index][j_index] = num
			if solve(board, ruledNumbers, ruledSum, ruledOperation):
				return True
			# Backtrack
			else:
				board[i_index][j_index] = 0

	return False

def solveRoutine (skt):
	# receive real game data
	data = skt.recv (CHUNK)
	print (data)
	(OrigGameBoard, ruledNumbers, ruledSum, ruledOperation) = setData(data)
	gameBoard = OrigGameBoard
	solve (gameBoard, ruledNumbers, ruledSum, ruledOperation)

	resultSum = 0
	for num_pos in ruledNumbers:
		num_i = num_pos[0] - 1
		num_j = num_pos[1] - 1
		curNum = gameBoard[num_i][num_j]
		resultSum += curNum
	print ("total sum: {}".format(resultSum))
	
	to_JSON = json.dumps(gameBoard) + '\n'
	skt.send (to_JSON)

	# Debug printings
	myresult = ''
	for line in to_JSON.split ('],'):
		line = line[2:]
		line = line + ']'
		if line.endswith('\n]'):
			line = line[:-1]
		line += '\n'
		myresult += line
	print (myresult)
	
	
	# receive solution response
	data = skt.recv (CHUNK)
	print (data)
	return

def main():

	s = socket.socket()
	s.connect ((IP,PORT))

	# welcome message
	data = s.recv (CHUNK)
	s.send ('\n')

	# example
	data = s.recv (CHUNK)
	s.send ('\n')

	counter = 0
	while counter < 100:
		solveRoutine (s)
		counter += 1
	
	#receive flag
	data = s.recv (CHUNK)
	print (data)
		
	return


if __name__ == '__main__':
	main()