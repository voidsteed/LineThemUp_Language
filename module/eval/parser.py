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
def parser(filename):
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
        temp = currentLexeme
        advance()
        return temp

    def matchNoAdvance(lType):
        if not check(lType):
            raise GrammarSyntaxError(lType, currentLexeme.type)

    #Dr.Lusth reminded me through email about fucntion Def should be define, also Kaleb gave me the implement idea.
    def functionDef():
        tree = Lexeme(FUNCDEF)
        match(DEF)
        name = match(ID)
        tree.left = name
        match(OPAREN)
        con = Lexeme(CON)
        tree.right = con
        con.left = optParamsList()
        match(CPAREN)
        con.right = block()
        return tree

    def functionDefPending():
        return check(DEF)

    def optParamsList():
        if paraListsPending():
            return paramsList()
        return None 

    def paraListsPending():
        return check(ID)

    def paramsList():
        tree = Lexeme(PARAMSLIST)
        tree.left = match(ID)
        if check(COMMA):
            match(COMMA)
            tree.right = paramsList()
        return tree

    def block():
        tree = Lexeme(BLOCK)
        match(OBRACE)
        tree.left = optStatementList()
        match(CBRACE)
        return tree

    def optStatementList():
        if statementListPending():
            return statementList()
        return None

    def statementList():
        tree = Lexeme(STATELIST)
        tree.left = statement()
        if statementListPending():
            tree.right = statementList()
        return tree

    def statementListPending():
        return statementPending()
    
    #updated the statement, it can describe function as statement
    def statement():
        tree = Lexeme(STATEMENT)
        if exprPending():
            tree.left = expr()
            tree.right = match(SEMICOLON)
        elif ifStatementPending():
            tree.left = ifStatement()
        elif whileStatementPending():
            tree.left = whileStatement()
        elif functionDefPending():
            tree.left = functionDef()#put a function def in statement, to describe my language, Dr.lusth's emailremind me and Kaleb helped me too.
        elif check(RETURN):
            tree.left = match(RETURN)
            opt = optExpr()
            tree.left.left = opt
            match(SEMICOLON)
        elif check(ASSIGN):
            tree.left = assignment()
        else:
            tree.left = match(PRINT)
            match(OPAREN)
            tree.left.left = optArgList()
            match(CPAREN)
            match(SEMICOLON)
        return tree

    def arrayDef():
        tree = match(ARRAY)
        match(OPAREN)
        tree.left = optArgList()
        match(CPAREN)
        return tree
    
    def arrayPending():
        check(ARRAY)

    def arrayIndex():
        tree = match(ARRAYINDEX)
        match(OPAREN)
        tree.left = optArgList()
        match(CPAREN)
        return tree

    def arrayIndexPending():
        check(ARRAYINDEX)

    def arraySet():
        tree = match(ARRAYSET)
        match(OPAREN)
        tree.left = optArgList()
        match(CPAREN)
        return tree

    def arrayIndexPending():
        check(ARRAYSET)
    
    def statementPending():
        return ifStatementPending() or whileStatementPending() or check(RETURN) or functionDefPending() or check(PRINT) or exprPending() or assignmentPending() or arrayPending()

    def optExpr():
        if exprPending:
            return expr()
        return None

    def expr():
        temp = primary()
        if operatorPending():
            tree = operator()
            tree.right = expr()
            tree.left = temp
            return tree
        return temp

    def exprPending():
        return primaryPending()

    def operator():
        if check(PLUS):
            return match(PLUS)
        elif check(MINUS):
            return match(MINUS)
        elif check(DIVIDEDBY):
            return match(DIVIDEDBY)
        elif check(TIMES):
            return match(TIMES)
        elif check(EXPO):
            return match(EXPO)
        elif check(GREATERTHAN):
            return match(GREATERTHAN)
        elif check(LESSTHAN):
            return match(LESSTHAN)
        elif check(MOD):
            return match(MOD)
        elif check(AND):
            return match(AND)
        elif check(OR):
            return match(OR)
        else:
            return match(EQUAL)
    
    def operatorPending():
        return check(PLUS) or check(MINUS) or check(DIVIDEDBY) or check(TIMES) or check(EXPO) or check(MOD) or check(GREATERTHAN) or check(LESSTHAN) or check(EQUAL) or check(OR) or check(AND) or check(ARRAY) or check(ARRAYINDEX) or check(ARRAYSET)
    
    def assignment():
        tree = match(ASSIGN)
        temp = match(ID)
        match(EQUAL)
        tree.left = temp
        tree.right = expr()
        match(SEMICOLON)
        return tree

    def assignmentPending():
        return check(ASSIGN)
    
    #from previous grammar and Got idea from Dr.Lusth's lecture
    def primary():
        if check(INTEGER):
            tree = match(INTEGER)
        elif check(REAL):
            tree = match(REAL)
        elif check(STRING):
            tree =  match(STRING)
        elif check(OPAREN):
            tree = Lexeme(GROUP)
            match(OPAREN)
            tree.left = expr()
            match(CPAREN)
        elif check(ARRAY):
            tree = arrayDef()
        elif check(ARRAYINDEX):
            tree = arrayIndex()
        elif check(ARRAYSET):
            tree = arraySet()
        elif check(NOT):
            tree = match(NOT)
            tree.left = primary()
        else:
            tree = varExpr()
        return tree

    def primaryPending():
        return check(INTEGER) or check(REAL) or check(STRING) or check(OPAREN) or varExprPending() or check(ARRAY) or check(ARRAYINDEX) or check(ARRAYSET) or check(NOT)

    def varExpr():
        tree = Lexeme(VAREXPR)
        tree.left = match(ID)
        if check(OPAREN):
            match(OPAREN)
            temp = optArgList()
            tree.right = temp
            match(CPAREN)
        return tree

    def varExprPending():
        return check(ID)

    def optArgList():
        if argListPending():
            return argList()
        return Lexeme(EMPTY)

    def argList():
        tree = Lexeme(ARGLIST)
        tree.left = expr()
        if check(COMMA):
            match(COMMA)
            tree.right = argList()
        return tree

    def argListPending():
        return exprPending()

    def ifStatementPending():
        return check(IF)

    def ifStatement():
        tree = match(IF)
        ifblock = Lexeme(CON)
        tree.left = ifblock
       # match(OPAREN)
        ifblock.left  = expr()
       # match(CPAREN)
        ifblock.right = block()
        opts = Lexeme(CON)
        tree.right = opts
#        opts.left = optElif()
        opts.left = optElse()
        return tree

    def optElse():
        if check(ELSE):
            tree = match(ELSE)
            tree.left = block()
            return tree

    def optInit():#Kaleb came up with this idea, and i borrowed it
        if check(EQUAL):
            tree = match(EQUAL)
            tree.left = expr()
            return tree

    def whileStatementPending():
        return check(WHILE)

    def whileStatement():
        tree = match(WHILE)
        match(OPAREN)
        tree.left = expr()
        match(CPAREN)
        tree.right = block()
        return tree

    try:
        s = statementList()	
        return s

    except GrammarSyntaxError as e:
        print('illegal') 
    #need to print the syntaxError
        print('GrammarSyntaxError: expected lexeme of type {c}, got type {l}'.format(c = e.checkType, l = e.lexType))#format form from Kaleb
        sys.exit(1)

parser(sys.argv[1])
