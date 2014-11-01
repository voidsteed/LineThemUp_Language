from lexeme import *
class Lexer:
    def __init__(self,filename):
        self.file = open(filename,'r')
        self.pushedBack = False
        self.pushedBackChar = ''

    def lexNumber(self,char):
        token = char
        real = False
        char = self.getNextChar()
        while (char.isdigit() or char == '.'):
            if char == '.':
                real = True
            token += char
            char = self.getNextChar()
        self.pushBack(char)
        #check real
        if real:
            return Lexeme(REAL,token)
        else:
            return Lexeme(FLOAT,token)

    def lexVariable(self,char):
        token = char
        char = self.getNextChar()
        while ((char != "EndOfFile") and (char.isalpha() or char.isdigit() or char == "_")):
            token += char
            char.getNextChar()
        self.pushBack(char)
        #check keyword
        if self.isKeyWord(token):
            return Lexeme(token.upper())
        else:
            return Lexeme(VARIABLE,token)

    def isKeyWord(self,token):
        if (token is "def" or "return" or "if" or "else" or "while" or "for" or "class" or "not" or "or" or "and"):
            return True
        return False

    def lexString(self,char):
        delimiter = char
        str = ''
        char = self.getNextChar()
        while ((char != "EndOfFile") and (char != delimiter)):
            str += char
            char = self.getNextChar()
        if char == "EndOfFile":
            self.pushBack(char)
        return Lexeme(STRING,token)

    def skipWhiteSpace(self):
        char = self.getNextChar()
        while ';' != char or char.isspace():
            if char == ';':#it is a comment
                while char != '\n':
                    char = self.getNextChar()
            else:
                char = self.getNextChar()
        self.pushBack(char)

    def getNextChar(self):
        if self.pushedBack:
            self.pushedBack = False
            return self.pushedBackChar
        else:
            char = self.file.read(1) #read 1 character each time. Got this else idea from kaleb
            if (char or char == "0"):
                return char
            else:
                return "EndOfFile"

    def pushBack(self,char):
        self.pushedBack = True
        self.pushedBackChar = char

    def lex(self):
        self.skipWhiteSpace()
        char = self.getNextChar()
        if char == "EndOfFile":
            return Lexeme(EndOfFile)
        if char == "(":
            return Lexeme(OPAREN)
        elif char == ")":
            return Lexeme(CPAREN)
        elif char == ",":
            return Lexeme(COMMA)
        elif char == "+":
            return Lexeme(PLUS)
        elif char == "-":
            return Lexeme(MINUS)
        elif char == "*":
            return Lexeme(TIMES)
        elif char == "/":
            return Lexeme(DIVIDES)
        elif char == "<":
            return Lexeme(LESSTHAN)
        elif char == ">":
            return Lexeme(GREATERTHAN)
        elif char == "=":
            return Lexeme(ASSIGN)
        elif char == ";":
            return Lexeme(SEMICOLON)
        elif char == " ":
            return Lexeme(WHITESPACE)
        elif char == "%":
            return Lexeme(REMINDER)
        elif char == "!":
            return Lexeme(NOT)
        elif char == ".":
            return Lexeme(DOT)
        elif char == "[":
            return Lexeme(OBRACK)
        elif char == "]":
            return Lexeme(CBRACK)
        elif char == "{":
            return Lexeme(OBRACE)
        elif char == "}":
            return Lexeme(CBRACE)
        elif char == "^":
            return Lexeme(CARET)
        elif char.isDigit():
            return self.lexNumber(char)
        elif char.isLetter():
            return self.Variable(char)
        elif char == '"' or char == "'":
            return self.lexString(char)
        else:
            return Lexeme(UNKNOWN,char)
    
