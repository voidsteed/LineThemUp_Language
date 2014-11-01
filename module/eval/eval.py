#Line'em Up
#Yujun Liu
#evaluator

import sys
from parser import *
from environment import *

returned = False

def evaluate(tree,env):
    if tree.type == INTEGER or tree.type == STRING or tree.type == REAL:
        return tree
    elif tree.type == ID:
        temp = lookup(tree,env)
        return temp 
    elif tree.type == PLUS or tree.type == MINUS or tree.type == TIMES or tree.type == DIVIDEDBY or tree.type == EXPO or tree.type == GREATERTHAN or tree.type == LESSTHAN or tree.type == MOD or tree.type == EQUAL or tree.type == EXPO:
        return evalOp(tree,env)
    elif tree.type == FUNCDEF:
        return evalFuncDef(tree,env)
    elif tree.type == BLOCK:
        return evalBlock(tree,env)
    elif tree.type == STATELIST:
        return evalStateList(tree,env)
    elif tree.type == STATEMENT:
        return evalStatement(tree,env)
    elif tree.type == ARGLIST:
        return evalArgs(tree,env)
    elif tree.type == VAREXPR:
        if tree.right and tree.right.type != ARRAY:
            return evalFuncCall(tree,env)
        elif tree.right== ARRAY:
            return evalArray(tree,env)
        else:
            temp = evaluate(tree.left,env)
            return temp 
    elif tree.type == NOT:
        return evalNot(tree,env)
#Kaleb told me this idea beacause when I use conditions, the complex expression should be in a group, so it can just come out a result for whole expression.
    elif tree.type == GROUP:
        return evaluate(tree.left,env)
    elif tree.type == IF:
        return evalIf(tree,env)
    elif tree.type == ELSE:
        return evalElse(tree,env)
    elif tree.type == AND or tree.type == OR:

        return evalLogicOp(tree,env)
    elif tree.type == ASSIGN:
        return evalAssign(tree,env)
    elif tree.type == WHILE:
        return evalWhile(tree,env)
    elif tree.type == ENV:
        return tree
    elif tree.type == RETURN:
        return evalReturn(tree,env)
    elif tree.type == PRINT:
        return evalPrint(tree,env)
    elif tree.type == ARRAY:
        return evalArray(tree,env)
    elif tree.type == ARRAYINDEX:
        return evalIndex(tree,env)
    elif tree.type == ARRAYSET:
        return evalSet(tree,env)
    else:
        print("************BAD EXPRESSIONS!**************",tree.type)

def evalPrint(tree,env):
    def printArgs(arg,e):
        if arg and arg.type != EMPTY:
            result = evaluate(arg.left,env)
            if result.type == ENV:
                #this is when I was doing simulator, variable sometimes pass a function, it can't be printed so this one is for printing the function. Idea from Kaleb.
                print("<function {name}>".format(name=arg.left,end=' '))
            else:
                print(evaluate(arg.left,e).word,end=' ')
                printArgs(arg.right,e)
        else:
            print()
    if tree.left.type != EMPTY:
        printArgs(tree.left,env)
        print()
    else:
        print()

def evalStateList(tree,env):
    last = evaluate(tree.left,env)
    if tree.right:
        last = evaluate(tree.right,env)
    return last

def evalStatement(tree,env):
    result = evaluate(tree.left,env)
    return result

def evalReturn(tree,env):
    global returned
    returned = True
    if tree.left:
        return evaluate(tree.left,env)
    else:
        return Lexeme(EMPTY)

def evalNot(tree,env):
    boolean = evaluate(tree.left,env)
    result = Lexeme(INTEGER)
    if boolean.word:
        result.word = 0
    else:
        result.word = 1
    return result

def evalIf(tree,env):
    boolean = evaluate(tree.left.left,env)
    
    if boolean.word:
        return evaluate(tree.left.right,env)
    elif tree.right.left:
        return evaluate(tree.right.left,env)
    else:
        return boolean

def evalElse(tree,env):
    #print("Here in ----------------------------> evalElse")
    return evaluate(tree.left,env)

def evalAssign(tree,env):
    #print("Here in ----------------------------> evalAssign")
    name = tree.left 
    #expr = evaluate(tree.right,env)
    current = lookup(name,env,True)
    if current:
        setVar(name,evaluate(tree.right,env),env)
    else:
        insert(name,evaluate(tree.right,env),env)



def evalOp(tree,env):
    #print("Here in ----------------------------> evalOp")
    #print("OPtree----------------------------->",tree)
    #print("tree.left-----XXXXXXX----------->",tree.left)
    a = evaluate(tree.left,env)
    #print("a in evalOP is ",a)
    b = evaluate(tree.right,env)
    op = tree.word
    if a.type == REAL or b.type == REAL:
        result = Lexeme(REAL)
        if op == '=':
            result.word = eval(str(a.word) + "==" + str(b.word))
        else:
            result.word = eval(str(a.word) + tree.word + str(b.word))
    elif a.type == INTEGER:
        result = Lexeme(INTEGER)
        if op == '=':
            result.word = eval(str(a.word) + "==" + str(b.word))
        else:
            result.word = eval(str(a.word) + tree.word + str(b.word))
    elif b.type == STRING:
        result = Lexeme(STRING)
        if op == '=':
            result.word = (a.word == b.word)
        elif op == '+':
            result.word = (a.word + b.word)
        else:
            print("Bad operation! String just can do plus operation.")
    else:
        #print("OPtree----------------------eval Tree.left------->",evaluate(tree.left,env))
        #print("tree--------------->",tree)
        result = Lexeme(INTEGER)
        #a = evaluate(tree.left)
        result.word = eval(str(a.word) + "==" + str(b.word))

    if result.word == False:
        result.word = 0
    elif result.word == True:
        result.word = 1
    #print("result of evalOP",result.word)
    return result

