from Tkinter import *
from random import randint


class Game:
	
	board = []
	rowNumber = 0; colNumber = 0
	emptyColor = "light sea green"
	cellSize = 30

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

		#creates initial board and draws board
		self.createBoard()
		self.drawGame()

		self.initializePieces()
		self.newFallingPiece()

		#persists until user exits game
		self.root.mainloop()

	def drawGame(self):
		self.drawBackground()
		self.drawBoard()

	def drawBackground(self):
		self.canvas.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill="black")

	#creates initial board filled with emptyColor
	def createBoard(self):
		for row in range(self.rowNumber):
			currRow = []
			for col in range(self.colNumber):
				currRow.append(self.emptyColor)
			self.board.append(currRow)

	#draw board, with colors based on location in board
	def drawBoard(self):
		for row in range(self.rowNumber):
			for col in range(self.colNumber):
				self.drawCell(col, row, self.board[row][col])

	#takes in indices of board cell and draws a cell there
	def drawCell(self, x, y, color):
		#aligns x and y with position on canvas
		x = (x+1.5)*self.cellSize
		y = (y+1.5)*self.cellSize

		#draws outer border and then inner color
		self.canvas.create_rectangle(x, y, x+self.cellSize, y+self.cellSize, fill="black")
		self.canvas.create_rectangle(x+1, y+1, 
			x+self.cellSize-1, y+self.cellSize-1, 
			fill=color)

	def redrawAll():
		self.drawGame()

	def initializePieces(self):
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

	def newFallingPiece(self):
		#gets random piece and corresponding color
		random = randint(0, len(self.tetrisPieces)-1)
		randomPiece = self.tetrisPieces[random]
		color = self.tetrisPieceColors[random]

		#gets starting indices for new piece
		startX = 0
		startY = self.colNumber/2 - len(randomPiece[0])/2
		self.drawFallingPiece(randomPiece, color, startX, startY)
	
	#draws new falling piece based on boolean values of piece
	def drawFallingPiece(self, randomPiece, color, x, y):
		#draws piece
		for row in range(len(randomPiece)):
			for col in range(len(randomPiece[row])):
				if randomPiece[row][col] == True:
					self.drawCell(y+col, x+row, color)


game = Game(15, 10)


