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
     
    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)
     
    # Set the height and width of the screen
    size = [1000, 800]
    screen = pygame.display.set_mode(size)
     
    pygame.display.set_caption("My Game")
     
    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    global images, Gamma
    gammaDef = Definition('Gamma',[],AST('set',[]))
    Program.update(gammaDef)
    compile(F+'.led')
    DefinedFuns = Program.definedSymbols()
    print('defined funs:', DefinedFuns)
    # initialize the state in LED program memory
    initBody = Program.body('initialState',0)
    gammaDef = Definition('Gamma',[],initBody[1])
    # update Gamma in the program
    Program.update(gammaDef)
    #images = [convert(x) for x in val(AST('display').expression())[1]]
    #print(val(AST('images').expression()))
    draw(screen,val(AST('display').expression())[1])
    while not done:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        #clock.tick(10)
        #clickAST = AST('tuple',[0,1])
        #keyboardAST = AST('set',[1,2])
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            #elif event.type == KEYDOWN:
                #if event.key == pygame.K_ESCAPE:
                    #done=True
                    #sys.exit()
                #elif event.key ==pygame.K_LEFT:
                    #keyboardAST = AST('set',[AST("L")])
                #elif event.key ==pygame.K_RIGHT:
                    #keyboardAST = AST('set',[AST("R")])
            elif event.type == MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                # update click in Program
                clickAST = AST('tuple',[click[0],click[1]])
                keyboardAST = AST('set',[1,2])                
                # update input in Program
                inputAST = AST('tuple',[clickAST,keyboardAST])
                # convert the value of transition into a AST and put it as the body of Gamma
                gammaDef = Definition('Gamma',[],AST(val(AST('transition',[inputAST]).expression())))
                Program.update(gammaDef)
                # undraw the screen
                screen.blit(screen, (0, 0))
                # draw the screen
                draw(screen,val(AST('display').expression())[1])
        
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
 
# Be IDLE friendly
    pygame.quit()


run()
