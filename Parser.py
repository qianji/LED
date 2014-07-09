######################################################################
# Parser

# Qianji Zheng
# July 2014
######################################################################

from Tokenizer import *
from Evaluater import *
'''
This simple parser program parses the following grammar:

'''
'''
A *node* is a string
An *AST* is either a 3-tuple (root,left,right), where root is a node, left and right are *AST*, or a node. 
If *AST* is a 3-tuple (r,l,r), it represents a abstract syntax tree with r as its root node, l its left tree and r its right tree
If *AST* is a node r, it represents an abstract syntax tree with r as its root node and no subtrees.
A *var* or an *identifier* is a nonempty string of letters and digits beginning with a letter.
A *num* is a nonempty string of digits
'''
''''''''''''''''''''''''''''''''''''''''''''
# All the functions in this file that starts with the word "parse" have the same signature as follows:
# list(string) -> AST * bool
# if S is a list of string then parse**(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the corresponding rule of the grammar
# otherwise parse**(S) = (None,False).
# Each rule is given right before the funtion definiton
''''''''''''''''''''''''''''''''''''''''''''

# rule: funcBody -> Expression | conditional
def parseFuncBody(S):
    tree2,flag2 = parseExpression(S)
    if flag2:
        return (tree2,True)
    tree1,flag1 = parseConditional(S)
    if flag1:
        return (tree1,True)
    return (None,False)

# rule: conditional -> ifClauses | ifClauses ; term otherwise
def parseConditional(S):
    if S[-1]=='otherwise':
        S = S[:-1]
        # find the last ';' of S
        i = lastIndex(';',S)
        (t2,f2)=parseIfClauses(S[0:i])
        (t1,f1)= parseTerm(S[i+1:])
        if f1 and f2: 
            if(t2[0]=='cond'):
                # add otherwise to the list of AST
                return (('cond',t2[1]+[('ow',[t1])]),True) 
            else:
                return (('cond',[t2,('ow',[t1])]),True) 

    tree1,flag1 = parseIfClauses(S)
    if flag1:
        return (tree1,True) 
    return (None,False)    

# rule: ifClasuses -> ifClause | ifClause ; ifClauses
def parseIfClauses(S):
    for i in range(len(S)):
        if S[i]==';':
            (t1,f1)=parseIfClause(S[0:i])
            (t2,f2)= parseIfClauses(S[i+1:])
            if f1 and f2: 
                if(isinstance(t2,tuple) and t2[0]=='cond'):
                    return (('cond',[t1]+t2[1]),True) 
                else:
                    return (('cond',[t1,t2]),True)
    (tree,flag) = parseIfClause(S)
    if flag: 
        return (tree,True)    
    return (None,False)    

# rule: ifClause -> term if statement
def parseIfClause(S):
    for i in range(len(S)):
        if S[i]=='if':
            (t1,f1)=parseTerm(S[0:i])
            (t2,f2)= parseSentence(S[i+1:])
            if f1 and f2: 
                return (('if',[t2,t1]),True) 
    return (None,False)    

'''
# str * list<str> -> int
# If C is a string and S is a list of string, lastIndex(C, S) is the index of the last C in S if there is at least C,
# otherwise lastIndex(C, S) = 0

'''
def lastIndex(C, S):
    index = 0
    for i in range(len(S)):
        if(S[i]==C):
            index = i
    return index
            
            
# Expression -> Sentence | Term
def parseExpression(S):
    tree2,flag2 = parseSentence(S)
    if flag2:
        return (tree2,True)
    tree1,flag1 = parseTerm(S)
    if flag1:
        return (tree1,True)
    return (None,False)

def parseSentence(S):
    return parseS6(S)

def parseS6(S):
    for i in range(len(S)):
        if S[i]=='<=>':
            (t1,f1)=parseS5(S[0:i])
            (t2,f2)= parseS6(S[i+1:])
            if f1 and f2: 
                return (('<=>',[t1,t2]),True) 
    (tree,flag) = parseS5(S)
    if flag: 
        return (tree,True)    
    return (None,False)

