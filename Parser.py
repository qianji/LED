######################################################################
# Parser
# Qianji Zheng, Texas Tech University
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
'''
# All the functions in this file that starts with the word "parse" have the same signature as follows if their function signatures are not provided:
# list(string) -> AST * bool
# If S is a list of string then parse**(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the corresponding rule of the grammar
# otherwise parse**(S) = (None,False).
# Each rule is given right before the function definition
'''

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
            # statement and sentence are used interchangely 
            (t2,f2)= parseSentence(S[i+1:])
            if f1 and f2: 
                return (('if',[t2,t1]),True) 
    return (None,False)    

'''
# helper function
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

# rule: Sentence -> S6
def parseSentence(S):
    return parseS6(S)

# rule: S6 -> S5    |   S5 <=>  S6
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

# rule: S5  ->   S4    |   S4 =>  S5
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

# rule: S4  > S3     |   S4  or  S3
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

# rule: S3  ->  S2     |   S3  &  S2
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

#rule: S2  ->  S0   |  ~ S2
def parseS2(S):
    if len(S)==0:
        return (None,False)
    if S[0]=='~':
        (t1,f1)= parseS2(S[1:])
        if f1: 
            return (('~',[t1]),True) 
    (tree,flag) = parseS1(S)
    if flag: 
        return (tree,True)    
    return (None,False)

#rule S1 -> S0    |   some  var  in  term : S1    |   all   var  in  term : S1
def parseS1(S):
    # some  var  in  term : S1 | all   var  in  term : S1
    (tree,flag) = parseSomeAll(S)
    if flag: 
        return (tree,True)    
    # S0
    (tree,flag) = parseS0(S)
    if flag: 
        return (tree,True)    
    return (None,False)

# rule: some  var  in  term : S1 | all   var  in  term : S1
def parseSomeAll(S):
    separators = ['some','all']
    if len(S)<6:
        return(None,False)
    if S[0] in separators:
        try:
            i = S.index('in')
            j = S.index(':')
            t1,f1 = parseVar(S[1])
            t2,f2 = parseTerm(S[i+1:j])
            t3,f3 = parseS1(S[j+1:])
            if f1 and f2 and f3:
                return (S[0],[t1,t2,t3])
        except ValueError:
            return (None,False)
    return (None,False)
#rule S0  ->   term   infpred   term 
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

# rule: term  ->   T4  | lambda  vars . term
def parseTerm(S):
    t,f = parseT4(S)
    if f:
        return parseT4(S)
    t1,f1 = parseLambda(S)
    if f1:
        return parseLambda(S)
    return (None,False)

# rule: term -> lambda  vars . term
def parseLambda(S):
    if len(S)<4:
        return (None,False)
    if S[0]=='lambda':
        try:
            # find '.' in S
            i = S.index('.')
        except ValueError:
            return (None,False)
        (t1,f1)=parseVars(S[1:i])
        (t2,f2)= parseTerm(S[i+1:])
        if f1 and f2: 
            if isinstance(t1,tuple) and t1[0]=='cstack':
                return (('lambda',[t1[1],t2]))
            else:
                return (('lambda',[[t1],t2]),True) 
    return (None,False)
# rule: vars -> var | var vars        
def parseVars(S):
    if len(S)==1:
        (tree,flag) = parseVar(S)
        if flag: 
            return (tree,True)  
    (t1,f1)=parseVar(S[0])
    (t2,f2)= parseVars(S[1:])
    if f1 and f2: 
        if(isinstance(t2,tuple) and t2[0]=='cstack'):
            return (('cstack',[t1]+t2[1]),True) 
        else:
            return (('cstack',[t1,t2]),True)
    return (None,False)
# rule: var
def parseVar(S):
    if len(S)==1:
        if isIdentifier(S):
            return (S[0],True)
    return (None,False)     
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

# rule: T2   ->  T1   |  Prefix2  T2
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

# rule: T1 -> T0 | T1 [term]  | T0  ^  T2
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
    # T0 ^ T2
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
    
#rule 0: T0 -> numeral | identifier | (term) | pipe term pipe | floor(term) | ceil(term) | prefun(terms) | 
#              vector | set | tuple | Pow (vector) | choose(vector)| { term .. term } | { term pipe Stmt }
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
        # parse range { term .. term }
        (tree,flag) = parseRange(S)
        if flag: return (tree,True)
        # parse { term pipe Stmt }
        (tree,flag) = parseTermPipeStmt(S)
        if flag: return (tree,True)
    except IndexError:
        return(None,False) 
    return (None,False)

# rule: T0 -> prefun ( terms )
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

# rule: prefun -> identifier
def parsePrefun(S):
    if(len(S)==1):
        if isIdentifier(S[0]):
            return (S[0],True)
    return (None,False)

# rule: terms -> term | term , terms
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
# helper function
# str -> bool
# isIdentifier(S) iff S is an *identifier*
'''
def isIdentifier(S):
    if not alpha(S[0]): return False
    for c in S:
        if not (alphaNum(c)): return False
    return True

