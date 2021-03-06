#change something to fit new type
#got some ideas from Dr.lusth's Scanner and Kaleb's

from lexeme import *

class Lexer:
    def __init__(self, filename):
        self._file = open(filename,'r')
        self._pushed = False
        self._pushedChar = ''
    
    def lex(self):
        self._skipWhiteSpace()
        ch = self._getNextChar()
        if ch == 'EOF':
            #'EOF' is self._getNextCharacter's way of showing that it's the end of the file.
            return Lexeme(ENDofINPUT)
        #check for symbol characters
        elif ch == '(':
            return Lexeme(OPAREN,'(')
        elif ch == ')':
            return Lexeme(CPAREN,')')
        elif ch == ',':
            return Lexeme(COMMA,',')
        elif ch == '+':
            return Lexeme(PLUS,'+')
        elif ch == '*':
            return Lexeme(TIMES,'*')
        elif ch == '-':
            return Lexeme(MINUS,'-')
        elif ch == '/':
            return Lexeme(DIVIDEDBY,'/')
        elif ch == '<':
            return Lexeme(LESSTHAN,'<')
        elif ch == '>':
            return Lexeme(GREATERTHAN,'>')
        elif ch == '=':
            return Lexeme(EQUAL,'=')
        elif ch == ';':
            return Lexeme(SEMICOLON,';')
        elif ch == ':':
            return Lexeme(COLON,':')
        elif ch == '.':
            return Lexeme(DOT,'.')
        elif ch == '%':
            return Lexeme(MOD,'%')
        elif ch == '^':
            return Lexeme(EXPO,'^')
        elif ch == '?':
            return Lexeme(COMPARE,'?')
        elif ch == '[':
            return Lexeme(OBRACK,'[')
        elif ch == ']':
            return Lexeme(CBRACK,']')
        elif ch == '{':
            return Lexeme(OBRACE,'{')
        elif ch == '}':
            return Lexeme(CBRACE,'}')
        elif ch == '!':
            return Lexeme(NOT,'!')
        elif ch == '&':
            return Lexeme(AND,'&')
        elif ch == '|':
            return Lexeme(OR,'|')
        elif ch == '$':
            return Lexeme(ASSIGN,'$')
        elif ch.isdigit():
            return self._lexNumber(ch)
        elif ch.isalpha():
            return self._lexVariable(ch)
        elif ch == '"' or ch == "'":
            return self._lexString(ch)
        else:
            return Lexeme(UNKNOWN, ch)

    def _skipWhiteSpace(self):
        ch = self._getNextChar()
        while (ch.isspace() or ch == '#'):
            #use for comment
            if ch == '#': 
                while ch != '\n':
                    ch = self._getNextChar()
            else:
                ch = self._getNextChar()
        self._pushback(ch)
    
    #accumulates an integer or a real
    def _lexNumber(self,ch):
        token = ch
        real = False
        ch = self._getNextChar()
        while (ch.isdigit() or ch == '.'):
            if ch == '.':
                real = True
            token += ch
            ch = self._getNextChar()
        self._pushback(ch)
        if real:
            return Lexeme(REAL, float(token))
        else:
            return Lexeme(INTEGER, int(token))

#accumulates a variable(including key word)
    def _lexVariable(self,ch):
        token = ch
        ch = self._getNextChar()
        while ((ch != "EOF") and (ch.isalpha() or ch.isdigit() or ch == "_")):
            token += ch
            ch = self._getNextChar()
        self._pushback(ch)
        if self._isKeyword(token):
            return Lexeme(token.upper(),token)
        else:
            return Lexeme(ID, token)

    def _isKeyword(self,token):
        if (token == "def" or token == "if" or token == "else" or token == "while" or token == "and" or token == "not" or token == "or" or token == "return" or token == "print" or token == "array" or token == "arrayIndex" or token == "arraySet"):
            return True
        return False

    #accumulates a string
    def _lexString(self,ch):
        delimiter = ch
        token = ''
        ch = self._getNextChar()
        #got delimiter idea from Dr.Lusth's scanner
        while ((ch != "EOF") and (ch != delimiter)):
            token += ch
            ch = self._getNextChar()
        if ch == "EOF":
            self._pushback(ch)
        return Lexeme(STRING, token)

    def _pushback(self,ch):
        #stores the last character read so that it isn't lost when going to the next token
        self._pushedChar = ch
        self._pushed = True

    def _getNextChar(self):
        if self._pushed:
            self._pushed = False
            return self._pushedChar
        else:
            ch = self._file.read(1)
            if (ch or ch == "0"):
                return ch
            else:
                #ch is empty, indicates end of file
                return "EOF"

