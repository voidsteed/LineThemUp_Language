from types import *

class Lexeme:
    def __init__(self,type,token=None,left=None,right=None):
        self.type = type
        self.word = token
        self.left = left
        self.right = right

    def __repr__(self):
        if self.word:
            return self.type + ' ' + str(self.word)
        else:
            return self.type

    def __eq__(self,other):
        if other:
            return self.word == other.word and self.type == other.type
        return False

    def __str__(self):
        return self.__repr__()