def parseS5(S):
    for i in range(len(S)):
        if S[i]=='=>':
            (t1,f1)=parseS4(S[0:i])
            (t2,f2)= parseS5(S[i+1:])
            if f1 and f2: 
                return (('=>',[t1,t2]),True) 
    (tree,flag) = parseS4(S)
    if flag: 
        return (tree,True)    
    return (None,False)

def parseS4(S):
    for i in range(len(S)):
        if S[i]=='or':
            (t1,f1)=parseS4(S[0:i])
            (t2,f2)= parseS3(S[i+1:])
            if f1 and f2: 
                return (('or',[t1,t2]),True) 
    (tree,flag) = parseS3(S)
    if flag: 
        return (tree,True)    
    return (None,False)

def parseS3(S):
    for i in range(len(S)):
        if S[i]=='&':
            (t1,f1)=parseS3(S[0:i])
            (t2,f2)= parseS2(S[i+1:])
            if f1 and f2: 
                return (('and',[t1,t2]),True) 
    (tree,flag) = parseS2(S)
    if flag: 
        return (tree,True)    
    return (None,False)

def parseS2(S):
    if len(S)==0:
        return (None,False)
    if S[0]=='~':
        (t1,f1)= parseS2(S[1:])
        if f1: 
            return (('~',[t1]),True) 
    (tree,flag) = parseS0(S)
    if flag: 
        return (tree,True)    
    return (None,False)

InfpredS0 = ['=','<','>','<=','>=','in','subeq']
def parseS0(S):
    if len(S)==0: return(None,False)
    for i in range(len(S)):
        for infpred in InfpredS0:
            if S[i]==infpred:
                (t1,f1)=parseTerm(S[0:i])
                (t2,f2)= parseTerm(S[i+1:])
                if f1 and f2: 
                    return ((infpred,[t1,t2]),True)    
    # (Sentence)
    if S[0]=='(' and S[len(S)-1]==')':
        (tree,flag)=parseSentence(S[1:len(S)-1])
        if flag: return (tree,True)
    # prerel (terms)
    if S[len(S)-1] ==')':
        (tree,flag) = parseUserDefinedFun(S)
        if flag: return (tree,True)
    return (None,False)      

def parseTerm(S):
    return parseT4(S)

# rule: T4   ->  T3   |   T4 Infix4 T3
InfixT4 = ['+','-','union','\\']
def parseT4(S):
    for i in range(len(S)):
        for infix in InfixT4:
            if S[i]==infix:
                (t1,f1)=parseT4(S[0:i])
                (t2,f2)= parseT3(S[i+1:])
                if f1 and f2: 
                    return ((infix,[t1,t2]),True) 
    (tree,flag) = parseT3(S)
    if flag: 
        return (tree,True)    
    return (None,False)   

# rule: T3   ->  T2   |   T3 Infix3 T2  
InfixT3 = ['*','/','mod','nrsec',]
def parseT3(S):
    for i in range(len(S)):
        for infix in InfixT3:
            if S[i]==infix:
                (t1,f1)=parseT3(S[0:i])
                (t2,f2)= parseT2(S[i+1:])
                if f1 and f2: 
                    return ((infix,[t1,t2]),True) 
    (tree,flag) = parseT2(S)
    if flag: 
        return (tree,True)    
    return (None,False)

PrefixT2 = ['+','-']
def parseT2(S):
    if len(S)==0:
        return (None,False)
    for prefix in PrefixT2:
        if S[0]==prefix:
            (t,f)= parseT2(S[1:])
            if f: 
                return ((prefix+'1',[t]),True) 
    (tree,flag) = parseT1(S)
    if flag: 
        return (tree,True)    
    return (None,False)    

