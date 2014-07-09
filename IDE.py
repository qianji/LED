'''
Qianji Zheng
July 2014
This program have test functions to combine the parser and evaluator together.
'''
from Compiler import compile
from Tokenizer import tokens
from Evaluater import val
from Parser import *
# import the global variable Program
import Compiler

# [This comment To be removed]
'''
If F is a string which is the name of a .led file (without the extension) run(F)
compiles program F and lets the user enter expressions to evaluate using the
definitions in F.
'''
def run(F):
    compile(F+'.led')
    #print(Compiler.Program)
    DefinedFuns = definedFuns(Compiler.Program)
    print('Defined functions: ',DefinedFuns)
    print()
    print('Enter an expression and hit [return] to get its value.')
    print('Hit [return] at the prompt to exit.')
    print()
    while True:
        if len(Compiler.Program)>0:
            e = input('> ')
            if e=='':
                return
            else:
                expression,eFlag = tokens(e)
                if eFlag:
                    tree, tFlag = parseExpression(expression)
                    if tFlag:
                        value = val(tree)
                        print(value)
                        print()
                    else:
                        print('Cannot parse the tree.')
                else:
                    print('Cannot tokenize the expression.')
        else:
            print("No program in the memory. Please use compile(t) to load the program first, where t is the name of your program file")
            return 

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
    values = []
    for e in L:
        e=tokens(e)[0]
        v = val(parseExpression(e)[0])
        values.append(v)
    return values
'''
# Program -> set
# If P is a program, then definedFuns(P) is a set of function named defined in P.
'''
def definedFuns(P):
    return {Def[0] for Def in P}
#compile('cp.txt')
#run('test_c')
#print(parseIfClauses(tokens('1 if 1<1; 2 if 2<2; 3 if 3<3')[0]))
#print(parseConditional(tokens('1 if 1<1; 2 if 2<2; 3 if 3<3;4 otherwise')[0]))
#print(parseConditional(tokens(' x+2 if x<-3; x+1 if x<0;x-1 otherwise')[0]))
#print(parseIfClauses(tokens('x+1 if x<0')[0]))
#print(parseConditional(tokens('x+1 if x<0;x-1 otherwise')[0]))
#print(parseConditional(tokens('3*x  if x<0;x-1 otherwise',)[0]))
#print(compile('cp.txt'))
#print(compile('p.txt'))
#print(val(parseExpression(tokens('0 >=1 &  1> 0')[0])[0]))
#print(tokens('|<10,20,30>|'))
#print(val(parseExpression(tokens('<10,20,30>[2]')[0])[0]))
#print(tokens('|<10,20,30>|')[0])
L = tokens('(1,2)[0]')[0]
T = parseExpression(L)[0]
print(val(T))

#print (val(parseExpression( tokens( '(10, 20)' )[0] ) [0]))
#print(closeParentesis('f{}}'))
#print(firstFuncHead('{ def dafad}'))
#print(removeComments('{def t(x) := {{}}{x,x+1} }'))
#print(parseSet("{2,3,4}"))
#print(expressionValues(['(1,2)[0]']))

