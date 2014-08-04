'''
Qianji Zheng
July 2014

This program have test functions to combine the parser and evaluator together.
'''
from Compiler import compile
from Tokenizer import tokens
from Evaluater import val
from Parser import *
from GlobalVars import *
# import the global variable Program

def prettyString(E):
    if isNumber(E) or isAtom(E): return(str(E))
    if isSet(E): return('{' + prettyStack(E[1]) + '}')
    if isVector(E): return( '<' + prettyStack(E[1]) + '>')
    if isTuple(E): return( '(' + prettyStack(E[1]) + ')')

def prettyStack(elts):
    Str = ''
    if not elts==[]:
        Str += prettyString(elts[0])
        for e in elts[1:]:
            Str += ',' + prettyString(e)
    return Str  

'''
If F is a string which is the name of a .led file (without the extension) run(F)
compiles program F and lets the user enter expressions to evaluate using the
definitions in F.
'''
def run(F=''):
    if not F=='':
        compile(F+'.led')
    #print(Compiler.Program)
    DefinedFuns = definedFuns(Program)
    if len(DefinedFuns)>0:
        print('Defined functions: ',DefinedFuns)
        print()
    print('Enter an expression and hit [return] to get its value.')
    print('Hit [return] at the prompt to exit.')
    print()
    while True:
        e = input('> ')
        if e=='':
            return
        else:
            expression,eFlag = tokens(e)
            if eFlag:
                tree, tFlag = parseExpression(expression)
                if tFlag:
                    print(prettyString(tree.val()))
                    print()
                else:
                    print('Cannot parse the tree.')
            else:
                print('Cannot tokenize the expression.')

'''
# This function is used for UnitTest
# str * str * list<list<num> -> list<>
# If F is the name of the file of the program, FunN is one of the functions in F and 
# ParamsL is a list of valid parameters of FunN
# then functionValues(F,FunN,ParamsL) is the value of the FunN(ParamsL) in F
'''

def functionValues(F,FunN,ParamsL):        
    compile(F+'.led')
    values = []
    for Params in ParamsL:        
        # construct the params for the expression
        paramsStr = ''
        for i in range(len(Params)):
            if not i == len(Params)-1:
                paramsStr += str(Params[i])+','
            else:
                paramsStr += str(Params[i])
        # check for constant definition g = 12
        if paramsStr=='':
            e = FunN
        else:
            e = FunN + '(' + paramsStr + ')'
        expression,eFlag = tokens(e)
        if eFlag:
            tree, tFlag = parseExpression(expression)
            if tFlag:
                values.append(val(tree))
    return values      

'''
list<str> -> list<int>
This is a helper function for testing evaluater
If L is a list of expressions, then expressionValues(L) is a list of values corresponds to L
'''
def expressionValues(L):
    #compile('test.led')
    values = []
    for e in L:
        e=tokens(e)[0]
        #v = val(parseExpression(e)[0])
        tree = parseExpression(e)[0]
        v = tree.val()
        values.append(v)
    return values
'''
# Program -> set
# If P is a program, then definedFuns(P) is a set of function named defined in P.
'''
def definedFuns(P):
    return {Def[0] for Def in P}