# rule: T1 -> T0 | vector [term]  | T0  ^  T1
InfixT1 = ['^']
def parseT1(S):
    if len(S)==0:
        return (None,False)
    # T1[term]
    if S[-1] == ']':
        # search back forward from the end of S to find the first [ 
        lb = firstIndexBack('[',len(S)-1,S)
        if lb ==None:
            return (None,False)
        else:
            t1,f1 = parseT1(S[:lb])
            t2,f2 = parseTerm(S[lb+1:len(S)-1])
            if f1 and f2:
                return (('sub',[t1,t2]),True)
    # T0 ^ T1
    for i in range(len(S)):
        for infix in InfixT1:
            if S[i]==infix:
                (t1,f1)=parseT0(S[0:i])
                (t2,f2)= parseT2(S[i+1:])
                if f1 and f2: 
                    return ((infix,[t1,t2]),True) 
    # T0
    (tree,flag) = parseT0(S)
    if flag: 
        return (tree,True)    
    return (None,False) 
    
'''
# list(string) -> AST * bool
# if S is a list of string then parseT0(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to rule T0 of the grammar
# otherwise parseE0(S) = (None,False).
#rule 0: T0 -> numeral | identifier | (term) | pipe term pipe | floor(term) | ceil(term) | prefun(terms) | vector | set | tuple | Pow (vector) | choose(vector)
'''
def parseT0(S):
    if len(S)==0:
        return (None,False)
    try:
        # (term)
        if S[0]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[1:len(S)-1])
            if flag: return (tree,True)
        # |term|
        if S[0]=='|' and S[len(S)-1]=='|':
            (tree,flag)=parseTerm(S[1:len(S)-1])
            if flag: return (('pipes',[tree]),True)        
        # floor ( term )
        if S[0]=='floor' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[2:len(S)-1])
            if flag: return (('floor',[tree]),True)   
        # ceil ( term )
        if S[0]=='ceil' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[2:len(S)-1])
            if flag: return (('ceil',[tree]),True)
        # Pow(vector)
        if S[0]=='Pow' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseVector(S[2:len(S)-1])
            if flag: return (('pow',[tree]),True)
        # choose(vector)
        if S[0]=='choose' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseVector(S[2:len(S)-1])
            if flag: return (('choose',[tree]),True)
        # prefun (terms)
        if S[len(S)-1] ==')':
            (tree,flag) = parseUserDefinedFun(S)
            if flag: return (tree,True)
        if len(S)==1: 
            # numeral    
            if isNumeral(S[0]): return (eval(S[0]),True)
            # identifier
            if isIdentifier(S[0]): return (S[0],True)
         # parse vector   
        (tree,flag) = parseVector(S)
        if flag: return (tree,True)
         # parse set   
        (tree,flag) = parseSet(S)
        if flag: return (tree,True)
        # parse tuple
        (tree,flag) = parseTuple(S)
        if flag: return (tree,True)
    except IndexError:
        return(None,False) 
    return (None,False)
'''
# list(string) -> AST * bool
# if S is a list of string then parseUserDefinedFun(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the following rule of the grammar
# otherwise parseUserDefinedFun(S) = (None,False).
# rule: T0 -> prefun ( terms )
'''
def parseUserDefinedFun(S):
    try:
        if S[len(S)-1] ==')':
            # find the first index of '(' in S. It throws ValueError if '(' is not in S
            i = S.index('(') 
            (t1,f1)=parsePrefun(S[0:i])
            (t2,f2)= parseTerms(S[i+1:len(S)-1])
            if f1 and f2: 
                if(isinstance(t2,tuple) and t2[0]=='cstack'):
                    return ((t1,t2[1]),True) 
                else:
                    return ((t1,[t2]),True)
    except ValueError:
        return(None,False)         
    return (None,False)
'''
# list(string) -> AST * bool
# if S is a list of string then parsePrefun(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the following rule of the grammar
# otherwise parsePrefun(S) = (None,False).
# rule: prefun -> identifier
'''
def parsePrefun(S):
    if(len(S)==1):
        if isIdentifier(S[0]):
            return (S[0],True)
    return (None,False)

'''
# list(string) -> AST * bool
# if S is a list of string then parseTerms(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the following rule of the grammar
# otherwise parseTerms(S) = (None,False).
# rule: terms -> term | term , terms
'''
def parseTerms(S):
    for i in range(len(S)):
        if S[i]==',':
            (t1,f1)=parseTerm(S[0:i])
            (t2,f2)= parseTerms(S[i+1:])
            if f1 and f2: 
                if(isinstance(t2,tuple) and t2[0]=='cstack'):
                    return (('cstack',[t1]+t2[1]),True) 
                else:
                    return (('cstack',[t1,t2]),True)
    (tree,flag) = parseTerm(S)
    if flag: 
        return (tree,True)    
    return (None,False)     
     
