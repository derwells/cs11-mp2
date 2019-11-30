# We import a file containing my version of the trie tree data 
# structure, which will be particularly useful in searching for
# valid words
import pyglet
from modules import my_trie
from random import choice
from math import sqrt

# Constants for indexing the tuples that contain relevant information
# about which letter we're looking at an what word we're considering
# it to be a part of as we traverse the board
ROW = 0
COL = 1
NODE = 2	
GRID = 3
ADJ = [[1, 1],[-1, 1], [1, -1], [-1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]]
ALPH = "AAAAAABBCCDDDEEEEEEEEEEEFFGGHHHHHIIIIIIJKLLLLMMNNNNNNOOOOOOOPP$RRRRRSSSSSSTTTTTTTTTUUUVVWWWXYYYZ"

class Engine():
	"""
	This class handles the game logic. It generates a random grid of letters and, 
	aided by the :class:`.Trie` object, calculates all possible words aided by the :class:`.Trie` object 
	as well as storing other game-related information such as the maximum possible words and the current 
	score of the player. It is called by the :class:`.Interface` object on game runtime. Throughout the 
	whole instance of the game, only one :class:`.Engine` instance will be used, and is therefore should 
	not be called upon directly by the main method.

	Attributes:
		self.trie (Trie): The word trie formed by the current board configuartions.
		self.max_score (int): The maximum possible score given possible words.
		self.curr_score (int): The current score of game state.
		self.game_board_size (int): The dimensions of the current board. Has two possible values: 4 and 5.
		self.game_board (list): A two-dimensional array of characters representing the current game board.
		self.game_solutions (set): The set of all calculated possible words given a board and the dictionary of words.
		self.game_answered (list): The list of correct answered so far in a game state.
	"""
	def __init__(self):
		self.trie = my_trie.Trie()
		self.trie.add_to_trie(open("dictionary.txt", "r").read().split("\n"))
		self.max_score = None
		self.curr_score = None
		self.game_board_size = None
		self.game_board = None
		self.game_solutions = set()
		self.game_answered = []

	def make_board(self, size):
		self.game_board_size = size
		self.max_score = 0
		self.curr_score = 0
		board = []
		for i in range(0, int(size**2), size):
			board.append([choice(ALPH) for j in range(size)])
		self.game_board = board
		return

	def solve_boggle(self):
		self.make_lower_case(self.game_board)
		for i in range(len(self.game_board)):
			for j in range(len(self.game_board[0])):
				self.game_solutions.update(self.words_from_start(self.game_board, i, j, self.trie))
		return

	def words_from_start(self, board, i, j, trie):
		solutions = set()
		stack = []
		stack.append((i, j, trie.root, board))
		while len(stack) > 0:
			curr_letter = stack.pop()
			curr_node = curr_letter[NODE]
			for delta in ADJ:
				dx, dy = delta
				x = min(max(curr_letter[ROW] + dx, 0), self.game_board_size - 1)
				y = min(max(curr_letter[COL] + dy, 0), self.game_board_size - 1)
				board_copy = []
				for i in curr_letter[GRID]:
					row_copy = []
					for j in i:
						row_copy.append(j)
					board_copy.append(row_copy) 
				child = curr_node.get_child(board_copy[x][y])
				if not child:
					continue
				if child.complete == None:
					word_length = 0
				else:
					word_length = len(child.complete)
				if child.complete and word_length >= 3:
					if not (child.complete in self.game_solutions or child.complete in solutions):
						self.max_score += self.points(child.complete)
						solutions.add(child.complete)
				board_copy[x][y] = None
				stack.append((x, y, child, board_copy))
		return solutions

	def make_lower_case(self, mat):
		length = self.game_board_size
		for row in range(length):
			for col in range(length):
				mat[row][col] = mat[row][col].lower()

	def points(self, word):
		word_length = len(word)
		for letter in word:
			if letter == "$":
				word_length += 1
		if word_length <= 4:
				score = 1
		elif word_length == 5:
			score = 2
		elif word_length == 6:
			score = 3
		elif word_length == 7:
			score = 5
		elif word_length >= 8:
			score = 11 
		return score
	
	def verify(self, word):
		if word in self.game_solutions and not(word in self.game_answered):
			return True
		else:
			return False