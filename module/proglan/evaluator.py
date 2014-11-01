# Zergling programming language
# Evaluator / interpreter
# by Kaleb Williams

from parser import *
from environment import *
import sys

returned = False

def evaluate(tree,env):
	if tree:
		#print("evaluating",tree)
		if tree.type == INTEGER or tree.type == REAL or tree.type == STRING:
			return tree
		elif tree.type == ID:
			temp = lookup(tree,env)
			#print(tree,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",temp)
			return temp
		elif tree.type == ARRAYDEF:
			return evalArrayDef(tree,env)
		elif tree.type == FUNCDEF:
			return evalFuncDef(tree,env)
		elif tree.type == 'env':
			return tree
		elif tree.type == ARGLIST:
			return evalArgs(tree, env)
		elif tree.type == BLOCK:
			return evalBlock(tree, env)
		elif tree.type == STATESEQ:
			temp = evalStateSeq(tree, env)
			#print("SSEEEEEEEEEEEEEEEQ",temp)
			return temp
		elif tree.type == STATEMENT:
			temp = evalStatement(tree, env)
			#print("ssssssssssstatement:",temp)
			return temp
		elif tree.type == PLUS or tree.type == MINUS or tree.type == DIVIDEDBY or tree.type == TIMES or tree.type == CARET or tree.type == MOD or tree.type == GREATERTHAN or tree.type == GREATERTHANEQUAL or tree.type == LESSTHAN or tree.type == LESSTHANEQUAL or tree.type == EQUAL:
			return evalSimpleOp(tree,env)
		elif tree.type == AND or tree.type == OR:
			return evalShortCircuitOp(tree,env)
		elif tree.type == ASSIGN:
			return evalAssign(tree,env)
		elif tree.type == VAREXPR:
			#print("VAREXPR:",tree.left,tree.right)
			if tree.right and tree.right.type != ARRAYDEF:
				#print("Iiiiiiiiin the VexpR braaaaaaaaaaaaaaaaanch",evalFuncCall(tree,env))
				return evalFuncCall(tree,env)
			elif tree.right:
				#print("Iiiiiiiiin the VexpR braaaaaaaaaaaaaaaaanch C")
				return evalArrayIndex(tree,env)
			else:
				#print("Iiiiiiiiin the VexpR braaaaaaaaaaaaaaaaanch B",tree.left,evaluate(tree.left,env))
				return evaluate(tree.left,env)
		elif tree.type == UMINUS:
			return evalUMinus(tree, env)
		elif tree.type == NOT:
			return evalNot(tree, env)
		elif tree.type == GROUP:
			return evaluate(tree.left, env)
		elif tree.type == IF:
			return evalIf(tree, env)
		elif tree.type == ELIF:
			return evalElif(tree, env)
		elif tree.type == ELSE:
			return evalElse(tree, env)
		elif tree.type == WHILE:
			return evalWhile(tree, env)
		elif tree.type == RETURN:
			temp = evalReturn(tree, env)
			return temp
		elif tree.type == PRINT:
			return evalPrint(tree, env)
	else:
		#print("Returning None")
		return None

def evalArrayIndex(tree, env):
	#print("in evalArrayIndex, returned is",returned)
	array = evaluate(tree.left, env)
	index = evaluate(tree.right.left,env)
	value = array.value[index.value]
	if isinstance(value, str):
		lexeme = Lexeme(STRING)
	elif isinstance(value, int):
		lexeme = Lexeme(INTEGER)
	elif isinstance(value, float):
		lexeme = Lexeme(REAL)
	lexeme.value = value
	return lexeme

def evalArrayDef(tree, env):
	#print("in evalArrayDef, returned is",returned)
	argsList = tree.left
	array = Lexeme(ARRAY,[])
	def accumulate(argsList):
		if argsList:
			array.value.append(evaluate(argsList.left,env).value)
			accumulate(argsList.right)
	#print(array.value)
	#print(argsList)
	if argsList and argsList.type != EMPTY:
		accumulate(argsList)
	return array