'''
# str -> bool
# isIdentifier(S) iff S is an *identifier*
'''
def isIdentifier(S):
    if not alpha(S[0]): return False
    for c in S:
        if not (alphaNum(c)): return False
    return True

'''
# string -> bool
# isNumeral(S) iff S is a *numeral*
'''
def isNumeral(S):
    for c in S:
        if not (digit(c) or c=='.'): return False
    return True

    
'''
#  AST -> bool
If T is an AST, then hasIdentifier(T) iff there is at least one indentifier in T
'''    
def hasIdentifier(T):
    if isScalar(T): return False
    if isIdentifier(T): return True
    (Op,X) = T
    for i in X:
        if hasIdentifier(i):
            return True

    return False
    
'''
value(S) is used for unit testing
'''
def value(S):
    (S,f1) = tokens(S)
    tree,f2 = parseExpression(S)
    v = val(tree)
    return v

'''
string -> dict * bool
If S is a string of the function definitions of funcDef or relDef defined in LED, then parseDfn(S) = (dict,True), where dict is a dictionary 
otherwise parseDfn(S) = (None,False)
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
'''
# Dfn -> funcDef | relDef
'''
def parseDfn(S):
    program2,flag2 = parseFuncDef(S)
    if flag2:
        return (program2,True)
    program1,flag1 = parseRelDef(S)
    if flag1:
        return (program1,True)
    return (None,False)  

'''
string -> dict * bool
If S is a string of the function definitions of funcDef defined in LED, then parseFuncDef(S) = (dict,True), where dict is a dictionary 
otherwise parseFuncDef(S) = (None,False)
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
# funcDef -> identifier ( vars )  :=   funcBody
'''
def parseFuncDef(S):
    program = {}
    for i in range(len(S)):
        if S[i]==':=':
            ((fName,fParams),f1)=parseLHS(S[0:i])
            (t2,f2)= parseFuncBody(S[i+1:])
            if f1 and f2: 
                paramNumber = len(fParams)
                #put the content in the dictionary
                program[(fName,paramNumber)] = (fParams,t2)
                return(program,True)     
    return (None,False)     

'''
string -> dict * bool
If S is a string of the function definitions of relDef defined in LED, then parseRelDef(S) = (dict,True), where dict is a dictionary 
otherwise parseRelDef(S) = (None,False)
'''

'''
# relDef -> identifier ( vars ) iff   sentence
'''
def parseRelDef(S):
    program = {}
    for i in range(len(S)):
        if S[i]=='iff':
            ((fName,fParams),f1)=parseLHS(S[0:i])
            (t2,f2)= parseSentence(S[i+1:])
            if f1 and f2: 
                paramNumber = len(fParams)
                #put the content in the dictionary
                program[(fName,paramNumber)] = (fParams,t2)
                return(program,True)     
    return (None,False) 
'''
###
This is the candidate program using the format of keyword 'let'. To be deleted
###
string -> dict * bool
If S is string of the function definitions of LED, then parseProgram(S) = (dict,True), where dict is a dictionary 
otherwise parseProgram(S) = (None,False)
For example, the following program let f(x) = x^2 let g(x,y) = y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
def parseProgramLet(S):
    program = {}
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
        #tree,flag = parseExpression(S[firstEqualIndex+1:secondLetIndex])
        tree,flag = parseFuncBody(S[firstEqualIndex+1:secondLetIndex]) 
        # parse the left hand side of the function definition between the first 'let' and the first '='
        ((fName,fParams),flag2) = parseLHS(S[firstLetIndex+1:firstEqualIndex])
        if flag and flag2:
            paramNumber = len(fParams)
            #put the content in the dictionary
            program[(fName,paramNumber)] = (fParams,tree)
            # move to next function definition
            S= S[secondLetIndex:len(S)]
        else:
            # print the message
            return (None,False)
    return (program,True)


