from environment import *

def main():
    print("Creating a new environment")
    env = newEnvironment()
    print("The environment is ")
    displayAll(env)
    print("Adding variable x with value 3")
    populate('x',3,env)
    print("The environment is ")
    displayAll(env)
    print("Extending the environment with y:4 and z:'hello'")
    env = extend(cons('y',cons('z',None)),cons(4, cons('hello',None)),env)
    print("The local environment is ")
    displayLocal(env)
    print("The environment is ")
    displayAll(env)
    print('lookUp "x" is', lookUp('x',env))
    print("x is setting to 7")
    setVar('x',7,env)
    print('lookUp "x" is', lookUp('x',env))
    print('lookUp if "e" is in environment: ')
    print(lookUp('e',env))


main()

