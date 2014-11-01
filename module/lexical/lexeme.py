from types import *

class Lexeme:
    def __init__(self,type,token=None):
        self.type = type
        self.word = token

    def __print__(self):
        if self.word:
            return self.type + ' ' + str(self.word)
        else:
            return self.type

    def __str__(self):
        return self.__print__()