'''
# helper function
# string -> bool
# isNumeral(S) iff S is a *numeral*
'''
def isNumeral(S):
    for c in S:
        if not (digit(c) or c=='.'): return False
    return True
    
'''
# helper function
#  AST -> bool
# If T is an AST, then hasIdentifier(T) iff there is at least one indentifier in T
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
string -> dict * bool
If S is a string of the function definitions of funcDef or relDef defined in LED, then parseDfn(S) = (dict,True), where dict is a dictionary 
otherwise parseDfn(S) = (None,False)
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
'''
# rule: Dfn -> funcDef | relDef
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
#rule: funcDef -> identifier ( vars )  :=   funcBody
'''
def parseFuncDef(S):
    program = {}
    for i in range(len(S)):
        if S[i]==':=':
            t1,f1 = parseLHS(S[0:i])
            if f1:
                (fName,fParams)=parseLHS(S[0:i])[0]
                paramNumber = len(fParams)
                (t2,f2)= parseFuncBody(S[i+1:])
                if f2: 
                    #put the content in the dictionary
                    program[(fName,paramNumber)] = (fParams,t2)
                    return(program,True)    
                else:
                    print('cannot parse function definition right side: ',' '.join(S[i+1:])) 
            else:
                    print('cannot parse function definition left side: ',' '.join(S[0:i])) 
    return (None,False)     

# relDef -> identifier ( vars ) iff   sentence
def parseRelDef(S):
    program = {}
    for i in range(len(S)):
        if S[i]=='iff':
            t1,f1 = parseLHS(S[0:i])
            if f1:
                (fName,fParams)=parseLHS(S[0:i])[0]
                paramNumber = len(fParams)
                (t2,f2)= parseSentence(S[i+1:])
                if f2: 
                    #put the content in the dictionary
                    program[(fName,paramNumber)] = (fParams,t2)
                    return(program,True)    
                else:
                    print('cannot parse function definition right side: ',' '.join(S[i+1:])) 
            else:
                    print('cannot parse function definition left side: ',' '.join(S[0:i]))    
    return (None,False) 

'''
# string -> list< list<string> >
# if S is a string of the program that has f1, f2, ... fn functions, then parseProgram(S)=([L1, L2, ... Ln],True), where L1... Ln 
# are lists of corresponding function to f1, f2,... fn.
'''
def parseProgram(S):
    allFunctions = []
    separators = ['iff',':=']
    lpI = 0
    while len(S)>0:
        # find the first iff or := in S
        firstI = firstIndex(separators,S)
        if firstI ==None:
            allFunctions.append(S)
            S=[]
        else:
            # find the second iff or := in S
            secondI = firstIndex(separators,S[firstI+1:])
            # if there is only one iff or :=
            if secondI==None:
                allFunctions.append(S)
                S=[]
            else:
                # secondeI is the index-1 of the second iff or := in S
                secondI += firstI
                # if there are no '(' or ')'  in the function head
                if not S[secondI] ==')':
                    lpI =secondI+1
                else:
                    # search backward from secondI to find the first '('
                    lpI = firstIndexBack('(',secondI,S)
                # find the end of the first function definition
                end = lpI -2 
                eachFunc = S[:end+1]
                allFunctions.append(eachFunc)
                if end+1==0:
                    S = []
                else:
                    S = S[end+1:]
    return allFunctions

'''
# helper function
# char * int * str -> int
firstIndexBack(C, secondeI, S) searches backward from index of secondI of S to find the first C in S
'''        
def firstIndexBack(C,secondI,S):
    for i in range(secondI,-1, -1):
        if S[i]==C:
            return i
    return None

'''
# helper function
# str * list<str> -> int
# If Cs is a string and S is a list of string, firstIndex(Cs, S) is the first index of one of the member of Cs in S,
# otherwise firstIndex(Cs, S) = None

