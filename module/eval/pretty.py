from parser import *
def prettyPrint(tree):
    if tree:
        if tree.type == INTEGER or tree.type == REAL or tree.type == STRING or tree.type == ID:
            print(tree.word,end='')
        elif tree.type == FUNCDEF:
            print("def ",end='')
            prettyPrint(tree.left)
            print("(",end='')
            prettyPrint(tree.right.left)
            print(")",end='')
            prettyPrint(tree.right.right)
        elif tree.type == PARAMSLIST or tree.type == ARGLIST:
            prettyPrint(tree.left)
            if tree.right:
                print(',',end='')
                prettyPrint(tree.right)
        elif tree.type == BLOCK:
            print('{')
            prettyPrint(tree.left)
            print('}')

        elif tree.type == ARRAY:
            print("array",end='')
            print('(',end='')
            prettyPrint(tree.left)
            print(')',end='')

        elif tree.type == ARRAYINDEX:
            print("arrayIndex",end='')
            print('(',end='')
            prettyPrint(tree.left)
            print(')',end='')

        elif tree.type == ARRAYSET:
            print("arrayIndex",end='')
            print('(',end='')
            prettyPrint(tree.left)
            print(')',end='')

        elif tree.type == STATELIST:
            prettyPrint(tree.left)
            if tree.right:
                prettyPrint(tree.right)
        elif tree.type == STATEMENT:
            prettyPrint(tree.left)
            if tree.right:
                prettyPrint(tree.right)
        elif tree.type == SEMICOLON:
            print(';')
        elif tree.type == NOT:
            print("not")
            prettyPrint(tree.left)
        elif tree.type == PLUS or tree.type == MINUS or tree.type == DIVIDEDBY or tree.type == TIMES or tree.type == MOD or tree.type == GREATERTHAN or tree.type == LESSTHAN or tree.type == EQUAL or tree.type == AND or tree.type == OR:
            prettyPrint(tree.left)
            print(' ',end='')
            print(tree.word,end='')
            print(' ',end='')
            prettyPrint(tree.right)
        elif tree.type == VAREXPR:
            prettyPrint(tree.left)
            if tree.right and tree.right.type != EMPTY and tree.right:
                print('(',end='')
                prettyPrint(tree.right)
                print(')',end='')
        elif tree.type ==GROUP:
            prettyPrint(tree.left)
        elif tree.type == IF:
            print("if (",end='')
            prettyPrint(tree.left.left)
            print(')',end='')
            prettyPrint(tree.left.right)
            if tree.right.left:
                prettyPrint(tree.right.left)
        elif tree.type == ASSIGN:
            print('$',end='')
            prettyPrint(tree.left)
            print(' ',end='')
            print('= ',end='')
            prettyPrint(tree.right)
            print(';')
        elif tree.type == ELSE:
            print("else")
            prettyPrint(tree.left)
        elif tree.type == WHILE:
            print("while ",end='')
            print('(',end='')
            prettyPrint(tree.left)
            print(')',end='')
            print()
            prettyPrint(tree.right)
        elif tree.type == RETURN:
            print("return ",end='')
            if tree.left:
                prettyPrint(tree.left)
            print(';')
        elif tree.type == PRINT:
            print("print",end='')
            print("(",end='')
            prettyPrint(tree.left)
            print(")",end='')
            print(";")
        elif tree.type == EMPTY:
            print(end='')
        else:
            print("invalid expression!")

prettyPrint(parser(sys.argv[1]))
