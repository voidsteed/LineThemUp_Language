# Zergling programming language
# Lexeme data structure
# by Kaleb Williams

from types import *

class Lexeme:
	def __init__(self, type, token=None):
		self.type = type
		self.value = token
		self.delimiter = None
		self.right = None
		self.left = None 

	def __eq__(self, other):
		if other:
			#print("in lexeme comparison::::__>>>", self, other)
			return self.value == other.value and self.type == other.type
		return False

	def __repr__(self):
		if (self.value or self.value == 0):
			return self.type + ' ' + str(self.value)
		else:
			#Keyword or symbol, value is represented as "None" because it would be the same as the type, and therefore redundant.
			return self.type

	def __str__(self):
		return self.__repr__()