'''
def firstIndex(Cs, S):
    index = 0
    for i in range(len(S)):
        for C in Cs:
            if(S[i]==C):
                return i
    return None

'''
list<str> -> (str * list<str>) * bool
If S is a list of string that comply to the format of the left hand side of the function definition, 
then parseLHS(S) = ((fName,fParams),True), where fname is a string and fParams is a list of strings
otherwise, parseLHS(S) = (None,False)
'''
def parseLHS(S):
    if len(S)==1 and isIdentifier(S[0]):
        return ((S[0],[]),True)
    if isIdentifier(S[0]) and S[1]=='(' and S[len(S)-1]==')':
        fName = S[0] # the name of the function
        # f()
        if len(S)==3:
            return ((fName,[]),True)
        t,f = parseTerms(S[2:-1])
        if f:
            S = S[2:len(S)-1]
            fParams = params(S)
            return ((fName,fParams),True)
    return (None,False)

'''
# helper function
list<str> -> list<str>
If S is a list of string that comply to the format of the parameters of the function definition, 
then params(S) is a list of parameters of the function definition
otherwise, params(S) = []
'''
def params(S):
    return [p for p in S if not p==',']

'''
# Program -> set
# If P is a program, then definedFuns(P) is a set of function named defined in P.
'''
def definedFuns(P):
    return {Def[0] for Def in P}

# helper function for removeComments
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
'''
# helper function for removeComments
# If canpushParser(S,state) and c=S[0], the newState(state,c) is the
# state resulting from pushing c onto the stack.
'''
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
str -> str
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
# helper function for removeComments
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
            
# rule: vector -> <  >  | <  terms >
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
    
# rule: set -> {  }  | { terms }
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

    
# rule: set -> | ( terms )
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

# rule: T0 ->  { term .. term }
def parseRange(S):
    if len(S)<5:
        return (None,False)
    # {term}
    if S[0]=='{' and S[len(S)-1]=='}':
        # find the first index of '..' in S
        try:
            i = S.index('..')
        except ValueError:
            return (None,False)
        (t1,f1)= parseTerm(S[1:i])
        (t2,f2)=parseTerm(S[i+1:-1])
        if f1 and f2: 
            return(('intRange',[t1,t2]),True)
    return (None,False)

# rule: T0 -> { term pipe Stmt }
def parseTermPipeStmt(S):
    if len(S)<5:
        return (None,False)
    # {term}
    if S[0]=='{' and S[len(S)-1]=='}':
        # find the first index of '..' in S
        try:
            i = S.index('|')
        except ValueError:
            return (None,False)
        (t1,f1)= parseTerm(S[1:i])
        (t2,f2)=parseSentence(S[i+1:-1])
        if f1 and f2: 
            return(('setComp',[t1,t2]),True)
    return (None,False)
#print(parseTerms(tokens('2+2,3,x2')[0]))
#print(isIdentifier('2'))
