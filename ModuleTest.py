'''
This module is used for test individual modules in LED. Please use UnitTest.py if you would like to do the unit testing 
'''
#from Compiler import compile
from Tokenizer import tokens
#from Evaluater import val
#from Parser import *
#from IDE import *
from Tokenizer import *
from Expression import *
from LEDProgram import *
from Evaluater import val
from Parser import *
from Compiler import *
from EaselLED import *

import sys, os, pygame
from pygame.locals import *
from pygame.compat import geterror

'''
Test tokens(S) in Tokenizer.py
'''
def test_tokens():
    while True:
        e = input('Please input the strings to be tokenized: ')
        if e=='':
            return
        else:
            print('token is',tokens(e)[0])

def test_evaluator(expression):
    expression,eFlag = tokens(expression)
    start_time = timeit.default_timer()
    tree, tFlag = parseExpression(expression)
    elapsed = timeit.default_timer() - start_time
    print("Parsing time",elapsed)
    if tFlag:
        start_time = timeit.default_timer()
        value = val(tree.expression())
        elapsed = timeit.default_timer() - start_time
        print("Evaluating time",elapsed)
        if not value ==None:
            if isinstance(value,Fraction):
                value = numeralValue(value)
            print(prettyString(value))

compile('ThackerPente.led')
expression = 'newState((B,(10,10)),({(W,(10,11)),(W,(10,12)),(W,(11,10)),(W,(12,10)),(B,(10,13)),(B,(13,10))},B,0,0, (W,(11,10))))'
compile('temp2.led')
#e2 = 'g(C)+g(C)'
test_evaluator(expression)

#print(dictionary[0])
#print(dictionary.dic)
'''
'''
#run('test')
#test_tokens()
#print(parseExpression(tokens('{1..23}')[0])

#run()
#t = AST('tuple',[1,2,3])
#print(prettyString(t.val()))
#t = tokens('some x in {0,1,2} : x<0')[0]
#print(t)
#E = parseExpression(t)
#print(E)
#print( E[0].val())
#ast = AST(1)
#print(ast)
#run('test')
#a1 = AST('tuple',[AST(1),AST(2),AST(3)])
#a2 = AST('+',[AST(1),AST(2)])
#a3 = AST(1)
#a = AST('com',[a1,a2,a3])
#print(a.toString())
#play('tttftb')
#run('test')


