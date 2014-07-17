'''
Qianji Zheng
July 2014
'''

from Tokenizer import tokens
from Evaluater import val
from Parser import *

'''    
string -> 
If F is the name of the file containing the function definitions of LED with .led as its extension, then compile(F) compile the functions in the file 
and update the content of the program in the global variable "Program"
otherwise 
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
def compile(F):
    global Program
    try:
        file = open(F)
        programText = open(F).read()
        file.close()
    except FileNotFoundError as e:
        print(e)
        return
    # read the file as a string
    t = removeComments(programText)
    #tokenize the file
    text,tokenF = tokens(t)
    #print(text)
    #text,tokenF = tokens(programText)
    if tokenF:
        # get a list of function definitions from text
        funcs= parseProgram(text)
        for i in range(len(funcs)):    
            p,programF = parseDfn(funcs[i])
            if programF:
                Program.update(p)
            else:
                print("Failed parsing #",i," program: ", ' '.join(funcs[i]))
                return
        # TODO:  Write program to log.txt instead of printing.
        # Separate the functions by line breaks.
    else:
        print("Failed to tokenize the program")

#compile('cp.txt')
#run()
#print(parseProgram(tokens('f(x) := x^2 g(x,y) := y+2*x')[0]))
#compile('conditional_program_test.txt')
