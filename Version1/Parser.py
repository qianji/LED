######################################################################
# Parser
# Qianji Zheng, Texas Tech University
# July 2014
######################################################################

from Tokenizer import *
from Evaluater import *
from Utility import *
'''
This simple parser program parses the following grammar:

'''
'''
A *node* is a string
An *AST* is either a 3-tuple (root,left,right), where root is a node, left and right are *AST*, or a node. 
If *AST* is a 3-tuple (r,l,r), it represents a abstract syntax tree with r as its root node, l its left tree and r its right tree
If *AST* is a node r, it represents an abstract syntax tree with r as its root node and no subtrees.
A *var* or an *identifier* is a nonempty string of letters and digits beginning with a letter.
A *numeral* is a nonempty string of digits
An *atom* is an identifier preceded by a backquote, such as `x and `o.
'''
'''
# All the functions in this file that starts with the word "parse" have the same signature as follows if their function signatures are not provided:
# list(string) -> AST * bool
# If S is a list of string then parse**(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the corresponding rule of the grammar
# otherwise parse**(S) = (None,False).
# Each rule is given right before the function definition
'''
'''
string -> dict * bool
If S is a string of the function definitions of funcDef or relDef defined in LED, then parseDfn(S) = (dict,True), where dict is a dictionary 
otherwise parseDfn(S) = (None,False)
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
'''
# rule: Dfn -> funcDef | relDef | ifThenDef
'''
def parseDfn(S):
    program3,flag3 = parseIfThenDef(S)
    if flag3:
        return (program3,True)
    program2,flag2 = parseFuncDef(S)
    if flag2:
        return (program2,True)
    program1,flag1 = parseRelDef(S)
    if flag1:
        return (program1,True)

    return (None,False) 

'''
string -> dict * bool
If S is a string of the function definitions of IfThenDef defined in LED, then parseIfThenDef(S) = (dict,True), where dict is a dictionary 
otherwise parseIfThenDef(S) = (None,False)
For example, the following program If x=2 & y=3 then h := x+y  would be represented by the following dictionary: 
{('h',0):([],('+',[2,3]))} 
#rule: IfThenDef -> If sentence then funcDef
'''
def parseIfThenDef(S):
    program = {}
    try:
        i = S.index('If')
        j = S.index('then')
    except ValueError:
        return(None,False)
    t1,f1 = parseSentence(S[i+1:j])
    if f1:
        (p,f2)= parseFuncDef(S[j+1:])
        if f2: 
            #put the content in the dictionary
            key,value = p.popitem()
            #sub the expression
            #print(t1)
            b = solutionSet(t1)
            if b==None or len(b)==0:
                expr = value[1]
            else:
                expr = subExpression(value[1],b[0])
            program[key] = (value[0],expr)
            return(program,True)    
        else:
            print('cannot parse then statement definition: ',' '.join(S[j+1:])) 
    else:
            print('cannot parse if statement definition: ',' '.join(S[i+1:j])) 
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
# duplicate with parseFuncDef. To be refactored soon
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
 

# rule: funcBody -> Expression | conditional
def parseFuncBody(S):
    tree1,flag1 = parseConditional(S)
    if flag1:
        return (tree1,True)
    tree2,flag2 = parseExpression(S)
    if flag2:
        return (tree2,True)
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

# rule: Sentence -> S6 | ( S6 )
def parseSentence(S):
    tree2,flag2 = parseS6(S)
    if flag2:
        return (tree2,True)
    if S[0]=='(' and S[-1]==')':
        tree1,flag1 = parseS6(S[1:-1])
        if flag1:
            return (tree1,True)
    return (None,False)

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

#rule: S2  ->  S1   |  ~ S2
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

#rule S1 -> S0    |   some  var  in  term : S2    |   all   var  in  term : S2
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

# rule: some  var  in  term : S2 | all   var  in  term : S2
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
            t3,f3 = parseS2(S[j+1:])
            if f1 and f2 and f3:
                return ((S[0],[t1,t2,t3]),True)
        except ValueError:
            return (None,False)
    return (None,False)
#rule S0  ->   term   infpred   term | identifier | consecutives
InfpredS0 = ['=','<','>','<=','>=','in','subeq']
def parseS0(S):
    if len(S)==0: return(None,False)
    # parse identifier
    if len(S)==1:
        if isIdentifier(S[0]):
            return (S[0],True)
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
    if len(S)>=5:
        (tree,flag) = parseConsecutives(['<','<='],S)
        if flag: return (tree,True)   
        (tree,flag) = parseConsecutives(['>','>='],S)
        if flag: return (tree,True)  
    return (None,False)      

# operators = ['<','<=']
# rule: consecutives -> consecutive | term op consecutive   op is one of the memeber in operators
def parseConsecutives(operators,S):
    #operators = ['<','<=']
    connector = 'and'
    if operators[0]=='U':
        connector ='U'
    t1,f1 = parseConsecutive(operators,S)
    if f1:
        return (t1,f1)
    try:
        #i = S.index('<')
        i = firstIndex(operators,S)
        if i==None:
            return (None,False)        
        (t1,f1)=parseTerm(S[0:i])
        (t2,f2)= parseConsecutives(operators,S[i+1:])
        if f1 and f2:
            #return (('<',[t1]+t2[1]),True)
            
            return ( (connector, [ (S[i],[t1,t2[1][0][1][0]]), t2]) , True )
    except ValueError:
        return(None,False)
    return (None,False)  

# rule: consecutive -> term < term < term
def parseConsecutive(operators,S):
    #operators = ['<','=','<=']
    connector = 'and'
    if operators[0]=='U':
        connector ='U'
    if len(S)<5:
        return (None,False)
    try: 
        # get the first '<'
        #i = S.index('<')
        i = firstIndex(operators,S)
        if i==None:
            return (None,False)
        # get the second '<'
        # j = S[i+1:].index('<') +i+1
        j = firstIndex(operators,S[i+1:])
        if j==None:
            return (None,False)
        j= j+i+1
        (t1,f1)=parseTerm(S[0:i])
        (t2,f2)= parseTerm(S[i+1:j])
        (t3,f3) = parseTerm(S[j+1:])
        if f1 and f2 and f3: 
            #return (('<',[t1,t2,t3]),True) 
            return ( (connector, [ (S[i],[t1,t2]), (S[j],[t2,t3]) ]) , True )
    except ValueError:
        return (None,False)  
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
InfixT4 = ['+','-','U','\\']
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

# rule: T2   ->  T1   |  Prefix2  T2 | Bigop [  Stmt  ] T2  |  Bigop [ Stmt ] ^ [ Stmt ] T2
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
    (tree,flag) = parseBigop(S)
    if flag: 
        return (tree,True)      
    return (None,False)    

Bigop = ['Sum','Prod','Union','Nrsec']
# rule: Bigop [  Stmt  ] T2  |  Bigop [ Stmt ] ^ [ Stmt ] T2 | Bigop[var = term] ^ [term] T2
def parseBigop(S):
    (tree,flag) = parseBigop1(S)
    if flag: 
        return (tree,True) 
    (tree,flag) = parseBigop2(S)
    if flag: 
        return (tree,True)  
    (tree,flag) = parseBigop3(S)
    if flag: 
        return (tree,True)     
    return (None,False)  
# rule: Bigop [  Stmt  ] T2
def parseBigop1(S):
    if len(S)<5:
        return(None,False)
    if S[0] in Bigop:
        try:
            # starting from the next char of the first '[', find the first ']' that does not match '['
            i = closeParentesis('[',S[2:])
            if i==None:
                return (None,False)
            i = i+2
            t1,f1 = parseSentence(S[2:i])
            t2,f2 = parseT2(S[i+1:])
            if f1 and f2:
                return ((S[0],[t1,t2]),True)
        except ValueError:
            return (None,False)
    return (None,False)

# rule: Bigop [ Stmt ] ^ [ Stmt ] T2
def parseBigop2(S):
    if len(S)<9:
        return(None,False)
    if S[0] in Bigop:
        try:
            # starting from the next char of the first '[', find the first ']' that does not match '['
            i = closeParentesis('[',S[2:])
            if i==None:
                return (None,False)
            # add 2 to get the correct index
            i=i+2
            j = i+1
            k = closeParentesis('[',S[j+2:])
            if k == None:
                return (None,False)
            k=k+2+j
            t1,f1 = parseSentence(S[2:i])
            t2,f2 = parseSentence(S[j+2:k])
            t3,f3 = parseT2(S[k+1:])
            if f1 and f2 and f3:
                return ((S[0],[t1,t2,t3]),True)
        except ValueError:
            return (None,False)
    return (None,False)

# rule: Bigop[var = term] ^ [term] T2
# Bigop[var = term1]^[term2] term3 should parse with the same AST as Bigop[var in {term1...term2}] term3
def parseBigop3(S):
    if len(S)<11:
        return(None,False)
    if S[0] in Bigop:
        try:
            # find the first '=', except will catch it if not found 
            e = S.index('=')
            f = S.index('^')
            # starting from the next char of the first '[', find the first ']' that does not match '['
            i = closeParentesis('[',S[2:])
            if i==None:
                return (None,False)
            # add 2 to get the correct index
            i=i+2
            
            j = i+1
            k = closeParentesis('[',S[j+2:])
            if k == None:
                return (None,False)
            k=k+2+j
            t1a,f1a = parseVar(S[2:e])
            t1b,f1b = parseTerm(S[e+1:i])
            t2,f2 = parseTerm(S[j+2:k])
            
            t3,f3 = parseT2(S[k+1:])
            if f1a and f1b and f2 and f3 :
                # Bigop[var = term1]^[term2] term3 should parse with the same AST as Bigop[var in {term1...term2}] term3
                ts = ('in',[t1a,('intRange',[t1b,t2]) ])
                return ((S[0],[ts,t3]),True)
        except ValueError:
            return (None,False)
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
    
#rule 0: T0 -> atom | numeral | identifier | (term) | pipe term pipe | floor(term) | ceil(term) | prefun(terms) | 
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
            if flag: return (('Pow',[tree]),True)
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
            if isNumeral(S[0]): 
                # if the numeral starts with 0 and numeral !=0
                if len(S[0])>1 and S[0][0]=='0':
                    return(eval(S[0][1:]),True)
                else:
                    return (eval(S[0]),True) 
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
        # parse atom
        (tree,flag) = parseAtom(S)
        if flag: return (tree,True)
        # parse consecutive unions
        (tree,flag) = parseConsecutives(['U'],S)
        if flag: return (tree,True)
    except IndexError:
        return(None,False) 
    return (None,False)

# rule: T0 -> atom
def parseAtom(S):
    if len(S)==1:
        if len(S[0])>1:
            if S[0][0]=='`' and isIdentifier(S[0][1:]):
                return(S[0],True)
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
    if len(S)==0: return False
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
