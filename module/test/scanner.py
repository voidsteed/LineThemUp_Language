from lexer import *
import sys

def scanner(filename):
    l = Lexer(filename)
    token = l.lex()
    while token.type != ENDofINPUT: #read tokens until end of file
        print(token)
        token = l.lex()

def main():
    scanner(sys.argv[1])

main()
