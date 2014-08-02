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
Test tokens(S) in Tokenizer.py
'''
def test_tokens():
    while True:
        e = input('Please input the strings to be tokenized: ')
        if e=='':
            return
        else:
            print(tokens(e)[0])

'''
'''
#run('test')
#test_tokens()
print(parseExpression(tokens('{1..23}')[0]))
#run()