def evalPrint(tree, env):
	#print("in evalPrint, returned is",returned)
	def printArgs(arg, e):
		if arg and arg.type != EMPTY:
			result = evaluate(arg.left,env)
			if result.type == 'env':
				print("<function {name}>".format(name = arg.left.left,end=' '))
			else:
				print(result.value,end=' ')
				printArgs(arg.right, e)
		else:
			print()
	if tree.left.type != EMPTY:
		printArgs(tree.left, env)
	else:
		print()

def evalStateSeq(tree, env):
	#print("in evalStateSeq, returned is",returned,tree.left.left)
	last = evaluate(tree.left, env)
	#print("afteeeeeeeeeeeeeeeeeeeeeeeeeeeeeer evaluate",tree.left.left.left,returned)
	#print("{{{{{{{{{{{{{{{{{{{{{{{",tree.left.left,last,returned)
	if tree.right and not returned:
		#print("Not returning!!!!!!!!!!!!",tree.right.left.left)
		last = evaluate(tree.right, env)
		#print("not there yet... last is",last,tree.left.left,tree.right.left.left)
	if returned:
		#print("RETURNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",last,tree.left.left)
		return last
	#else:
		#print("lololololololololololololololololololol")
		#displayLocal(env)

def evalStatement(tree, env):
	#print("in evalStatement, returned is",returned)
	temp = evaluate(tree.left, env)
	#print("innnnnnn evalStatement",temp)
	return temp

def evalReturn(tree, env):
	#print("in evalReturned, returned is",returned)
	#print("&&&&&&&&&&&&&&&&&&&&&&&&& in evalReturn")
	global returned
	if tree.left:
		temp = evaluate(tree.left,env)
		returned = True
		#print("reeeeeeeeeeeeeeeetuuuuuuurning",temp)
	#	displayLocal(evaluate(tree.left.left,env).left)
		return temp
	#print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++past return",tree)
	returned = True
	#print("Returning None")
	return None
	
def evalNot(tree, env):
	#print("in evalNot, returned is",returned)
	boolean = evaluate(tree.left,env)
	result = Lexeme(INTEGER)
	if boolean.value:
		result.value = 0
	else:
		result.value = 1
	return result
	
def evalUMinus(tree, env):
	primary = evaluate(tree.left,env)
	result = Lexeme(primary.type)
	result.value = -primary.value
	return result

def evalWhile(tree, env):
	last = Lexeme(EMPTY)
	while evaluate(tree.left, env) != Lexeme(INTEGER, 0) and not returned:
		last = evaluate(tree.right, env)
	return last

def evalIf(tree,env):
	#print("in evalIf, returned is",returned)
	boolean = evaluate(tree.left.left,env)
	#print("IN EVALIF!!!!!!!!!!!!",tree.left.left.left,boolean)
	finished = False
	if boolean.value:
		return evaluate(tree.left.right,env)
	elif tree.right.left:
		result = evaluate(tree.right.left,env)
		if result != Lexeme(EMPTY):
			return result
	if tree.right.right:
		return evaluate(tree.right.right,env)
	return Lexeme(EMPTY)

def evalElif(tree,env):
	#print("in evalElif, returned is",returned)
	boolean = evaluate(tree.left.left,env)
	if boolean.value:
		return evaluate(tree.left.right,env)
	elif tree.right:
		return evaluate(tree.right,env)
	else:
		return Lexeme(EMPTY)

def evalElse(tree,env):
	#print("in evalElse, returned is",returned)
	return evaluate(tree.left,env)	

def evalAssign(tree,env):
	#print("in evalAssign, returned is",returned)
	#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<In evalAssign",tree,tree.left)
	if tree.left.type == ARRAYASSIGN:
		#print("In evalAssign A",tree.left.left,",,,,,,,,",tree.left.right)
		name = tree.left.left
		index = evaluate(tree.left.right,env)
	else:
	#	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%In evalAssign B",tree.right.left,tree.right,evaluate(tree.right,env))
		name = tree.left
		index = None
	current = lookup(name, env, True)
	#print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Current::",current)
	if index and current:
		#print("><><><><><><><><><><><><><><><><><><><><><><<><><><><><><<><><><><><><><><><><><><><><><><><><>")
		i = index.value
		if i == len(current.value):
			current.value.append(None)	
		current.value[i] = evaluate(tree.right, env).value
	elif current:
		#print("_____________________________________________________________________________________________________________________________________________________________________________setting",name,evaluate(tree.right,env))
		setVar(name, evaluate(tree.right,env), env)
	else:
		#print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,inserting",name,evaluate(tree.right,env))
		insert(name, evaluate(tree.right,env), env)

