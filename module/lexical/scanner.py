from lexer import *
import sys

def scanner(filename):
    l = Lexer(filename)
    token = l.lex()
#read all tokens until they are all exhault
    while token.word != ENDofFILE:
        print(token)
        token = l.lex()

def main():
    scanner(sys.argv[1])
main()

    
