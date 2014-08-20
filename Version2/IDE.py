'''
Qianji Zheng
July 2014

This program have test functions to combine the parser and evaluator together.
'''
from Tokenizer import *
from Expression import *
from LEDProgram import *
from Evaluater import val
from Parser import *
from Compiler import *
from EaselLED import *

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
    DefinedFuns = Program.definedSymbols()
    if len(DefinedFuns)>0:
        print('Defined functions: ',DefinedFuns)
        print()
    print('Enter an expression and hit [return] to get its value.')
    print('Enter quit() at the prompt to exit.')
    print()
    while True:
        e = input('> ')
        if e=='':
            continue
        else:
            expression,eFlag = tokens(e)
            if eFlag:
                if len(expression)==3 and expression[0]=='quit' and expression[1]=='(' and expression[-1]==')': return
                if len(expression)>3:
                    if expression[0]=='run' and expression[1]=='(' and expression[-1]==')':
                        return run(expression[2])
                    if expression[0]=='play' and expression[1]=='(' and expression[-1]==')':
                        return play(expression[2])
                tree, tFlag = parseExpression(expression)
                if tFlag:
                    value = val(tree)
                    if not value ==None:
                        print(prettyString(value))
                    print()
                else:
                    print('Failed to parse the expression. It is not a valid expressioin.')
            else:
                print('Failed to tokenize the expression.The last 10 valid tokens are',expression[-10:])

# play(F) executes the game defined in LED file F. 

def play(F):
    global images, Gamma, click
    displayWindow = GraphWin("My game", displaySize()[0], displaySize()[1])
    clickDef = Definition('click',[],AST('tuple',[0,0]))
    gammaDef = Definition('Gamma',[],AST('set',[]))
    Program.update(clickDef)
    Program.update(gammaDef)
    compile(F+'.led')
    DefinedFuns = Program.definedSymbols()
    print('defined funs:', DefinedFuns)
    # initialize the state in LED program memory
    initBody = Program.body('init',0)
    gammaDef = Definition('Gamma',[],initBody[1])
    # update Gamma in the program
    Program.update(gammaDef)
    images = [convert(x) for x in val(AST('display'))[1]]
    # Create a window to play in
    while(True):
        for x in images: x.draw(displayWindow)
        c = displayWindow.getMouse()
        click = (c.getX(),displaySize()[1] - c.getY())
        # update click in Program
        clickAST = AST('tuple',[click[0],click[1] ])
        clickDef = Definition('click',[],clickAST)
        Program.update(clickDef)
        # update newState in Program
        newStateBody = Program.body('newState',0)
        # convert the value of newState into a AST and put it as the body of Gamma
        gammaDef = Definition('Gamma',[],AST(val(AST('newState'))))
        Program.update(gammaDef)
        for I in images: I.undraw()
        images = [convert(x) for x in val(AST('display'))[1]]  
run()
