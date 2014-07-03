'''
This program reads in a text file, stores its contents as a string 
(presumably consisting of function definitions separated by white space), 
tokenizes it, splits it up into its component definitions using the 'let' keywords, and stores them as a dict.

Function definitions have the following grammar: 
Dfn -> let identifier ( vars ) = Expression 
var -> identifier 
vars -> var | var , vars 
The definition f(x1,...,xn):= E is represented by the Python dictionary entry ('f',n) : ([x1,...,xn],E). 
For example, the following program let f(x) = x^2 let g(x,y) = y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
from src.Tokenizer import *
from src.ParserV9 import *
'''
string -> dict * bool
If F is the name of the file containing the function definitions of LED, then parseProgram(F) = (dict,True), where dict is a dictionary 
otherwise parseProgram(F) = (None,False)
For example, the following program let f(x) = x^2 let g(x,y) = y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
def parseProgram(F):
    program = {}
    # read the file as a string
    #programText = open(F).read()
    programText = ''.join([line.strip() for line in open(F)])
    #tokenize the file
    #print(programText)
    S,F = tokens(programText)
    if F:
        while(len(S)>0):
            #find the first 'let' in S
            firstLetIndex = S.index('let')
            # find the first '=' immediately after the first 'let'
            firstEqualIndex = S.index('=')
            # find the second 'let' in S 
            try:
                secondLetIndex = S[firstLetIndex+1:].index('let') + firstLetIndex+1
            except ValueError:
                #if cannot find the second 'let', then reach the last function definition of the program
                secondLetIndex = len(S)
            # parse the expression in between the first '=' and the second 'let'
            tree,flag = parseExpression(S[firstEqualIndex+1:secondLetIndex])
            # parse the left hand side of the function definition between the first 'let' and the first '='
            ((fName,fParams),flag2) = parseLHS(S[firstLetIndex+1:firstEqualIndex])
            if flag and flag2:
                paramNumber = len(fParams)
                #put the content in the dictionary
                program[(fName,paramNumber)] = (fParams,tree)
            # move to next function definition
            S= S[secondLetIndex:len(S)]
        return (program,True)
    return (None,False)  
'''
list<str> -> str * list<str>
If S is a list of string that comply to the format of the left hand side of the function definition, 
then parseLHS(S) = ((fName,fParams),True), where fname is a string and fParams is a list of strings
otherwise, parseLHS(S) = (None,False)
'''
def parseLHS(S):
    if isVar(S[0]) and S[1]=='(' and S[len(S)-1]==')':
        fName = S[0]
        S = S[2:len(S)-1]
        fParams = params(S)
        return ((fName,fParams),True)
    return (None,False)

'''
list<str> -> list<str>
If S is a list of string that comply to the format of the parameters of the function definition, 
then params(S) is a list of parameters of the function definition
otherwise, params(S) = []
'''
def params(S):
    return [p for p in S if not p==',']

print(parseProgram('program.txt'))
#print(parseProgram('program.txt'))
