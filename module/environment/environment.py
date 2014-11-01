import sys
from lexeme import *

class lookUpEnvError(Exception):
    def __init__(self, var):
        self.var = var
    def __str__():
        repr(self.var)

class setEnvError(lookUpEnvError):
    pass

def cons(a, b):
    n = Lexeme(ENV)
    n.left = a
    n.right = b
    return n

def car(cell):
    return cell.left

def setCar(cell,val):
    cell.left = val

def cdr(cell):
    return cell.right

def setCdr(cell,val):
    cell.right = val

def cadr(cell):
    return car(cdr(cell))

def newEnvironment():
    return cons(cons(None, cons(None,None)), None)

def populate(var,val,env):
    local = car(env)
    local.left = cons(var,car(local))
    local.right.left = cons(val,local.right.left)
    return val

def sameVar(a, b):
    if a != b:
        return False
    return True

def lookUp(var,env):
    try:
        while env != None:
            local = car(env)
            vars = car(local)
            vals = cadr(local)
            while vars != None:
                if sameVar(var,car(vars)):
                    return car(vals)
                vars = cdr(vars)
                vals = cdr(vals)
            env = cdr(env)
        raise lookUpEnvError(var)
    except lookUpEnvError as e:
        print('lookUpEnvError: variable {v} undefined.'.format(v = e.var))
        sys.exit(1)

def extend(vars,vals,env):
    return cons(cons(vars,cons(vals,None)), env)

def setVar(var, val, env):
    try:
        while env != None:
            local = car(env)
            vars = car(local)
            vals = cadr(local)
            while vars != None:
                if sameVar(var,car(vars)):
                    oldVal = car(vals)
                    setCar(vals,val)
                    return oldVal
                vars = cdr(vars)
                vals = cdr(vals)
            env = cdr(env)
        raise setEnvError(var)
    except setEnvError as e:
        print('setEnvError: variable {v} undefined.'.format(v = e.var))
        sys.exit(1)

def displayLocal(env):
    local = car(env)
    vars = car(local)
    vals = cadr(local) 
    if vars == None:
        print('*******'+ "Env is empty")
    while vars != None:
        print(repr(car(vars)) + ' is ' + repr(car(vals)))
        vars = cdr(vars)
        vals = cdr(vals)


def displayAll(env):
    while env != None:
        displayLocal(env)
        env = cdr(env)
        
