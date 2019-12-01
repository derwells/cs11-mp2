import pyglet
from modules import trie
from random import randint
from math import sqrt


class Engine():
	"""This class handles the game logic. 
	
	Generates a random grid of letters and, aided by the :class:`.Trie` object, calculates all
	possible words aided by the :class:`.Trie` object  as well as storing other game-related 
	information such as the maximum possible words and the current score of the player. It is called 
	by the :class:`.Interface` object on game runtime. Throughout the whole instance of the game, only
	one :class:`.Engine` instance will be used, and is therefore should not be called upon 
	directly by the main method. Code for :class:`Engine` and :class:`Trie` were modified 
	and are sourced from: https://github.com/macallmcqueen/boggle-solver-using-trie.git.

	Attributes:
		trie (Trie): The word trie formed by the current board configuartions.
		max_score (int): The maximum possible score given possible words.
		curr_score (int): The current score of game state.
		game_board_size (int): The dimensions of the current board. Has two possible values: 4 and 5.
		game_board (list): A two-dimensional array of characters representing the current game board.
		game_solutions (set): The set of all calculated possible words given a board and the dictionary of words.
		game_answered (list): The list of correct answered so far in a game state.
	"""
	

	def __init__(self):
		"""Constructor method"""

		self.trie = trie.Trie()
		self.trie.add_to_trie(open("resources/data/dictionary.txt", "r").read().split("\n"))
		self.max_score = 0
		self.curr_score = 0
		self.game_board_size = 0
		self.game_board = []
		self.game_solutions = set()
		self.game_answered = []

	def make_board(self, size):
		"""Creates NxN letter array and sets it to :attr:`.game_board` 
		
		Args:
			size (int): Represents N in an NxN board. Picked by user in :class:`.Inteface`.
		
		Returns:
			no value
		"""

		self.game_board_size = size
		self.game_board = []
		self.max_score = 0
		self.curr_score = 0

		letter_cubes = [
			"AACIOT",
			"ABILTY",
			"ABJMO$",
			"ACDEMP",
			"ACELRS",
			"ADENVZ",
			"AHMORS",
			"BIFORX",
			"DENOSW",
			"DKNOTU",
			"EEFHIY",
			"EGKLUY",
			"EGINTV",
			"EHINPS",
			"ELPSTU",
			"GILRUW",
			"AACIOT",
			"ABILTY",
			"ABJMO$",
			"ACDEMP",
			"ACELRS",
			"ADENVZ",
			"AHMORS",
			"BIFORX",
			"DENOSW"
		]

		row_count = 0
		row = []
		for cube in range(size*size):
			idx = randint(0,5)
			row.append(letter_cubes[cube][idx])
			row_count += 1
			if row_count == size:
				self.game_board.append(row)
				row = []
				row_count = 0
		return

	def solve_board(self):
		"""Recursive function that traverses current boggle board and
		updates :attr:`.game_solutions` with possible words.
		"""

		self.make_lower_case(self.game_board)
		for i in range(self.game_board_size):
			for j in range(self.game_board_size):
				self.game_solutions.update(self.words_from_start(self.game_board, i, j, self.trie))
		return

	def words_from_start(self, board, i, j, trie):
		"""Returns set of possible words starting from position (i,j) in the board.
		Uses Trie to verify word.

		Args:
			board (list): A two-dimensional array holding the NxN game board.
			i (int): The row index of beginning letter. 
			j (int): The column index of the beginning letter.
			trie (Trie): Dictionary Trie of the possible words given dictionary file
		
		Returns:
			solutions (set): Possible words starting from (i,j).
		"""

		solutions = set()
		stack = []
		stack.append((i, j, trie.root, board))
		adj_dist = [
			[1, 1],[-1, 1],[1, -1],[-1, -1],
			[0, 1],[1, 0],[0, -1],[-1, 0]
		]
		while len(stack) > 0:
			curr_letter = stack.pop()
			curr_node = curr_letter[2]
			for delta in adj_dist:
				dx, dy = delta
				x = min(max(curr_letter[0] + dx, 0), self.game_board_size - 1)
				y = min(max(curr_letter[1] + dy, 0), self.game_board_size - 1)
				board_copy = []
				for i in curr_letter[3]:
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
		"""Converts to lower case to avoid case-sensitivity"""

		length = self.game_board_size
		for row in range(length):
			for col in range(length):
				mat[row][col] = mat[row][col].lower()

	def points(self, word):
		"""Calculates points in a given word.

			Args:
				word (string): User answer.
			
			Returns:
				points (int): To be added to total score. Based on length of string.
		"""

		word_length = len(word)
		for letter in word:
			if letter == "$":
				word_length += 1
		if word_length <= 4:
				points = 1
		elif word_length == 5:
			points = 2
		elif word_length == 6:
			points = 3
		elif word_length == 7:
			points = 5
		elif word_length >= 8:
			points = 11 
		return points
	
	def verify(self, word):
		"""Determines if word is a valid answer.
		
		Args:
			word (string): User answer.

		Returns:
			bool
		"""

		if word in self.game_solutions and not(word in self.game_answered):
			return True
		else:
			return False