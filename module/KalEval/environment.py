# Zergling programming language
# Environment
# by Kaleb Williams

from lexeme import *
import sys

class LookUpError(Exception):
	def __init__(self, var):
		self.var = var

	def __str__(self):
		return repr(self.var)

class SetError(LookUpError):
	pass

def cons(a,b):
	n = Lexeme("env")
	n.left = a
	n.right = b
	return n

def car(cell):
	return cell.left

def cdr(cell):
	return cell.right

def setCar(cell, val):
	cell.left = val

def setCdr(cell, val):
	cell.right = val

def newEnvironment():
	return cons(cons(None, cons(None, None)), None)

def insert(var, val, env):
	local = car(env)
	local.left = cons(var, local.left)
	local.right.left = cons(val, local.right.left)
	return val

def lookup(var, env, safe=False):
	try:
		while (env != None):
			local = car(env)
			vars = car(local)
			vals = car(cdr(local))
			while vars != None:
				#print("in lookup------><><>>>> ", car(vars), var)
				#print("what the fuck?????",car(vars)==var)
				if var == car(vars):
					return car(vals)
				vars = cdr(vars)
				vals = cdr(vals)
			env = cdr(env)
		if not safe:
			raise LookUpError(var)
	except LookUpError as e:
		print('LookUpError: {c} is undefined.'.format(c = e.var))
		sys.exit(1)
	return False

def setVar(var, val, env):
	try:
		while (env != None):
			local = car(env)
			vars = car(local)
			vals = car(cdr(local))
			while vars != None:
				if var == car(vars):
					oldVal = car(vals)
					setCar(vals, val)
					return oldVal
				vars = cdr(vars)
				vals = cdr(vals)
			env = cdr(env)
		raise SetError(var)
	except SetError as e:
		print('SetError: {c} is undefined.'.format(c = e.var))
		sys.exit(1)

def extend(vars, vals, env):
	return cons(cons(vars, cons(vals, None)), env)

def displayLocal(env):
	local = car(env)
	vars = car(local)
	vals = car(cdr(local))
	if vars == None:
		print("     (Empty)")
	while vars != None:
		print("     " + repr(car(vars)) + ":" + repr(car(vals)))
		vars = cdr(vars)
		vals = cdr(vals)

def displayAll(env):
	while (env != None):
		displayLocal(env)
		print()
		env = cdr(env)

