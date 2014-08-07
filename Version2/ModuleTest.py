'''
This module is used for test individual modules in LED. Please use UnitTest.py if you would like to do the unit testing 
'''
from Compiler import compile
from Tokenizer import tokens
from Evaluater import val
from Parser import *
from GlobalVars import *
from IDE import *
from EaselLED import *

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
play('tttftb')
#run('test')