'''
# string -> list< list<string> >
# if S is a string of the program that has f1, f2, ... fn functions, then parseProgram(S)=[L1, L2, ... Ln], where L1... Ln 
# are lists of corresponding function to f1, f2,... fn.
'''
def parseProgram(S):
    allFunctions = []
    separators = ['iff',':=']
    lpI = 0
    while len(S)>0:
        # find the first iff or := in S
        firstI = firstIndex(separators,S)
        # find the second iff or := in S
        secondI = firstIndex(separators,S[firstI+1:])
        # if there is only one iff or :=
        if secondI==None:
            allFunctions.append(S)
            S=[]
        else:
            secondI += firstI
            # search backward from secondI to find the first '('
            lpI = firstIndexBack('(',secondI,S)
            # find the end of the first function defintion
            end = lpI -2 
            eachFunc = S[:end+1]
            allFunctions.append(eachFunc)
            if end+1==0:
                S = []
            else:
                S = S[end+1:]
    return allFunctions

'''
firstIndexBack(C, secondeI, S) searches backward from index of secondI of S to find the first C in S
'''        
def firstIndexBack(C,secondI,S):
    for i in range(secondI,-1, -1):
        if S[i]==C:
            return i
    return None
'''
# lsit<str> * list<str> -> int
# If Cs is a list of string and S is a list of string, firstIndex(C, S) is the first index of one of the member of C in S,
# otherwise firstIndex(Cs, S) = len(S) 

'''
def firstIndex(Cs, S):
    index = 0
    for i in range(len(S)):
        for C in Cs:
            if(S[i]==C):
                return i
    return None

'''
list<str> -> str * list<str>
If S is a list of string that comply to the format of the left hand side of the function definition, 
then parseLHS(S) = ((fName,fParams),True), where fname is a string and fParams is a list of strings
otherwise, parseLHS(S) = (None,False)
'''
def parseLHS(S):
    if isIdentifier(S[0]) and S[1]=='(' and S[len(S)-1]==')':
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

'''

'''
'''
# Program -> set
# If P is a program, then definedFuns(P) is a set of function named defined in P.
'''
def definedFuns(P):
    return {Def[0] for Def in P}

# canPushParser(S,state) iff, in the current state S with the current stack stk,
# stk+[S[0]] is the beginning of a token.

def canPushParser(S,state):
    if S==[]: return False
    if state =='success': return False
    if state == 'spec1' : return False
    c=S[0]
    if state == 'empty': 
        return c == '{'
    if state == 'lb': return c=='d' or white(c)
    if state=='d': return 'e'
    if state == 'e': return c=='f'
    if state == 'f': return white(c) or c == 's'
    if state == 's': return white(c)
    if state =='w1' : return c=='d' or white(c)
    if state == 'w2' : return 'w2'
    return False

# If canpushParser(S,state) and c=S[0], the newState(state,c) is the
# state resulting from pushing c onto the stack.

def newStateParser(state,c):
    if state == 'empty':
        return 'lb' if c=='{' else \
               'spec1'  
    if state =='lb':return 'd' if c =='d' else 'lb' if white(c) else 'spec1'
    if state == 'd': return 'e' if c=='e' else 'spec1'
    if state == 'e': return 'f' if c=='f' else 'spec1'
    if state == 'f': return 's' if c=='s' else 'w2' if white(c) else 'spec1'
    if state == 's': return 'w2' if white(c) else 'spec1'
    if state =='w2': return 'w2' if white(c) else 'success'

'''
# string -> list< list<string> >
# if S is a string of the program that has f1, f2, ... fn functions and 0 or more comments, then parseProgram(S)=[L1, L2, ... Ln], where L1... Ln 
# are lists of corresponding function to f1, f2,... fn.
'''
        
'''
# If S is a string, then firstFuncHead(S)=(s,e), where s is the first index of { followed by 0 or more white space 
# and followed by 'def' or 'defs' and 0 or more white spaces and e is the first non white space character after 'def' or 'defs'
# For example, if S = '{defs daf}' then firstFuncHead(S) = (0,7)
'''
def firstFuncHead(S):
    for i in range(len(S)):
        if S[i]=='{':
            state = 'empty'
            temp = list(S[i:])
            end = i
            while canPushParser(temp,state):
                state = newStateParser(state,temp[0])
                temp.pop(0)
                end= end +1
            if state == 'success':
                return (i,end)
    return None

