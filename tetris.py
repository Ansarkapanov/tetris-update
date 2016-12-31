from Tkinter import *
from random import randint


class Game:

	#variables for board design
	board = []
	rowNumber = 0; colNumber = 0
	emptyColor = "light sea green"
	cellSize = 30

	tetrisPieces = []
	tetrisPieceColors = []
	isGameOver = False
	score = 0

	#variables to keep track of falling piece
	fallingPiece = []
	fallingPieceColor = ""
	pieceX = 0; pieceY = 0

	def __init__(self, rowNumber, colNumber):
		self.rowNumber = rowNumber
		self.colNumber = colNumber

		#creates root
		self.root = Tk()
		self.root.resizable(width=0, height=0)

		#creates canvas
		self.canvasWidth = self.cellSize*(self.colNumber+3)
		self.canvasHeight = self.cellSize*(self.rowNumber+3)
		self.canvas = Canvas(self.root, width=self.canvasWidth, height=self.canvasHeight)
		self.canvas.pack()

		#creates initial board, draws board, initializes pieces
		self.createBoardAndPieces()
		self.drawGame()

		#creates new falling piece
		self.newFallingPiece()

		self.drop()

		self.root.bind("<Key>", self.keyPressed)
		#persists until user exits game
		self.root.mainloop()

	#clears canvas and draws game
	def redrawAll(self):
		#erase existing items
		self.canvas.delete(ALL)
		self.drawGame()

	#initial method to draw an empty game and board
	def drawGame(self):
		self.drawBackground()
		self.drawBoard()

	#creates the background
	def drawBackground(self):
		self.canvas.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill="black")

	#creates initial board filled with emptyColor, initializes pieces
	def createBoardAndPieces(self):
		for row in range(self.rowNumber):
			currRow = []
			for col in range(self.colNumber):
				currRow.append(self.emptyColor)
			self.board.append(currRow)

		#initializes pieces and colors
		iPiece = [
			[ True,  True,  True,  True]
		]

		jPiece = [
			[ True, False, False ],
			[ True, True,  True]
		]

		lPiece = [
			[ False, False, True],
			[ True,  True,  True]
		]

		oPiece = [
			[ True, True],
			[ True, True]
		]

		sPiece = [
			[ False, True, True],
			[ True,  True, False ]
		]

		tPiece = [
			[ False, True, False ],
			[ True,  True, True]
		]

		zPiece = [
			[ True,  True, False ],
			[ False, True, True]
		]
		self.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
		self.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]

	#draw board, with colors based on location in board
	def drawBoard(self):
		for row in range(self.rowNumber):
			for col in range(self.colNumber):
				self.drawCell(col, row, self.board[row][col])

	#takes in position and draws a cell on the board at the indices
	def drawCell(self, x, y, color):
		#aligns x and y with position on canvas
		x = (x+1.5)*self.cellSize
		y = (y+1.5)*self.cellSize

		#draws outer border and then inner color
		self.canvas.create_rectangle(x, y, x+self.cellSize, y+self.cellSize, fill="black")
		self.canvas.create_rectangle(x+1, y+1, 
			x+self.cellSize-1, y+self.cellSize-1, 
			fill=color)

	#picks random falling pieces
	def newFallingPiece(self):
		#gets random piece and corresponding color
		random = randint(0, len(self.tetrisPieces)-1)
		self.fallingPiece = self.tetrisPieces[random]
		self.fallingPieceColor = self.tetrisPieceColors[random]

		#gets starting cells for new piece
		self.pieceY = self.colNumber/2 - len(self.fallingPiece[0])/2
		self.pieceX = 0
		self.redrawAll()
		self.drawFallingPiece()
	
	#draws new falling piece based on boolean values of piece
	def drawFallingPiece(self):
		#draws piece
		for row in range(len(self.fallingPiece)):
			for col in range(len(self.fallingPiece[row])):
				if self.fallingPiece[row][col] == True:
					self.drawCell(self.pieceY+col, self.pieceX+row, self.fallingPieceColor)

	#moves falling piece if move is legal, redraws and draws falling piece again
	def moveFallingPiece(self, drow, dcol):
		if self.moveIsLegal(self.fallingPiece, self.pieceX+drow, self.pieceY+dcol):
			self.pieceX += drow
			self.pieceY += dcol
			#redraws moved piece and board
			self.redrawAll()
			self.drawFallingPiece()
			return True
		return False
	
	#checks if move is legal
	def moveIsLegal(self, piece, x, y):
		#checks piece at x, y for legal move
		for row in range(len(piece)):
			for col in range(len(piece[row])):
				#checks if move out of range of canvas
				if x+row not in range(self.rowNumber) or y+col not in range(self.colNumber):
					return False
				#checks if board filled at that position
				if piece[row][col] == True and self.board[x+row][y+col] != self.emptyColor:
					return False
		return True

	def rotateFallingPiece(self):
		testPiece = zip(*self.fallingPiece[::-1])
		if self.moveIsLegal(testPiece, self.pieceX, self.pieceY):
			self.fallingPiece = testPiece
			self.redrawAll()
			self.drawFallingPiece()

	def drop(self):
		delay = 500
		#if piece cannot move down further, place on board
		if not self.moveFallingPiece(1, 0):
			self.placeFallingPiece()
			self.newFallingPiece()
			#if new falling piece immediately illegal
			if not self.moveIsLegal(self.fallingPiece, self.pieceX, self.pieceY):
				self.isGameOver = True
				#create replay screen
				self.gameOver()
				return
		self.canvas.after(delay, self.drop)

	#changes board to include piece
	def placeFallingPiece(self):
		for row in range(len(self.fallingPiece)):
			for col in range(len(self.fallingPiece[row])):
				if self.fallingPiece[row][col] == True:
					self.board[self.pieceX+row][self.pieceY+col] = self.fallingPieceColor
		#remove full rows

	#
	def removeFullRows(self):
		

	def gameOver(self):
		pass

	#keyboard commands
	def keyPressed(self, event):
		if canvas.data.isGameOver == True:
			if event.char == "r":
				canvas.delete(ALL)
		else:		
			if event.keysym == 'Left':
				self.moveFallingPiece(0, -1)
			elif event.keysym == 'Down':
				self.moveFallingPiece(1, 0)
			elif event.keysym == 'Right':
				self.moveFallingPiece(0, 1)
			elif event.keysym == 'Up':
				self.rotateFallingPiece()

game = Game(15, 10)

