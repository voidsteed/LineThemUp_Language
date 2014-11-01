# Zergling programming language
# Evaluator / interpreter
# by Kaleb Williams

from parser import *
from environment import *
import sys


def evaluate(tree,env):
	returned = False
	if tree:
		if tree.type == INTEGER or tree.type == REAL or tree.type == STRING:
			return tree
		elif tree.type == ID:
			return lookup(tree,env)
		elif tree.type == ARRAYDEF:
			return evalArrayDef(tree,env)
		elif tree.type == FUNCDEF:
			return evalFuncDef(tree,env)
		elif tree.type == ARGLIST:
			return evalArgs(tree, env)
		elif tree.type == BLOCK:
			return evalBlock(tree, env)
		elif tree.type == STATESEQ:
			return evalStateSeq(tree, env)
		elif tree.type == STATEMENT:
			return evalStatement(tree, env)
		elif tree.type == PLUS or tree.type == MINUS or tree.type == DIVIDEDBY or tree.type == TIMES or tree.type == CARET or tree.type == MOD or tree.type == GREATERTHAN or tree.type == GREATERTHANEQUAL or tree.type == LESSTHAN or tree.type == LESSTHANEQUAL or tree.type == EQUAL:
			return evalSimpleOp(tree,env)
		elif tree.type == AND or tree.type == OR:
			return evalShortCircuitOp(tree,env)
		elif tree.type == ASSIGN:
			return evalAssign(tree,env)
		elif tree.type == VAREXPR:
			if tree.right and tree.right.type != ARRAYDEF:
				return evalFuncCall(tree,env)
			elif tree.right:
				return evalArrayIndex(tree,env)
			else:
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
			return evalReturn(tree, env)
		elif tree.type == PRINT:
			return evalPrint(tree, env)

def evalArrayIndex(tree, env):
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
	argsList = tree.left
	array = Lexeme(ARRAY,[])
	def accumulate(argsList):
		if argsList:
			array.value.append(evaluate(argsList.left,env).value)
			accumulate(argsList.right)
	accumulate(argsList)
	return array

def evalPrint(tree, env):
	def printArgs(arg, e):
		if arg:
			print(evaluate(arg.left,e).value,end=' ')
			printArgs(arg.right, e)
		else:
			print()
	if tree.left.type != EMPTY:
		printArgs(tree.left, env)
	else:
		print()

def evalStateSeq(tree, env):
	last = evaluate(tree.left, env)
	if tree.right:
		last = evaluate(tree.right, env)
	return last

def evalStatement(tree, env):
	return evaluate(tree.left, env)

def evalReturn(tree, env):
	global returned
	returned = True
	if tree.left:
		return evaluate(tree.left,env)
	return None
	
def evalNot(tree, env):
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
	while evaluate(tree.left, env) != Lexeme(INTEGER, 0):
		last = evaluate(tree.right, env)
	return last

def evalIf(tree,env):
	boolean = evaluate(tree.left.left,env)
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
	boolean = evaluate(tree.left.left,env)
	if boolean.value:
		return evaluate(tree.left.right,env)
	elif tree.right:
		return evaluate(tree.right,env)
	else:
		return Lexeme(EMPTY)

def evalElse(tree,env):
	return evaluate(tree.left,env)	

def evalAssign(tree,env):
	if tree.left.type == ARRAYASSIGN:
		name = tree.left.left
		index = tree.left.right
	else:
		name = tree.left
		index = None
	current = lookup(name, env, True)
	if index and current:
		i = index.value
		if i == len(current.value):
			current.value.append(None)	
		current.value[i] = evaluate(tree.right, env).value
	elif current:
		setVar(name, evaluate(tree.right,env), env)
	else:
		insert(name, evaluate(tree.right,env), env)

def evalSimpleOp(tree,env):
	a = evaluate(tree.left, env)
	b = evaluate(tree.right, env)
	op = tree.value
	if a.type == REAL or b.type == REAL:
		result = Lexeme(REAL)
	elif a.type == INTEGER:
		result = Lexeme(INTEGER)
	elif a.type == STRING:
		result = LEXEME(STRING)
	result.value = eval(str(a.value)+tree.value+str(b.value))
	if result.value == False:
		result.value = 0
	elif result.value == True:
		result.value = 1
	return result

def evalShortCircuitOp(tree,env):
	a = evaluate(tree.left, env)
	result = Lexeme(REAL)
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
	closure = cons(env, cons(getFuncDefParams(tree), getFuncDefBody(tree)));
	insert(getFuncDefName(tree),closure,env)

def getFuncDefParams(tree):
	return tree.right.left

def getFuncDefName(tree):
	return tree.left

def getFuncDefBody(tree):
	return tree.right.right

def evalFuncCall(tree,env):
	global returned
	returned = False
	closure = evaluate(getFuncCallName(tree),env)
	args = getFuncCallArgs(tree)
	params = getClosureParams(closure)
	body = getClosureBody(closure)
	senv = getClosureEnvironment(closure)
	eargs = evalArgs(args, env)
	xenv = extend(params,eargs,senv)
	return evaluate(body,xenv)

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
	return closure.right.left

def getClosureBody(closure):
	return closure.right.right

def getClosureEnvironment(closure):
	return closure.left

def evalBlock(tree,env):
	tree = tree.left
	while tree:
		result = evaluate(tree.left, env)
		tree = tree.right
		global returned
		if returned:
			returned = False
			return result

def main():
	env = newEnvironment()
	tree = parser(sys.argv[1])
	evaluate(tree,env)

main()
