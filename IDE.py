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

import sys, os, pygame
from pygame.locals import *
from pygame.compat import geterror
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
                    try:
                        value = val(tree.expression())
                        if not value ==None:
                            if isinstance(value,Fraction):
                                value = numeralValue(value)
                            print(prettyString(value))
                        print()
                    except:
                        print('Failed to evaluate the expression. It is not a valid expression')
                    continue
                d,defFlag = parseDfn(expression)
                if defFlag:
                    #print('parsing #',i,"function successfully",' '.join(funcs[i]))
                    Program.update(d)
                else:
                    print('Failed to parse the expression or definition.')
            else:
                print('Failed to tokenize the expression.The last 10 valid tokens are',expression[-10:])

def play(F):
    # Initialize the game engine
    pygame.init()

    # Set the height and width of the screen
    size = [1000, 800]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("My Game")

    # compile LED program
    compile(F+'.led')
    DefinedFuns = Program.definedSymbols()
    print('defined funs:', DefinedFuns)
    print() 
    try:
        # initialize the initial state in LED program memory
        initBody = Program.body('initialState',0)
        initStateAST = initBody[1]
        # set the global variable state named "GAMMA" in LED memory
        gammaDef = Definition('GAMMA',[],initStateAST)
        Program.update(gammaDef)
    except KeyError:
        print("initialState is not defined in your LED program")
        return
    # draw the initial images before play
    images = val(AST('images',[initStateAST]).expression())
    if images ==None:
        print("Failed evaluating images")
        return
    else:
        drawImages(screen,images[1])
    done = False
    clock = pygame.time.Clock()
    while not done:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        # 60 frame per second
        clock.tick(60)
        clickAST = AST('`nil')
        keyboardAST = AST('set',[])
        keys=[]
        for event in pygame.event.get(): # User did something
            #clickAST = AST('tuple',[-1,-1])
            #clickAST = AST('`nil')
            #keyboardAST = AST('set',[])
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
                sys.exit()
            elif event.type == KEYDOWN:
                #clickAST = AST("`nil")
                if event.key == pygame.K_ESCAPE:
                    done=True
                    sys.exit()
                else:
                    keys.append(event.key);
            elif event.type == MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                # update click in Program
                clickAST = AST('tuple',[click[0],click[1]])
                #keyboardAST = AST('set',[])                
                # update input in Program
                #inputAST = AST('tuple',[clickAST,keyboardAST])
                #drawSreeen(screen,inputAST)
        if len(keys)>0:
            keyboardAST = AST('set',[AST('string',keys)])
        inputAST = AST('tuple',[clickAST,keyboardAST])
        drawSreeen(screen,inputAST)
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
 
# Be IDLE friendly
    pygame.quit()

def drawSreeen(screen,inputAST):
    # get the current state in the program
    currentStateAST = Program.body('GAMMA',0)[1]

    #print(inputAST)
    # update the state 
    transition = val(AST('transition',[inputAST,currentStateAST]).expression())
    if transition==None:
        print('transition is not defined in your LED program')
        return
    gammaDef = Definition('GAMMA',[],AST(transition))
    Program.update(gammaDef)

    # undraw the screen
    screen.blit(screen, (0, 0))
    currentStateAST = Program.body('GAMMA',0)[1]
    # draw the screen with current state
    images = val(AST('images',[currentStateAST]).expression())
    if images ==None:
        print("Failed evaluating images")
        return
    else:
        drawImages(screen,images[1])

run()
