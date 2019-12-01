class TrieNode:
	"""
	Represents node in Trie class.
	
	Attributes:
		value (string): Letter contained in node.
		children (list): List of TrieNodes that are children of current TrieNode.
		complete (string): 'None' if TrieNode does not complete a word. 
			Otherwise, contains completed word, which is the concatenation of all past 
		TrieNode values.
	"""

	def __init__(self, value):
		"""Constructor method"""

		self.value = value
		self.children = []
		self.complete = None

	def add(self, child):
		"""Add child to the node"""

		self.children.append(child)

	def get_child(self, value):
		"""
		Find direct child of current node with given value

		Args:
			value (string): Refer to TrieNode.

		Returns:
			child (TrieNode): If requested value is present in direct children.
			None: Value is not present
		"""

		for child in self.children:
			if child.value == value:
				return child
		return None

	def __str__(self):
		return str(self.value)


class Trie:
	"""
	Data structure that allows for faster verification of word combinations through
	a collection of TrieNodes.

	Attributes:
		root (TrieNode): Root of current trie.
		listy (list): Dictionary of words. Read from .txt file in Engine class
	"""

	def __init__(self, listy=None):
		self.root = TrieNode('')

		if listy != None:
			self.add_to_trie(listy)

	def add_to_trie(self, listy): 
		"""Adds given list of words to trie

			Args:
				listy (list): Refer to Trie class.
		"""

		for word in listy:
			current_node = self.root
			for letter in list(word): 
				next_node = current_node.get_child(letter)
				if next_node == None:
					next_node = TrieNode(letter)
					current_node.add(next_node)
				current_node = next_node
			current_node.complete = word