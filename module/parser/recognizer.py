#got the function definition in statement idea from Dr.Lusth and Kaleb
# also Kaleb gave me the idea about ability to nest the function definitions

from lexer import *
import sys

    #throw the exceptions if the stream is not match.
    #part of idea is from Kaleb

class GrammarSyntaxError(Exception):
    def __init__(self, t, current):
        self.checkType = t
        self.lexType = current
    def __str__(self):
        return repr(self.checkType) + ", " + repr(self.lexType)

currentLexeme = None
def recognizer(filename):
    l = Lexer(filename)
#set currentLexeme to be global to track the lexeme
    global currentLexeme
    currentLexeme = l.lex()
    #helper functions for recognizing
    def check(lType):
        return currentLexeme.type == lType

    def advance():
        global currentLexeme
        currentLexeme = l.lex()

    def match(lType):
        matchNoAdvance(lType)
        advance()

    def matchNoAdvance(lType):
        if not check(lType):
            raise GrammarSyntaxError(lType, currentLexeme.type)

    #Dr.Lusth reminded me through email about fucntion Def should be define, also Kaleb gave me the implement idea.
    def functionDef():
        match(DEF)
        match(ID)
        match(OPAREN)
        optParamsList()
        match(CPAREN)
        block()

    def functionDefPending():
        return check(DEF)

    def optParamsList():
        if paraListsPending():
            paramsList()

    def paraListsPending():
        return check(ID)

    def paramsList():
        match(ID)
        if check(COMMA):
            match(COMMA)
            paramsList()

    def block():
        match(OBRACE)
        optStatementList()
        match(CBRACE)

    def optStatementList():
        if statementListPending():
            statementList()

    def statementList():
        statement()
        if statementListPending():
            statementList()

    def statementListPending():
        return statementPending()
    
    #updated the statement, it can describe function as statement
    def statement():
        if exprPending():
            expr()
            match(SEMICOLON)
        elif ifStatementPending():
            ifStatement()
        elif whileStatementPending():
            whileStatement()
        elif forStatementPending():
            forStatement()
        elif functionDefPending():
            functionDef()#put a function def in statement, to describe my language, Dr.lusth's emailremind me and Kaleb helped me too.
        elif check(RETURN):
            match(RETURN)
            optExpr()
            match(SEMICOLON)
        else:
            match(PRINT)
            match(OPAREN)
            optExpr()
            match(CPAREN)
            match(SEMICOLON)
        
    def statementPending():
        return ifStatementPending() or whileStatementPending() or forStatementPending() or check(RETURN) or functionDefPending() or check(PRINT) or exprPending() 

    def optExpr():
        if exprPending:
            expr()

    def expr():
        primary()
        if operatorPending():
            operator()
            expr()

    def exprPending():
        return primaryPending()

    def operator():
        if check(PLUS):
            match(PLUS)
        elif check(MINUS):
            match(MINUS)
        elif check(DIVIDEDBY):
            match(DIVIDEDBY)
        elif check(TIMES):
            match(TIMES)
        elif check(EXPO):
            match(EXPO)
        elif check(GREATERTHAN):
            match(GREATERTHAN)
        elif check(LESSTHAN):
            match(LESSTHAN)
        elif check(MOD):
            match(MOD)
        else:
            match(EQUAL)

    def operatorPending():
        return check(PLUS) or check(MINUS) or check(DIVIDEDBY) or check(TIMES) or check(EXPO) or check(MOD) or check(GREATERTHAN) or check(LESSTHAN) or check(EQUAL)

    #from previous grammar and Got idea from Dr.Lusth's lecture
    def primary():
        if check(INTEGER):
            match(INTEGER)
        elif check(REAL):
            match(REAL)
        elif check(STRING):
            match(STRING)
        elif check(OPAREN):
            match(OPAREN)
            expr()
            match(CPAREN)
        else:
            varExpr()

    def primaryPending():
        return check(INTEGER) or check(REAL) or check(STRING) or check(OPAREN) or varExprPending()

    def varExpr():
        match(ID)
        if check(OPAREN):
            match(OPAREN)
            optArgList()
            match(CPAREN)

    def varExprPending():
        return check(ID)

    def optArgList():
        if argListPending():
            argList()

    def argList():
        expr()
        if check(COMMA):
            match(COMMA)
            argList()

    def argListPending():
        return exprPending()

    def ifStatementPending():
        return check(IF)

    def ifStatement():
        match(IF)
        expr()
        block()
        optElif()
        optElse()

    def optElif():
        if check(ELIF):
            match(ELIF)
            expr()
            block()

    def optElse():
        if check(ELSE):
            match(ELSE)
            block()

    def optInit():#Kaleb came up with this idea, and i borrowed it
        if check(EQUAL):
            match(EQUAL)
            expr()

    def whileStatementPending():
        return check(WHILE)

    def whileStatement():
        match(WHILE)
        expr()
        block()

    def forStatementPending():
        return check(FOR)

#check the range function if it has a ID or INTEGER inside
    def forStatement():
        match(FOR)
        match(ID)
        match(IN)
        match(RANGE)#keyword range reminded by Kaleb 
        match(OPAREN)
        if check(ID):
            match(ID)
            match(COMMA)
            if check(ID):
                match(ID)
                match(CPAREN)
                block()
            else:
                match(INTEGER)
                match(CPAREN)
                block()


        else:
            match(INTEGER)
            match(COMMA)
            if check(ID):
                match(ID)
                match(CPAREN)
                block()
            else:
                match(INTEGER)
                match(CPAREN)
                block()

    try:
        statementList()	
        print('legal')
    except GrammarSyntaxError as e:
        print('illegal') 
    #need to print the syntaxError
        print('GrammarSyntaxError: expected lexeme of type {c}, got type {l}'.format(c = e.checkType, l = e.lexType))#format form from Kaleb
        sys.exit(1)

recognizer(sys.argv[1])
