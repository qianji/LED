'''
Qianji
March 2015
This file is created to be called in the server to evaluate an expression
'''

import sys
from Tokenizer import *
from Expression import *
from LEDProgram import *
from Evaluater import val
from Parser import *
from Compiler import *
from EaselLED import *

def evaluateLEDExpression():
    e = sys.argv[1]
    expression,eFlag = tokens(e)
    if eFlag:
        tree, tFlag = parseExpression(expression)
        if tFlag:
            try:
                value = val(tree.expression())
                if not value ==None:
                    if isinstance(value,Fraction):
                        value = numeralValue(value)
                    print(prettyString(value))
            except:
                print('Failed to evaluate the expression. It is not a valid expression')
            return
        d,defFlag = parseDfn(expression)
        if defFlag:
            #print('parsing #',i,"function successfully",' '.join(funcs[i]))
            Program.update(d)
        else:
            print('Failed to parse the expression or definition.')
    else:
        print('Failed to tokenize the expression.The last 10 valid tokens are',expression[-10:])

evaluateLEDExpression()

