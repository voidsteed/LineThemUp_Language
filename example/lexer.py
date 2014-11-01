from lexeme import *

class Lexer:
    def __init__(self, filename):
        self._file = open(filename,'r')
        self._pushedBack = False
        self._pushedBackChar = ''
    
    def lex(self):
        self._skipWhiteSpace()
        char = self._getNextChar()
        if char == 'EndOfFile':
            return Lexeme(ENDofINPUT)
        #check for symbol characters
        elif char == '(':
            return Lexeme(OPAREN)
        elif char == ')':
            return Lexeme(CPAREN)
        elif char == ',':
            return Lexeme(COMMA)
        elif char == '+':
            return Lexeme(PLUS)
        elif char == '*':
            return Lexeme(TIMES)
        elif char == '-':
            return Lexeme(MINUS)
        elif char == '/':
            return Lexeme(DIVIDEDBY)
        elif char == '<':
            return Lexeme(LESSTHAN)
        elif char == '>':
            return Lexeme(GREATERTHAN)
        elif char == '=':
            return Lexeme(EQUAL)
        elif char == ';':
            return Lexeme(SEMICOLON)
        elif char == ':':
            return Lexeme(COLON)
        elif char == '.':
            return Lexeme(DOT)
        elif char == '%':
            return Lexeme(MOD)
        elif char == '^':
            return Lexeme(CARET)
        elif char == '[':
            return Lexeme(OBRACK)
        elif char == ']':
            return Lexeme(CBRACK)
        elif char == '{':
            return Lexeme(OBRACE)
        elif char == '}':
            return Lexeme(CBRACE)
        elif char == '!':
            return Lexeme(NOT)
        elif char.isdigit():
            return self._lexNumber(char)
        elif char.isalpha():
            return self._lexVariable(char)
        elif char == '"' or ch == "'":
            return self._lexString(char)
        else:
            return Lexeme(UNKNOWN, char)

    def _skipWhiteSpace(self):
        char = self._getNextChar()
        while (char.isspace() or char == ';'):
            if char == ';': #identifies a comment
                while char != '\n':
                    char = self._getNextChar()
            else:
                char = self._getNextChar()
        self._pushback(char)
    
    def _lexNumber(self,char):
        #accumulates an integer or a real
        token = char
        flagOfReal = False
        char = self._getNextChar()
        while (char.isdigit() or char == '.'):
            if char == '.':
                flagOfReal = True
            token += char
            char = self._getNextChar()
        self._pushback(char)
        if flagOfReal:
            return Lexeme(REAL, float(token))
        else:
            return Lexeme(INTEGER, int(token))

    def _lexVariable(self,char):
        #accumulates a variable or a keyword
        token = char
        char = self._getNextChar()
        while ((ch != "EndOfFile") and (ch.isalpha() or ch.isdigit() or ch == "_")):
            token += char
            char = self._getNextChar()
        self._pushback(char)
        if self._isKeyword(token):
            return Lexeme(token.upper())
        else:
            return Lexeme(VARIABLE, token)

    def _isKeyword(self,token):
        if (token == "def" or token == "if" or token == "elif" or token == "else" or token == "while" or token == "for" or token == "not" ortoken == "class" or token == "and" or token == "or"):
            return True
        return False

    def _lexString(self,char):
        #accumulates a string
        delimiter = char
        string = ''
        char = self._getNextChar()
        while ((char != "EndOfFile") and (char != delimiter)):
            string += char
            char = self._getNextChar()
        if char == "EndOfFile":
            self._pushback(char)
        return Lexeme(STRING, token)

    def _pushback(self,char):
        #stores the last character read so that it isn't lost when going to the next token
        self._pushedBackChar = char
        self._pushedBack = True

    def _getNextChar(self):
        if self._pushedBack:
            self._pushedBack = False
            return self._pushedBackChar
        else:
            char = self._file.read(1)
            if (char or char == "0"):
                return char
            else:
                #ch is empty, indicates end of file
                return "EndOfFile"