'''
If S is a string, then removeComments(S) is a string that does not have any comments in S
'''
def removeComments(FS):
    S = FS
    allFunctionsText = ''
    while len(S)>0:
        # find the first {def or {defs S
        firstLb = firstFuncHead(S)
        if firstLb == None:
            S= []
        else:
            # find the first } after firstLb that is not in the function definition
            #firstRb = firstIndex(separators,S[firstLb[1]:])+firstLb[1]
            firstRb = closeParentesis(S[firstLb[1]:])+firstLb[1]
            allFunctionsText += S[firstLb[1]-1: firstRb] + '  '
            S = S[firstRb+1:]
    return allFunctionsText
'''
This is a function definition: {def f(x) = {x}+{x+2} }
closeParentesis(S) finds the first } that does not match any { in S
'''
def closeParentesis(S):
    S = list(S)
    #create an empty stack S
    index = 0
    stack = []
    while(len(S)>0):
        # read a character ch
        ch = S[0]
        #If ch is an opening paren (of any kind), push it onto stack
        if ch =='{':
            stack.append(ch)
        else:
            # If  ch  is a closing paren }, look at the top of stack.
            if ch=='}':
                #If stack is empty at this point, retrun index.
                if len(stack)==0:
                    return index
                top = stack[-1]
                # If the top of stack is the opening paren that corresponds to {, 
                # then pop stack and continue, this paren matches OK.
                if top=='{':
                    stack=stack[:-1]
                    S=S[1:]
                    index+=1
                    continue
                else:
                    return index   
        S=S[1:]
        index+=1 
    return None    
            
# vector -> <  >  | <  terms >
def parseVector(S):
    if len(S)<2:
        return (None,False)
    # < >
    if len(S)==2:
        if (S[0]=='<' and S[1]=='>'):
            return (('vector',[]),True)
    # <term>
    if S[0]=='<' and S[len(S)-1]=='>':
        (tree,flag)=parseTerms(S[1:len(S)-1])
        if flag: 
            if(isinstance(tree,tuple) and tree[0]=='cstack'):
                return (('vector',tree[1]),True)
            else:
                return(('vector',[tree]),True)
 
    return (None,False)
    
# set -> {  }  | { terms }
def parseSet(S):
    if len(S)<2:
        return (None,False)
    # {}
    if len(S)==2:
        if (S[0]=='{' and S[1]=='}'):
            return (('set',[]),True)
    # {term}
    if S[0]=='{' and S[len(S)-1]=='}':
        (tree,flag)=parseTerms(S[1:len(S)-1])
        if flag: 
            if(isinstance(tree,tuple) and tree[0]=='cstack'):
                return (('set',tree[1]),True)
            else:
                return(('set',[tree]),True)
 
    return (None,False)

    
# set -> | ( terms )
def parseTuple(S):
    if len(S)<2:
        return (None,False)
    # {term}
    if S[0]=='(' and S[len(S)-1]==')':
        (tree,flag)=parseTerms(S[1:len(S)-1])
        if flag: 
            if(isinstance(tree,tuple) and tree[0]=='cstack'):
                return (('tuple',tree[1]),True)
            else:
                return(('tuple',[tree]),True)
 
    return (None,False)

def main():  
    while True:
        i = input('please input your expression:')
        (S,f1) = tokens(i)
        if f1: 
            tree,f2 = parseExpression(S)
            if f2:
                print('The abstract syntax tree of your expression is',tree)
                '''
                if hasIdentifier(tree):    
                    x= eval(input('please input a number for x: '))
                    print(val(sub(x,'x',tree)))
                else:
                    print(val(tree))
                '''
            else:
                print("Wrong input format, cannot parse the input")
        else:
            print("cannot tokenize the input")
#main()      
#print(parseTerms(tokens('2+2,3,x2')[0]))
#print(isIdentifier('2'))