# We import a file containing my version of the trie tree data 
# structure, which will be particularly useful in searching for
# valid words
import my_trie
import time
from random import randint, choice
from math import sqrt

# First, we grab all the valid boggle words from the dictionary
dictionary = open("dictionary.txt", "r").read().split("\n")
alphabet = "AAAAAABBCCDDDEEEEEEEEEEEFFGGHHHHHIIIIIIJKLLLLMMNNNNNNOOOOOOOPP$RRRRRSSSSSSTTTTTTTTTUUUVVWWWXYYYZ"
adj = [[1, 1],[-1, 1], [1, -1], [-1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]]

# makes a trie out of all the words in the dictionary
trie = my_trie.Trie()
trie.add_to_trie(dictionary)


def make_board(size):
	board = []
	for i in range(0, int(size**2), size):
		board.append([choice(alphabet) for j in range(size)])
	return board


# Takes in a boggle board and returns the set
# of valid words on that boggle board
def solve_boggle(board, trie=trie):

	# # verifies that the input board is a valid N x M array
	# if not check_valid_matrix(board):
	# 	return ["invalid board"]

	make_lower_case(board)

	# the solutions will be stored in a set to eliminate duplicates
	solutions = set()

	# from each starting location on the board (every i,j coordinate),
	# we'll collect the set of valid words that begin at that location
	for i in range(len(board)):
		for j in range(len(board[0])):

			solutions.update(words_from_start(board, i, j, trie))

	solutions = list(solutions)
	convert_to_qu(solutions)
	solutions = set(solutions)

	return solutions


# Constants for indexing the tuples that contain relevant information
# about which letter we're looking at an what word we're considering
# it to be a part of as we traverse the board
ROW = 0
COL = 1
NODE = 2
GRID = 3


# Returns all the valid words that start at the given 
# i,j coordinate on the board
def words_from_start(board, i, j, trie):

	solutions = set()
	N = len(board[0])
	# stack for depth-first search
	stack = []
	# push on the coordinates of the start letter 
	# along with the root of the trie
	stack.append((i, j, trie.root, board))

	while len(stack) > 0:

		curr_letter = stack.pop()
		curr_node = curr_letter[NODE]

		# use a helper function to get all the letters to which our current
		# letter is adjacent

		# for each of these neighbors, 
		for delta in adj:
			dx, dy = delta
			x = min(max(curr_letter[ROW] + dx, 0), N - 1)
			y = min(max(curr_letter[COL] + dy, 0), N - 1)

			# copies board to avoid referencing
			board_copy = []
			for i in curr_letter[GRID]:
				row_copy = []
				for j in i:
					row_copy.append(j)
				board_copy.append(row_copy) 

			child = curr_node.get_child(board_copy[x][y])

			# if there isn't a node in the dictionary trie suggesting that
			# this letter is part of any word, we stop going down this path
			# by not pushing these current coordinates onto the stack
			if not child:
				continue

			if child.complete and len(child.complete) >= 3:
				solutions.add(child.complete)

			# essentially marks the node we just visited as visited
			board_copy[x][y] = None

			stack.append((x, y, child, board_copy))

	return solutions

# converts all the letters on the boggle board to 
# so that our input is not case sensitive
def make_lower_case(mat):

	length = len(mat[0])

	for row in range(length):
		for col in range(length):
			mat[row][col] = mat[row][col].lower()
			
def convert_to_qu(answer_list):
	for word in range(len(answer_list)):
		word_mutable = list(answer_list[word])
		if "$" in word_mutable:
			locations = [i for i, x in enumerate(word_mutable) if x == "$"]
			for idx in locations:
				if word_mutable[idx] == "$":
					word_mutable[idx] = "qu"
		answer_list[word] = ''.join(word_mutable)
	return

if __name__ == "__main__":

	# An example Boggle board

	board = [['$', 'I', 'Z', 'T'],
			 ['V', 'L', 'Y', 'S'],
			 ['H', 'N', 'A', 'C'],
			 ['I', 'R', 'T', '$']]

	# Call our solve_boggle function on the board, 
	# which returns a list of all the legal words on it
	result = solve_boggle(board)

	print(result, end - start)