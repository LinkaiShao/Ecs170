import random
import time
import pygame
import math
from copy import deepcopy

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	

	def play(self, env, move):
		start_time = time.process_time()
		# find possible moves
		# depth is how deep we will look into the tree
		# best move is which column is the best
		bestMove = 0
		depth = 3
		bestMove = self.MiniMax(deepcopy(env),depth)
		move[:] = [bestMove]
		print("What is time ???? !!!!", time.process_time() - start_time)
	def MiniMax(self, env, depth):
		# the best move
		bestMove = 0
		# the highest value
		switch = {1:2,2:1}
		player = self.position
		bestMove = self.max_value(env,depth,player,0)[1]
		# find the best move out of all possible ones
		print("best move is !!!!!!!")
		print(bestMove)
		return bestMove
	
	def max_value(self,env,depth,player,pathPoints):
		switch = {1:2,2:1}
		if (depth == 0):
			return pathPoints,None
		# if we have alreay
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		maxScore = float('-inf')
		# no where to go
		if(len(indices) == 0):
			return pathPoints
		bestMove = None
		origPathPoints = pathPoints
		for eachMove in indices:
			pathPoints = origPathPoints + self.EvaluationFunction(env,eachMove,player)
			copyEnv = deepcopy(env)
			self.simulate_move(copyEnv,eachMove,player)
			score = 0
			# we have won
			if (self.DoesItWin(copyEnv,eachMove,player)):
				if(depth == 3):
					return float('inf'),eachMove
				else:
					pathPoints += 39
			#if(depth==3):
				#print(copyEnv)
			score = self.min_value(copyEnv,depth - 1, switch[player],pathPoints)
			#if(depth==3):
				#print("MIn returned:")
				#print(score)
			if score > maxScore:
				maxScore = score
				bestMove = eachMove
		#if(depth == 3):
			#print("BEst Move is !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			#print(bestMove)
		return maxScore,bestMove
	def min_value(self,env,depth,player,pathPoints):
		switch = {1:2,2:1}
		if (depth == 0):
			return pathPoints
		
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		minScore = float('inf')
		# no where to go
		if(len(indices) == 0):
			return pathPoints
		origPathPoints = pathPoints
		for eachMove in indices:
			pathPoints = origPathPoints - 3 * self.EvaluationFunction(env,eachMove,player)
			copyEnv = deepcopy(env)
			self.simulate_move(copyEnv,eachMove,player)
			score = 0
			if (self.DoesItWin(copyEnv,eachMove,player)):
				pathPoints -= 80
			score = self.max_value(deepcopy(env),depth - 1, switch[player],pathPoints)[0]
			if score < minScore:
				minScore = score
		return minScore
		
	def simulate_move(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
	# check whether if the player wins with this move
	def DoesItWin(self, env, move, player):
		if (env.gameOver(move,player)):
			return True
		return False
	def EvaluationFunction(self, env, move, player):
		board = env.board
		row = env.topPosition[move]
		# opposition is the opposing player
		opposition = 1
		if player == opposition:
			opposition = 2
		# determine how much threat this move has
		threat = 0
		# threat is determined by 2 things
		# 1st is the ways for you to attack and how good it is to attack at this position
		# 2nd is how much space you can attack with 
		# space means that there are more variations that we can work with 

		# vertical first
		# if there is no way for me to win vetically, then there is no vertical threat
		# how much space on top is same as move
		bottomThreat = 0
		for i in range (5-row):
			if(board[row + i + 1][move] == opposition):
				break
			bottomThreat += 1
		# whether if vertical is even possible to win with
		spaceAvailable = bottomThreat + 1 + row
		if (spaceAvailable >=4):
			threat += spaceAvailable * bottomThreat
		# horizontal
		# extend left by 3 and right by 3, if possible
		leftSpace = 0
		rightSpace = 0
		leftThreat = 0
		rightThreat = 0
		for i in range (move):
			n = board[row][move - i - 1]
			if(n == opposition):
				break
			leftSpace += 1
			if(n == player):
				leftThreat += 1
		for i in range(7 - move - 1):
			n = board[row][move + i + 1]
			if(n == opposition):
				break
			rightSpace += 1
			if(n == player):
				rightThreat += 1
		overallHorizontalSpace = leftSpace + rightSpace
		# + 1 because of my current move
		if(overallHorizontalSpace + 1 >= 4):
			threat = threat + overallHorizontalSpace + overallHorizontalSpace*(leftThreat + rightThreat)
		#left diagonal
		#*
		# *
		#  *
		#   *
		leftUp = 0
		rightDown = 0
		leftUp = min(move,row)
		rightDown = min(6-row-1,7-move-1)
		leftupSpace = 0
		rightDownSpace = 0
		leftDiagonalThreat = 0
		for i in range(leftUp):
			n = board[row - 1 - i][move - 1 - i]
			if(n == opposition):
				break
			leftupSpace += 1
			if(n == player):
				leftDiagonalThreat += 1
		for i in range(rightDown):
			n = board[row + 1 + i][move + 1 + i]
			if(n == opposition):
				break
			rightDownSpace += 1
			if (n == player):
				leftDiagonalThreat += 1
		overallLeftDiagonalSpace = leftupSpace + rightDownSpace
		if(overallLeftDiagonalSpace + 1 >= 4):
			# 1 more addition of overall left diagonal space since space is also a priority
			threat = threat + overallLeftDiagonalSpace + overallLeftDiagonalSpace*(leftDiagonalThreat)
		#right diagonal
		#   *
		#  *
		# *
		#*
		rightUp = 0
		leftDown = 0
		rightUp = min(7-move-1,row)
		leftDown = min(6-row-1,move)
		rightUpSpace = 0
		leftDownSpace = 0
		rightDiagonalThreat = 0
		for i in range(rightUp):
			n = board[row - 1 - i][move + 1 + i]
			if(n == opposition):
				break
			rightUpSpace += 1
			if(n == player):
				rightDiagonalThreat += 1
		for i in range(leftDown):
			n = board[row + 1 + i][move - 1 - i]
			if(n == opposition):
				break
			leftDownSpace += 1
			if(n == player):
				rightDiagonalThreat += 1
		overallRightDiagonalSpace = rightUpSpace + leftDownSpace
		if(overallRightDiagonalSpace + 1 > 4):
			threat = threat + overallRightDiagonalSpace + overallRightDiagonalSpace * rightDiagonalThreat
		return threat			

		
		
		

class alphaBetaAI(connect4Player):

	def play(self, env, move):
		start_time = time.process_time()
		# find possible moves
		# depth is how deep we will look into the tree
		# best move is which column is the best
		bestMove = 0
		depth = 3
		bestMove = self.MiniMax(deepcopy(env),depth)
		move[:] = [bestMove]
		print("What is time ???? !!!!", time.process_time() - start_time)
	def MiniMax(self, env, depth):
		# the best move
		bestMove = 0
		# the highest value
		switch = {1:2,2:1}
		player = self.position
		bestMove = self.max_value(env,depth,player,0)[1]
		# find the best move out of all possible ones
		print("best move is !!!!!!!")
		print(bestMove)
		return bestMove
	
	def max_value(self,env,depth,player,pathPoints):
		switch = {1:2,2:1}
		if (depth == 0):
			return pathPoints,None
		# if we have alreay
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		maxScore = float('-inf')
		# no where to go
		if(len(indices) == 0):
			return pathPoints
		bestMove = None
		origPathPoints = pathPoints
		for eachMove in indices:
			pathPoints = origPathPoints + self.EvaluationFunction(env,eachMove,player)
			copyEnv = deepcopy(env)
			self.simulate_move(copyEnv,eachMove,player)
			score = 0
			# we have won
			if (self.DoesItWin(copyEnv,eachMove,player)):
				if(depth == 3):
					return float('inf'),eachMove
				else:
					pathPoints += 39
			#if(depth==3):
				#print(copyEnv)
			score = self.min_value(copyEnv,depth - 1, switch[player],pathPoints)
			#if(depth==3):
				#print("MIn returned:")
				#print(score)
			if score > maxScore:
				maxScore = score
				bestMove = eachMove
		#if(depth == 3):
			#print("BEst Move is !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			#print(bestMove)
		return maxScore,bestMove
	def min_value(self,env,depth,player,pathPoints):
		switch = {1:2,2:1}
		if (depth == 0):
			return pathPoints
		
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		minScore = float('inf')
		# no where to go
		if(len(indices) == 0):
			return pathPoints
		origPathPoints = pathPoints
		for eachMove in indices:
			pathPoints = origPathPoints - 3 * self.EvaluationFunction(env,eachMove,player)
			copyEnv = deepcopy(env)
			self.simulate_move(copyEnv,eachMove,player)
			score = 0
			if (self.DoesItWin(copyEnv,eachMove,player)):
				pathPoints -= 80
			score = self.max_value(deepcopy(env),depth - 1, switch[player],pathPoints)[0]
			if score < minScore:
				minScore = score
		return minScore
		
	def simulate_move(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
	# check whether if the player wins with this move
	def DoesItWin(self, env, move, player):
		if (env.gameOver(move,player)):
			return True
		return False
	def EvaluationFunction(self, env, move, player):
		board = env.board
		row = env.topPosition[move]
		# opposition is the opposing player
		opposition = 1
		if player == opposition:
			opposition = 2
		# determine how much threat this move has
		threat = 0
		# threat is determined by 2 things
		# 1st is the ways for you to attack and how good it is to attack at this position
		# 2nd is how much space you can attack with 
		# space means that there are more variations that we can work with 

		# vertical first
		# if there is no way for me to win vetically, then there is no vertical threat
		# how much space on top is same as move
		bottomThreat = 0
		for i in range (5-row):
			if(board[row + i + 1][move] == opposition):
				break
			bottomThreat += 1
		# whether if vertical is even possible to win with
		spaceAvailable = bottomThreat + 1 + row
		if (spaceAvailable >=4):
			threat += spaceAvailable * bottomThreat
		# horizontal
		# extend left by 3 and right by 3, if possible
		leftSpace = 0
		rightSpace = 0
		leftThreat = 0
		rightThreat = 0
		for i in range (move):
			n = board[row][move - i - 1]
			if(n == opposition):
				break
			leftSpace += 1
			if(n == player):
				leftThreat += 1
		for i in range(7 - move - 1):
			n = board[row][move + i + 1]
			if(n == opposition):
				break
			rightSpace += 1
			if(n == player):
				rightThreat += 1
		overallHorizontalSpace = leftSpace + rightSpace
		# + 1 because of my current move
		if(overallHorizontalSpace + 1 >= 4):
			threat = threat + overallHorizontalSpace + overallHorizontalSpace*(leftThreat + rightThreat)
		#left diagonal
		#*
		# *
		#  *
		#   *
		leftUp = 0
		rightDown = 0
		leftUp = min(move,row)
		rightDown = min(6-row-1,7-move-1)
		leftupSpace = 0
		rightDownSpace = 0
		leftDiagonalThreat = 0
		for i in range(leftUp):
			n = board[row - 1 - i][move - 1 - i]
			if(n == opposition):
				break
			leftupSpace += 1
			if(n == player):
				leftDiagonalThreat += 1
		for i in range(rightDown):
			n = board[row + 1 + i][move + 1 + i]
			if(n == opposition):
				break
			rightDownSpace += 1
			if (n == player):
				leftDiagonalThreat += 1
		overallLeftDiagonalSpace = leftupSpace + rightDownSpace
		if(overallLeftDiagonalSpace + 1 >= 4):
			# 1 more addition of overall left diagonal space since space is also a priority
			threat = threat + overallLeftDiagonalSpace + overallLeftDiagonalSpace*(leftDiagonalThreat)
		#right diagonal
		#   *
		#  *
		# *
		#*
		rightUp = 0
		leftDown = 0
		rightUp = min(7-move-1,row)
		leftDown = min(6-row-1,move)
		rightUpSpace = 0
		leftDownSpace = 0
		rightDiagonalThreat = 0
		for i in range(rightUp):
			n = board[row - 1 - i][move + 1 + i]
			if(n == opposition):
				break
			rightUpSpace += 1
			if(n == player):
				rightDiagonalThreat += 1
		for i in range(leftDown):
			n = board[row + 1 + i][move - 1 - i]
			if(n == opposition):
				break
			leftDownSpace += 1
			if(n == player):
				rightDiagonalThreat += 1
		overallRightDiagonalSpace = rightUpSpace + leftDownSpace
		if(overallRightDiagonalSpace + 1 > 4):
			threat = threat + overallRightDiagonalSpace + overallRightDiagonalSpace * rightDiagonalThreat
		return threat
		


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




