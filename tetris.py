from Tkinter import *
from random import randint


class Game:

	#variables for board design
	rowNumber = 15; colNumber = 10
	emptyColor = "light sea green"
	cellSize = 30

	#variables to keep track of falling piece
	fallingPiece = []
	fallingPieceColor = ""
	pieceX = 0; pieceY = 0

	#creates root
	root = Tk()
	root.resizable(width=0, height=0)

	#creates canvas
	canvasWidth = cellSize*(colNumber+3)
	canvasHeight = cellSize*(rowNumber+3)
	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.pack()

	def __init__(self):
		
		#creates initial board, draws board, initializes pieces
		self.canvas.delete(ALL)
		self.createBoardAndPieces()
		self.drawGame()

		#creates new falling piece and drops it
		self.newFallingPiece()
		self.drop()

		self.root.bind("<Key>", self.keyPressed)
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
		self.isGameOver = False
		self.score = 0

		self.board = []
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
		self.removeFullRows()

	#
	def removeFullRows(self):
		fullRows = 0
		emptyRow = [self.emptyColor]*self.colNumber

		for row in self.board:
			#checks for full rows
			if row.count(self.emptyColor) == 0:
				#deletes full rows and inserts empty row into board
				fullRows += 1
				self.board.remove(row)
				self.board.insert(0, emptyRow)

		#change score
		self.score += fullRows**2
		self.redrawAll()

	def gameOver(self):
		pass

	#keyboard commands
	def keyPressed(self, event):
		if self.isGameOver == True:
			if event.char == "r":
				self.canvas.delete(ALL)
				self.__init__()
		else:		
			if event.keysym == 'Left':
				self.moveFallingPiece(0, -1)
			elif event.keysym == 'Down':
				self.moveFallingPiece(1, 0)
			elif event.keysym == 'Right':
				self.moveFallingPiece(0, 1)
			elif event.keysym == 'Up':
				self.rotateFallingPiece()

game = Game()