def evalSimpleOp(tree,env):
	#print("in evalSimpleOp, returned is",returned)
	a = evaluate(tree.left, env)
	b = evaluate(tree.right, env)
	op = tree.value
	if a.type == REAL or b.type == REAL:
		result = Lexeme(REAL)
		result.value = eval(str(a.value)+tree.value+str(b.value))
	elif a.type == INTEGER:
		result = Lexeme(INTEGER)
		result.value = eval(str(a.value)+tree.value+str(b.value))
	elif a.type == STRING and tree.value == '+':
		result = Lexeme(STRING)
		result.value = a.value + b.value
	elif a.type == STRING and (tree.value == '<=' or tree.value == '<' or tree.value == '==' or tree.value == '>' or tree.value == '>='):
		result = Lexeme(INTEGER)
		result.value = eval("a.value"+tree.value+"b.value")
	else:
		result = Lexeme(INTEGER)
		result.value = eval(str(a.value)+tree.value+str(b.value))
	if result.value == False:
		result.value = 0
	elif result.value == True:
		result.value = 1
	return result

def evalShortCircuitOp(tree,env):
	#print("in evalShortCircuitOp, returned is",returned)
	a = evaluate(tree.left, env)
	result = Lexeme(INTEGER)
	if tree.type == AND:
		if not a.value:
			result.value = a.value
		else:
			result.value = a.value and evaluate(tree.right, env).value
	else:
		if a.value:
			result.value = a.value
		else:
			result.value = a.value or evaluate(tree.right, env).value
	return result

def evalFuncDef(tree, env):
	#print("in evalFuncDef, returned is",returned)
	closure = cons(env, cons(getFuncDefParams(tree), getFuncDefBody(tree)))
#	print("=====================",tree,"===============================Closure is",closure,evaluate(closure,env))
#	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",getFuncDefName(tree))
	insert(getFuncDefName(tree),closure,env)
	return closure
#	print("!!!!!!!!!!!!!!!!!!!!!!!!!!",lookup(getFuncDefName(tree),env))

def getFuncDefParams(tree):
	return tree.right.left

def getFuncDefName(tree):
	return tree.left

def getFuncDefBody(tree):
	return tree.right.right

def evalFuncCall(tree,env):
	#print("*************************************************************************in func call",tree,tree.left,lookup(tree.left,env))
	global returned
	closure = evaluate(getFuncCallName(tree),env)
	args = getFuncCallArgs(tree)
	params = getClosureParams(closure)
	body = getClosureBody(closure)
	senv = getClosureEnvironment(closure)
	eargs = evalArgs(args, env)
	xenv = extend(params,eargs,senv)
	temp = evaluate(body,xenv)
	returned = False
	#print("evalFuncCall------------> ",body,body.left,body.left.right.right.right.right.left.left.left.left,temp,getFuncCallName(tree))
	#displayLocal(xenv)
	#print("-------><----------------")
	return temp

def evalArgs(tree, env):
	if tree.left:
		evaledList = Lexeme(ARGLIST)
		newLexeme = Lexeme(tree.left.type)
		newLexeme = evaluate(tree.left,env)
		evaledList.left = newLexeme
		if tree.right:
			evaledList.right = evalArgs(tree.right, env)
		return evaledList

def getFuncCallArgs(tree):
	return tree.right

def getFuncCallName(tree):
	return tree.left

def getClosureParams(closure):
	#print("In getClosureParams",closure)
	return closure.right.left

def getClosureBody(closure):
	return closure.right.right

def getClosureEnvironment(closure):
	return closure.left

def evalBlock(tree,env):
	#print("in evalBlock, returned is",returned)
	temp = evaluate(tree.left, env)
	#print("```````````````````````````",temp,tree.left,tree.left.left.left)
	return temp

def main():
	env = newEnvironment()
	tree = parser(sys.argv[1])
	evaluate(tree,env)

main()
