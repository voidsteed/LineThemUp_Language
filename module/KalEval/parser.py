# Zergling programming language
# Parser
# by Kaleb Williams

from lexer import *
import sys

class LanguageSyntaxError(Exception):
	def __init__(self, t, current):
		self.checkType = t
		self.lexType = current

	def __str__(self):
		return repr(self.checkType) + ", " + repr(self.lexType)

lexemes = []
currentLexeme = None
currentIndex = 0
backtracked = 0
def parser(filename):
	lxr = Lexer(filename)
	global currentLexeme
	currentLexeme = lxr.lex()
	lexemes.append(currentLexeme)
	currentIndex = 0

	def functionDef():
		match(DEF)
		name = match(ID)
		match(OPAREN)
		params = optParamList()
		match(CPAREN)
		actions = block()
		tree = Lexeme(FUNCDEF)
		tree.left = name
		temp = Lexeme(CELL)
		temp.left = params
		temp.right = actions
		tree.right = temp
		return tree
	
	def functionDefPending():
		return check(DEF)
	
	def optParamList():
		if paramListPending():
			return paramList()
		else:
			return None
	
	def paramListPending():
		return check(ID)

	def paramList():
		name = match(ID)
		temp = Lexeme(PARAMLIST)
		if check(COMMA):
			match(COMMA)
			temp.right = paramList()
		else:
			temp.right = None
		temp.left = name
		return temp
	
	def block():
		temp = Lexeme(BLOCK)
		match(OBRACE)
		temp.left = optStatementSeq()
		match(CBRACE)
		return temp

	def optStatementSeq():
		if statementSeqPending():
			return statementSeq()
		else:
			return None
	
	def statementSeq():
		temp = Lexeme(STATESEQ)
		temp.left = statement()
		if statementSeqPending():
			temp.right = statementSeq()
		return temp

	def statementSeqPending():
		return statementPending()

	def statement():
		temp = Lexeme(STATEMENT)
		if expressionPending():
			temp.left = expression()
			temp.right = match(SEMICOLON)
		elif assignmentPending():
			temp.left = assignment()
			temp.right = match(SEMICOLON)
		elif ifStatementPending():
			temp.left = ifStatement()
		elif whileStatementPending():
			temp.left = whileStatement()
		elif check(RETURN):
			temp.left = match(RETURN)
			temp.left.left = optExpression()
			temp.right = match(SEMICOLON)
		elif functionDefPending():
			temp.left = functionDef()
		elif check(PRINT):
			temp.left = match(PRINT)
			match(OPAREN)
			temp.left.left = optArgList()
			match(CPAREN)
			match(SEMICOLON)
		return temp
		
	def statementPending():
		return expressionPending() or assignmentPending() or ifStatementPending() or whileStatementPending() or check(RETURN) or functionDefPending() or check(PRINT)
	
	def optExpression():
		if expressionPending():
			return expression()
		else:
			return None
	
	def expression():
		tree = primary()
		if operatorPending():
			temp = operator()
			temp.left = tree
			temp.right = expression()
			tree = temp
		return tree

	def expressionPending():
		return primaryPending()

	def assignment():
		temp = match(ID)
		if check(ASSIGN):
			tree = match(ASSIGN)
			tree.right = expression()
			tree.left = temp
		else:
			match(OBRACK)
			index = match(INTEGER)
			match(CBRACK)
			tree = match(ASSIGN)
			tree.right = expression()
			tree.left = Lexeme(ARRAYASSIGN)
			tree.left.left = temp
			tree.left.right = index
		return tree

	def assignmentPending():
		return check(ID)

	def operator():
		if check(PLUS):
			tree = match(PLUS)
		elif check(MINUS):
			tree = match(MINUS)
		elif check(DIVIDEDBY):
			tree = match(DIVIDEDBY)
		elif check(TIMES):
			tree = match(TIMES)
		elif check(CARET):
			tree = match(CARET)
		elif check(MOD):
			tree = match(MOD)
		elif check(GREATERTHAN):
			tree = match(GREATERTHAN)
		elif check(GREATERTHANEQUAL):
			tree = match(GREATERTHANEQUAL)
		elif check(LESSTHAN):
			tree = match(LESSTHAN)
		elif check(LESSTHANEQUAL):
			tree = match(LESSTHANEQUAL)
		elif check(AND):
			tree = match(AND)
		elif check(OR):
			tree = match(OR)
		else:
			tree = match(EQUAL)
		return tree

	def operatorPending():
		return check(PLUS) or check(MINUS) or check(DIVIDEDBY) or check(TIMES) or check(CARET) or check(MOD) or check(GREATERTHAN) or check(GREATERTHANEQUAL) or check(LESSTHAN) or check(LESSTHANEQUAL) or check(AND) or check(OR) or check(EQUAL)

	def primary():
		if check(INTEGER):
			tree = match(INTEGER)
		elif check(REAL):
			tree = match(REAL)
		elif check(STRING):
			tree = match(STRING)
		elif check(OPAREN):
			tree = Lexeme(GROUP)
			match(OPAREN)
			tree.left = expression()
			match(CPAREN)
		elif varExpressionPending():
			tree = varExpression()
		elif notPending():
			tree = match(NOT)
			tree.left = primary()
		elif check(OBRACK):
			tree = Lexeme(ARRAYDEF)
			match(OBRACK)
			tree.left = optArgList()
			match(CBRACK)
		else: #unary minus
			tree = match(MINUS)
			tree.type = UMINUS
			tree.left = primary()
		return tree

	def notPending():
		return check(NOT)

	def primaryPending():
		return check(INTEGER) or check(REAL) or check(STRING) or check(OPAREN) or varExpressionPending() or check(NOT) or check(MINUS) or check(OBRACK)

	def varExpression():
		tree = Lexeme(VAREXPR)
		tree.left = match(ID)
		if check(OPAREN):
			match(OPAREN)
			tree.right = optArgList()
			match(CPAREN)
		elif check(OBRACK):
			match(OBRACK)
			tree.right = Lexeme(ARRAYDEF)
			tree.right.left = match(INTEGER)
			match(CBRACK)
		return tree

	def varExpressionPending():
		hasID = check(ID)
		advance()
		hasBrack = check(OBRACK)
		advances = 1
		if hasID and hasBrack:
			while currentLexeme.type != CBRACK:
				advance()
				advances += 1
			advance()
			advances += 1
		hasAssign = check(ASSIGN)
		for i in range (0,advances):
			backtrack()
		return (hasID and (not hasAssign))

	def optArgList():
		if argListPending():
			return argList()
		else:
			return Lexeme(EMPTY)
	
	def argList():
		tree = Lexeme(ARGLIST)
		tree.left = expression()
		if check(COMMA):
			match(COMMA)
			tree.right = argList()
		return tree

	def argListPending():
		return expressionPending()

	def ifStatement():
		tree = match(IF)
		ifBlock = Lexeme(CELL)
		ifBlock.left = expression()
		ifBlock.right = block()
		tree.left = ifBlock
		opts = Lexeme(CELL)
		opts.left = optElif()
		opts.right = optElse()
		tree.right = opts
		return tree

	def ifStatementPending():
		return check(IF)

	def optElif():
		if check(ELIF):
			tree = match(ELIF)
			elifBlock = Lexeme(CELL)
			elifBlock.left = expression()
			elifBlock.right = block()
			tree.left = elifBlock
			tree.right = optElif()
			return tree
		else:
			return None

	def optElse():
		if check(ELSE):
			tree = match(ELSE)
			tree.left = block()
			return tree
		else:
			return None

	def whileStatement():
		tree = match(WHILE)
		tree.left = expression()
		tree.right = block()
		return tree

	def whileStatementPending():
		return check(WHILE)

	def check(t):
		return currentLexeme.type == t
	
	def advance():
		global lexemes
		global currentLexeme
		global currentIndex
		global backtracked
		if backtracked:
			backtracked -= 1
			current = lexemes[currentIndex+1]
		else:
			current = lxr.lex()
			lexemes.append(current)
		currentLexeme = current
		currentIndex += 1

	def backtrack():
		global lexemes
		global currentLexeme
		global currentIndex
		global backtracked
		currentIndex -= 1
		backtracked += 1
		currentLexeme = lexemes[currentIndex]

	def match(t):
		temp = currentLexeme
		matchNoAdvance(t)
		advance()
		return temp

	def matchNoAdvance(t):
		if not check(t):
			raise LanguageSyntaxError(t, currentLexeme.type)
	
	try:
		code = statementSeq()
		return code
	except LanguageSyntaxError as e:
		print('illegal') 
		print('LanguageSyntaxError: expected lexeme of type {c}, got type {l}'.format(c = e.checkType, l = e.lexType))
		sys.exit(1)
	
#parser(sys.argv[1])
