# Zergling programming language
# Pretty printer
# by Kaleb Williams

from parser import *

def prettyPrint(tree):
	if tree:
		if tree.type == INTEGER or tree.type == REAL or tree.type == ID:
			print(tree.value,end='')
		elif tree.type == STRING:
			print('{delimiter}{string}{delimiter}'.format(string = tree.value, delimiter = tree.delimiter),end='')
		elif tree.type == FUNCDEF:
			print("def ",end='')
			prettyPrint(tree.left)
			print("(",end='')
			prettyPrint(tree.right.left)
			print(")")
			prettyPrint(tree.right.right)
		elif tree.type == PARAMLIST or tree.type == ARGLIST:
			prettyPrint(tree.left)
			if tree.right:
				print(",",end='')
				prettyPrint(tree.right)
		elif tree.type == BLOCK:
			print("{")
			prettyPrint(tree.left)
			print("}")
		elif tree.type == STATESEQ:
			prettyPrint(tree.left)
			if tree.right:
				prettyPrint(tree.right)
		elif tree.type == STATEMENT:
			prettyPrint(tree.left)
			if tree.right:
				prettyPrint(tree.right)
		elif tree.type == SEMICOLON:
			print(";")
		elif tree.type == PLUS or tree.type == MINUS or tree.type == DIVIDEDBY or tree.type == TIMES or tree.type == CARET or tree.type == MOD or tree.type == GREATERTHAN or tree.type == GREATERTHANEQUAL or tree.type == LESSTHAN or tree.type == LESSTHANEQUAL or tree.type == EQUAL or tree.type == ASSIGN:
			prettyPrint(tree.left)
			print(" ",end='')
			print(tree.value,end='')
			print(" ",end='')
			prettyPrint(tree.right)
		elif tree.type == AND:
			prettyPrint(tree.left)
			print(" and ", end='')
			prettyPrint(tree.right)
		elif tree.type == OR:
			prettyPrint(tree.left)
			print(" or ", end='')
			prettyPrint(tree.right)
		elif tree.type == VAREXPR:
			prettyPrint(tree.left)
			if tree.right and tree.right.type != ARRAYDEF:
				print("(",end='')
				prettyPrint(tree.right)
				print(")",end='')
			elif tree.right:
				prettyPrint(tree.right)
		elif tree.type == UMINUS:
			print("-",end='')
			prettyPrint(tree.left)
		elif tree.type == NOT:
			print("not ",end='')
			prettyPrint(tree.left)
		elif tree.type == GROUP:
			print("(",end='')
			prettyPrint(tree.left)
			print(")",end='')
		elif tree.type == IF:
			print("if ",end='')
			prettyPrint(tree.left.left)
			print()
			prettyPrint(tree.left.right)
			if tree.right.left:
				prettyPrint(tree.right.left)
			if tree.right.right:
				prettyPrint(tree.right.right)
		elif tree.type == ELIF:
			print("elif ",end='')
			prettyPrint(tree.left.left)
			print()
			prettyPrint(tree.left.right)
			if tree.right:
				prettyPrint(tree.right)
		elif tree.type == ELSE:
			print("else")
			prettyPrint(tree.left)
		elif tree.type == WHILE:
			print("while ",end='')
			prettyPrint(tree.left)
			print()
			prettyPrint(tree.right)
		elif tree.type == RETURN:
			print("return ",end='')
			if tree.left:
				prettyPrint(tree.left)
		elif tree.type == PRINT:
			print("print(",end='')
			prettyPrint(tree.left)
			print(");")
		elif tree.type == ARRAYDEF:
			print("[",end='')
			prettyPrint(tree.left)
			print("]",end='')
		elif tree.type == ARRAYASSIGN:
			prettyPrint(tree.left)
			print("[",end='')
			prettyPrint(tree.right)
			print("]",end='')
		elif tree.type != EMPTY:
			print("Bad expression!")

prettyPrint(parser(sys.argv[1]))