def evalLogicOp(tree,env):
    #print("Here in ----------------------------> evalLogicOp")
    #print("tree----in LogicOP--------------->",tree)
    #print("tree.left----in LogicOP--------------->",tree.left)
    a = evaluate(tree.left,env)
    #print("logic a---------------->",a.word)
    #print("logic a--type-------------->",a.type)
    result = Lexeme(INTEGER)
    if tree.type == AND:
        if not a.word:
            result.word = a.word
        else:
            result.word = (a.word and evaluate(tree.right,env).word)
    else:
        if a.word:
            result.word = a.word
        else:
            result.word = a.word or evaluate(tree.right,env).word
    #print("evalLogicOp---result----------->",result)
    return result


def evalFuncDef(tree,env):
    #print("Here in -------------------> evalFuncDef")
    closure = cons(env, cons(getFuncDefParams(tree) , getFuncDefBody(tree)))
    insert(getFuncDefName(tree), closure,env)

def getFuncDefParams(tree):
    return tree.right.left

def getFuncDefName(tree):
    return tree.left 

def getFuncDefBody(tree):
    return tree.right.right

def getFuncCallName(tree):
    return tree.left

def getFuncCallArgs(tree):
    return tree.right

def getClosureParams(closure):
    return closure.right.left

def getClosureBody(closure):
    return closure.right.right

def getClosureEnv(closure):
    return closure.left

def evalFuncCall(tree,env):
    #print("Here in ---------------------------> evalFuncCall")
    global returned
    returned = False
    closure = evaluate(getFuncCallName(tree),env)
    args = getFuncCallArgs(tree)
    params = getClosureParams(closure)
    body = getClosureBody(closure)
    senv = getClosureEnv(closure)
    eargs = evalArgs(args,env)
    xenv = extend(params,eargs,senv)
    return evaluate(body,xenv)

def evalArgs(tree,env):
    #print("Here in ---------------------------> evalArgs")
    if tree.left:
        argList = Lexeme(ARGLIST)
        newLexeme = Lexeme(tree.left.type)
        newLexeme = evaluate(tree.left,env)
        argList.left = newLexeme
        if tree.right:
            argList.right = evalArgs(tree.right,env)
        return argList
        #expr = evaluate(tree.left,env)
        #argLex.left = expr
        #if tree.right and tree.right != None:
        #    args = evaluate(tree.right,env)
        #    argLex.right = args
        #return argLex


def evalBlock(tree,env):
    #print("Here in ----------------------------> evalBlock")
#    tree = tree.left
#    while (tree!= None):
    result = evaluate(tree.left,env)
#        tree = tree.right
    global returned
    if returned:
        returned = False
    return result

def isTrue(tree):
    if tree.type == INTEGER and tree.word == 1:
        return True
    return False

def evalWhile(tree,env):
    #print("Here in ----------------------------> evalWhile")
    #print("WHILE TREE-------------------------->",tree)
    #print("WHILE TREE.left-------------------------->",tree.left)
    #print("WHILE TREE.right-------------------------->",tree.right)
    last = Lexeme(EMPTY)
    while isTrue(evaluate(tree.left,env)): 
#    while evaluate(tree.left,env) !=Lexeme(INTEGER,0):
        last = evaluate(tree.right,env)
    return last

def evalArray(tree,env):
    #print("Here in ----------------------------> evalArray")
    size = evaluate(tree.left.left,env).word
    return Lexeme(ARRAY,[None]*size)

def evalIndex(tree,env):
    #print("tree.left.left.left ----------------------->",tree.left.left.left)
    #print("tree,left.right.left ----------------------->",tree.left.right.left)
    array = evaluate(tree.left.left.left,env).word
    index = evaluate(tree.left.right.left,env).word
    return Lexeme(ARRAYINDEX,array[index])

def evalSet(tree,env):
    #print("tree.left.right.left ----------------------->",tree.left.right.left)
    #print("tree.left.left.left ----------------------->",tree.left.left.left)
    #print("tree.left.right.right.left ----------------------->",tree.left.right.right.left)
    #print("tree.left.left ----------------------->",tree.left.left)
    #print("tree,left.right.left ----------------------->",tree.left.right.left)
    a = evaluate(tree.left.left.left,env).word
    i = evaluate(tree.left.right.left,env).word
    val = evaluate(tree.left.right.right.left,env).word
    a[i] = val
    return Lexeme(ARRAYSET,a)
    

def main():
    env = newEnvironment()
    tree = parser(sys.argv[1])
    evaluate(tree,env)

main()
