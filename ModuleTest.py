'''
This module is used for test individual modules in LED. Please use UnitTest.py if you would like to do the unit testing 
'''
from Compiler import compile
from Tokenizer import tokens
from Evaluater import val
from Parser import *
from GlobalVars import *
from IDE import *

'''
Test tokens in Tokenizer.py
'''
def test_tokens():
    while True:
        e = input('Please input the strings to be tokenized: ')
        if e=='':
            return
        else:
            print(tokens(e)[0])

test_tokens()
#run()
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
#L = tokens('(1,2)[0]')[0]
#T = parseExpression(L)[0]
#print(val(T))
#print (val(parseExpression( tokens( '(10, 20)' )[0] ) [0]))
#print(closeParentesis('f{}}'))
#print(firstFuncHead('{ def dafad}'))
#print(removeComments('{def t(x) := {{}}{x,x+1} }'))
#print(parseSet("{2,3,4}"))
#print(expressionValues(['(1,2)[0]']))
#run()