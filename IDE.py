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
            s = timeit.default_timer()

            start_time = timeit.default_timer()
            expression,eFlag = tokens(e)
            elapsed = timeit.default_timer() - start_time
            print("Tokenizing time",elapsed)
            if eFlag:
                # building in commands
                if len(expression)==3:
                    if expression[0]=='quit' and expression[1]=='(' and expression[-1]==')': return
                    # turn on the type checking
                    if expression[0]=='TCon' and expression[1]=='(' and expression[-1]==')':
                        #TypeChecking = True
                        TypeChecking.on()
                        print("Type checking is turned on. The intepreter might run slow")
                        continue
                    # turn off the type checking
                    if expression[0]=='TCoff' and expression[1]=='(' and expression[-1]==')':
                        TypeChecking.off()
                        print("Type checking is turned off")                        
                        continue
                if len(expression)>3:
                    if expression[0]=='run' and expression[1]=='(' and expression[-1]==')':
                        return run(expression[2])
                    if expression[0]=='play' and expression[1]=='(' and expression[-1]==')':
                        return play(expression[2])
                start_time = timeit.default_timer()
                tree, tFlag = parseExpression(expression)
                elapsed = timeit.default_timer() - start_time
                print("Parsing time",elapsed)
                if tFlag:
                    try:
                        start_time = timeit.default_timer()
                        value = val(tree.expression())
                        elapsed = timeit.default_timer() - start_time
                        print("Evaluating time",elapsed)
                        if not value ==None:
                            start_time = timeit.default_timer()                            
                            if isinstance(value,Fraction):
                                value = numeralValue(value)
                            print(prettyString(value))
                            elapsed = timeit.default_timer() - start_time
                            print("pretty printing time",elapsed)
                            elapsed = timeit.default_timer() - s
                            print("total time",elapsed)
                        #print(dictionary.dic)
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
    #print('defined funs:', DefinedFuns)
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
        #clock.tick(1000)
        clickAST = AST('`nil')
        keyboardAST = AST('set',[])
        keys=[]
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done=True
                    sys.exit()
                else:
                    keys.append(event.key);
            elif event.type == MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                # update click in Program
                clickAST = AST('tuple',[click[0],size[1]-click[1]])
        if len(keys)>0:
            keyboardAST = AST('set',[AST('string',keys)])
        inputAST = AST('tuple',[clickAST,keyboardAST])
        drawSreeen(screen,inputAST)
        #if ~drawSreeen(screen,inputAST):
        #    return
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        
        # reset the dictionary if it reaches some limit to prevent memory leak
        if dictionary.length()>1000000:
            dictionary.clear()
        if dictionary.length()==0:
            print("limite")
        pygame.display.flip()
 
# Be IDLE friendly
    pygame.quit()

def drawSreeen(screen,inputAST):
    # get the current state in the program
    currentStateAST = Program.body('GAMMA',0)[1]
    #print out the first element in the state
    #print(prettyString(val(currentStateAST.expression())[1][0]))
    # update the state 
    #start_time = timeit.default_timer()
    
    transition = val(AST('transition',[inputAST,currentStateAST]).expression())
    if transition==None:
        print('transition is not defined in your LED program')
        return False
    gammaDef = Definition('GAMMA',[],AST(transition))
    Program.update(gammaDef)
    #elapsed = timeit.default_timer() - start_time
    #print("updating  time",elapsed)

    # undraw the screen
    screen.blit(screen, (0, 0))
    currentStateAST = Program.body('GAMMA',0)[1]
    # draw the screen with current state
    images = val(AST('images',[currentStateAST]).expression())
    if images ==None:
        print("Failed evaluating images")
        return False
    else:
        drawImages(screen,images[1])
    return True

run()
