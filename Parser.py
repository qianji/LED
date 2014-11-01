# -*- coding: utf-8 -*-
######################################################################
# Parser
# Qianji Zheng, Texas Tech University
# July 2014
######################################################################
from Tokenizer import *
from Expression import *
from fractions import Fraction
''':
This simple parser program parses the following grammar:
######################################################################
Grammar of LED terms

T0    →  variable  |   numeral   |    definedConstant   |   ( term )   |   pipe term pipe   |
 { term .. term }  |  prefun (  terms  )  |   {  }   |  { terms }   |
 { term pipe Stmt }

T1   →  T0     |    T1  [ term  ]

T2   →   T1     |   T1  ^  T2

Bigop  →   Sum  |  Prod  |  Union  |  Nrsec

Prefix →   -  |  +  |   Bigop [  Stmt  ]  |  definedFunctionSymbol | floor | ceil

T3   →  T2   |  Prefix  T3

Infix4 →    *    |   /    |   mod  |   nrsec

T4   →  T3   |   T4  Infix4 T3

Infix5 →   +    |   -   |   U   |   \

T5   →  T4   |    T5 Infix5 T4

term  →   T5   |   lambda  vars . term  |  type var

terms   →   term    |   term  , terms

infpred →   =   |   <   |   >   |   <=   |   >=    |   in   |   subeq

infpredString → term  infpred  term  infpred  term | term  infpred  infpredString

S0  →  definedRelationSym term  |  term   infpred   term | term : type

S1  → S0    |   some  var  in  term . S1    |   all   var  in  term . S1

S2  →  S1   |  ~ S2

S3  →  S2     |   S3  &  S2

S4  → S3     |   S4  or  S3

S5  →   S4    |   S4 =>  S5

S6  →  S5    |   S5 <=>  S6

Stmt  →  S6

vars → var | var vars

guard → If  Stmt  then

constDef → constSym  := body  |  guard constSym  := body

ifBranch → term if Stmt

ifBranches → ifBranch | ifBranch  ifBranches

branches → ifBranches | ifBranches ; term  otherwise

whereClause → where Stmt

funDefBod →  term | branches

funRHS →  funDefBod | funDefBod whereClause

funcDef →  ?guard funcSym params := funDefBod  ?whereClause

relDef → ?guard  relSym params iff Stmt

varList → var | var , varlist

params → ( varList )

varDecl →  var var : type  | vars decls

decls  → varList : type  |  varList : type , decls

type → typeSymbol | type Product |  Set ( type ) | List ( type )
    |type -> type  | type ~> type |

typeProduct → type * type | type * typeProduct

indefiniteTerm → term | < type > | var where Stmt | ( varlist ) where Stmt

typeDef → typeSym ::= typeDefBody

typeDefBody →   indefiniteTerm | indefiniteTerm  pipe  typeDefBody

programElement var → varDecl |  constDef funcDef | relDef | typeDef

program → programElement | programElement program

######################################################################
'''
'''
A *var* or an *identifier* is a nonempty string of letters and digits beginning with a letter.
A *numeral* is a nonempty string of digits
Please refer Evaluater.py for the definition of AST
'''

'''
# All the functions in this file that starts with the word "parse" have the same signature as follows if their function signatures are not provided:
# list(string) -> AST * bool
# If S is a list of string then parse**(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to the corresponding rule of the grammar
# otherwise parse**(S) = (None,False).
# Each rule is given right before the function definition
'''
'''
######################################################################
'''
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
            if(t2.op()=='cond'):
                # add otherwise to the list of AST
                return (AST('cond',t2.args()+[AST('ow',[t1])]),True) 
            else:
                return (AST('cond',[t2,AST('ow',[t1])]),True) 

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
                if(isinstance(t2.tree,list) and t2.op()=='cond'):
                    return (AST('cond',[t1]+t2.args()),True) 
                else:
                    return (AST('cond',[t1,t2]),True)
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
                return (AST('if',[t2,t1]),True) 
    return (None,False)    

def parseWhereClause(S):
    '''rule: whereClause -> where Stmt
    '''
    if len(S)>1 and S[0]=='where':
        (t,f)=parseSentence(S[1:])
        if f:
            return (t,True)
    return(None,False)
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
                return (AST('<=>',[t1,t2]),True) 
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
                return (AST('=>',[t1,t2]),True) 
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
                return (AST('or',[t1,t2]),True) 
    (tree,flag) = parseS3(S)
    if flag: 
        return (tree,True)    
    return (None,False)

# rule: S3  ->  S2     |   S3  &  S2
def parseS3(S):
    for i in range(len(S)):
        # if S[i]=='&' or S[i]==',':
        if S[i]=='&':
            (t1,f1)=parseS3(S[0:i])
            (t2,f2)= parseS2(S[i+1:])
            if f1 and f2: 
                return (AST('and',[t1,t2]),True) 
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
            return (AST('~',[t1]),True) 
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

# rule: some  var  in  term . S2 | all   var  in  term . S2
def parseSomeAll(S):
    separators = ['some','all']
    if len(S)<6:
        return(None,False)
    if S[0] in separators:
        try:
            i = S.index('in')
            j = S.index('.')
            t1,f1 = parseVar(S[1])
            t2,f2 = parseTerm(S[i+1:j])
            t3,f3 = parseS2(S[j+1:])
            if f1 and f2 and f3:
                return (AST(S[0],[t1,t2,t3]),True)
        except ValueError:
            return (None,False)
    return (None,False)
#rule S0  ->   term   infpred   term | identifier | consecutives | expression typeExpression
InfpredS0 = ['=','<','>','<=','>=','in','subeq']
def parseS0(S):
    if len(S)==0: return(None,False)
    # parse identifier
    if len(S)==1:
        if isIdentifier(S[0]):
            return (AST(S[0]),True)
    for i in range(len(S)):
        for infpred in InfpredS0:
            if S[i]==infpred:
                (t1,f1)=parseTerm(S[0:i])
                (t2,f2)= parseTerm(S[i+1:])
                if f1 and f2: 
                    return (AST(infpred,[t1,t2]),True)    
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
        (tree,flag) = parseConsecutives(['='],S)
        if flag: return (tree,True)
    # Expression : typeExpression
    for i in range(len(S)):
         if S[i]==':':
             (t1,f1)=parseExpression(S[0:i])
             (t2,f2)= parseTypeExpression(S[i+1:])
             if f1 and f2: 
                 return (AST(':',[t1,t2]),True) 
    return (None,False)      

def universalParse(S,F):
    '''helper function to remove duplicate functions
    list<list<str>> * list<str> -> tuple
    If S is a list of parsing list of string, and F is a list of parsing functions
    then universalParse(S,F) = (trees,True), where trees is a list of the abstract syntax trees,
    if each memeber of S complies to its corresponding rule in F
    otherwise universalParse(S,F) = (None,False). 
    For example, if S = [['Int'],['Int']], F=['TExp0','TExp0'] then universalParse(S,F)= (trees,True), 
    where trees=[t1,t2] and t1 is AST of parseTExp0(S[0]) and t2 is the AST of parseTExp0(S[1])
    '''
    trees = []
    flags = []
    if len(F)>0 and len(F) ==len(S):
        for i in range(len(F)):
            func = functionNames(F[i])
            t,f = func(S[i])
            trees.append(t)
            flags.append(f)
        if all(flags):
            return (trees,True)
    return (None,False)

# typeProduct -> tExp0 * tExp0 | tExp0 * typeProduct
def parseTypeProduct(S):
    for i in range(len(S)):
        if S[i]=='*':
            (t1,f1)=parseTExp0(S[0:i])
            (t2,f2)= parseTypeProduct(S[i+1:])
            (t3,f3) = parseTExp0(S[i+1:])
            # tExp0 * typeProduct
            if f1 and f2: 
                if(isinstance(t2.tree,list) and t2.op()=='star'):
                    return (AST('star',[t1]+t2.args()),True) 
                else:
                    return (AST('star',[t1,t2]),True)
            # tExp0 * tExp0
            if f1 and f3:
                return (AST('star',[t1,t3]),True)
    return (None,False)

def parseTypeExpression(S):
    '''rule: typeExpression -> tExp0 |typeProduct | typeExpression U tExp0 | typeExpression U typeProduct
    '''
    # tExp0
    t,f = parseTExp0(S)
    if f:
        return (t,f)
    # typeExpression U tExp0 | typeExpression U typeProduct
    for i in range(len(S)):
        if S[i]=='U':
            t2,f2 = parseTypeExpression(S[0:i])
            t1,f1 = parseTExp0(S[i+1:])
            t3,f3 = parseTypeProduct(S[i+1:])
            if f1 and f2: 
                if(isinstance(t2.tree,list) and t2.op()=='typeU'):
                    return (AST('typeU',t2.args()+[t1]),True) 
                else:
                    return (AST('typeU',[t2,t1]),True)
            if f3 and f2: 
                if(isinstance(t2.tree,list) and t2.op()=='typeU'):
                    return (AST('typeU',t2.args()+[t3]),True) 
                else:
                    return (AST('typeU',[t2,t3]),True)
    # typeProduct
    if S.count('U')==0 and S.count('*')>0:
        t,f = parseTypeProduct(S)
        if f:
            return(t,f)

    return(None,False)

# TExp0 -> Bool | Nat | Int | Rat | (typeExpression)|Seq(tExp)|fSet(tExp)|typeSymbol 
def parseTExp0(S):
    # built-in types: Bool, Nat, Int, Rat, fSet, Seq, Lambda
    if len(S)==1 and isIdentifier(S[0]):
        return (AST(S[0]),True)
    # (typeExpression)
    if len(S)>2 and S[0]=='(' and S[-1]==')':
        return parseTypeExpression(S[1:-1])
    # Seq(tExp) or fSet(tExp)
    if len(S)>3 and S[1]=='(' and S[-1]==')':
        t,f = parseTypeExpression(S[2:-1])
        if S[0]=='fSeq' and f:
            return(AST('fSeq',[t]),True)
        if S[0]=='fSet' and f:
            return (AST('fSet',[t]),True)
    # a set 
    if len(S)>2 and S[0]=='{' and S[-1]=='}':
        return parseTerm(S)
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
            #return ( AST(connector, [ (S[i],[t1,t2[1][0][1][0]]), t2]) , True )
            return ( AST(connector, [ AST (S[i],[t1,(t2.args()[0]).args()[0]]) , t2]) , True )
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
            return ( AST(connector, [ AST(S[i],[t1,t2]) , AST( S[j],[t2,t3] ) ]) , True )
    except ValueError:
        return (None,False)  
    return (None,False)  
# rule: term  ->   T4  | lambda  vars . term | typeExpression
def parseTerm(S):
    t,f = parseT4(S)
    if f:
        return parseT4(S)
    t1,f1 = parseLambda(S)
    if f1:
        return parseLambda(S)
#     t,f = parseTypeExpression(S)
    # if f:
        # return(t,f)
    return (None,False)

# rule: term -> lam  vars . term
def parseLambda(S):
    if len(S)<4:
        return (None,False)
    if S[0]=='lam':
        try:
            # find '.' in S
            i = S.index('.')
        except ValueError:
            return (None,False)
        (t1,f1)=parseVars(S[1:i])
        (t2,f2)= parseTerm(S[i+1:])
        if f1 and f2: 
            if isinstance(t1.tree,list) and t1.op()=='cstack':
                return (AST('lambda',[('vars',t1.args()),t2]),True)
            else:
                #return (AST('lambda',[[t1],t2]),True) 
                return (AST('lambda',[('vars',[t1]),t2]),True) 
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
        if(isinstance(t2.tree,list) and t2.op()=='cstack'):
            return (AST('cstack',[t1]+t2.args()),True) 
        else:
            return (AST('cstack',[t1,t2]),True)
    return (None,False)
# rule: var
def parseVar(S):
    if len(S)==1:
        if isIdentifier(S):
            return (AST(S[0]),True)
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
                    return (AST(infix,[t1,t2]),True) 
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
                    return (AST(infix,[t1,t2]),True) 
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
                return (AST(prefix+'1',[t]),True) 
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
                return (AST(S[0],[t1,t2]),True)
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
                return (AST(S[0],[t1,t2,t3]),True)
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
                ts = AST('in',[t1a,AST('intRange',[t1b,t2]) ])
                return (AST(S[0],[ts,t3]),True)
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
                return (AST('sub',[t1,t2]),True)
    # T0 ^ T2
    for i in range(len(S)):
        for infix in InfixT1:
            if S[i]==infix:
                (t1,f1)=parseT0(S[0:i])
                (t2,f2)= parseT2(S[i+1:])
                if f1 and f2: 
                    return (AST(infix,[t1,t2]),True) 
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
            if flag: return (AST('pipes',[tree]),True)        
        # floor ( term )
        if S[0]=='floor' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[2:len(S)-1])
            if flag: return (AST('floor',[tree]),True)   
        # ceil ( term )
        if S[0]=='ceil' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[2:len(S)-1])
            if flag: return (AST('ceil',[tree]),True)
        # Pow(vector)
        if S[0]=='Pow' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseVector(S[2:len(S)-1])
            if flag: return (AST('Pow',[tree]),True)
        # choose(vector)
        if S[0]=='choose' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseVector(S[2:len(S)-1])
            if flag: return (AST('choose',[tree]),True)
        # prefun (terms)
        if S[len(S)-1] ==')':
            (tree,flag) = parseUserDefinedFun(S)
            if flag: return (tree,True)
        if len(S)==1: 
            # numeral    
            if isNumeral(S[0]):
                if isIntegerNum(S[0]):return (AST(int(Fraction(S[0]))),True)
                if isDecimalNonRepeating(S[0]):return (AST(Fraction(S[0])),True)
                return (AST(numeralRepeatingValue(S[0])),True)
                # if S[0] is a numeral that has a decimal fraction with a repeating block
            # identifier or quoted string
            if isIdentifier(S[0]) or isQuotedString(S[0]): return (AST(S[0]),True)
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
                return(AST(S[0]),True)
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
                if(isinstance(t2.tree,list) and t2.op()=='cstack'):
                    return (AST(t1,t2.args()),True) 
                else:
                    return (AST(t1,[t2]),True)
    except ValueError:
        return(None,False)         
    return (None,False)

# rule: prefun -> identifier
def parsePrefun(S):
    if(len(S)==1):
        if isIdentifier(S[0]):
            return (AST(S[0]),True)
    return (None,False)

# rule: terms -> term | term , terms
def parseTerms(S):
    for i in range(len(S)):
        if S[i]==',':
            (t1,f1)=parseTerm(S[0:i])
            (t2,f2)= parseTerms(S[i+1:])
            if f1 and f2: 
                if(isinstance(t2.tree,list) and t2.op()=='cstack'):
                    return (AST('cstack',[t1]+t2.args()),True) 
                else:
                    return (AST('cstack',[t1,t2]),True)
    (tree,flag) = parseTerm(S)
    if flag: 
        return (tree,True)    
    return (None,False)     

def parseGuard(S):
    '''rule: gurad -> If Stmt then
    '''
    if hasKeywords(S,['If','then']) and S[0]=='If' and S[-1]=='then':
        return parseSentence(S[1:-1])
    return (None,False)
     
def hasKeywords(L,Ws):
    '''list<str> * list<str> -> bool
    hasKeywords(L,Ws) iff all words in Ws is in L
    '''
    return all(word in L for word in Ws)
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

# def isQuotedString(S):
    # '''isQuotedString(S) iff S is a *quoted string*
    # string ->bool
    # A quoted string consists of zero or more string characters enclosed in double quotes (").  For example, the following are quoted strings:

         # "hi mom"   
         # "Go tell the Spartans\rThou who passest by"  
         # "John said \"hello\""
    # '''

def isNumeral(S):
    '''isNumeral(S) iff S is a *numeral*    
    string -> bool
    A *numeral* is either an *integer numeral*, a *decimal fraction*, or an *integer numeral* followed by a decimal fraction. For example, the following are LED numerals: 
    714   01   21.7   .3(145..)   0.(3..)   000  3.96(721..)
    '''
    return isIntegerNum(S) or isDecimalFraction(S) or isIntegerNumDotDecimalFraction(S)

def isIntegerNum(S):
    '''An *integer numeral* is a string of 1 or more  decimal digits (0-9) 
    string -> bool
    '''
    if len(S)<1:
        return False
    return all(x.isdigit() for x in S)

def isDecimalFraction(S):
    '''A *decimal fraction* is either 
        1) a decimal point  followed by one or more digits, or
        2) a decimal point, followed by zero or more digits, followed by a repeating block 
    string ->bool
    '''
    if len(S)<2: return False
    # get the index where repeating block starts
    index =S.find('(')
    if S[0]=='.':
        if index==-1:
            return all(x.isdigit() for x in S[1:])
        else:
            return all(x.isdigit() for x in S[1:index]) and isRepeatingBlock(S[index:])
            
def isRepeatingBlock(S):
    ''' A *repeating block* consists of a left parenthesis, followed by one or more decimal digits, followed by two periods, followed by a right  parenthesis. 
    string -> bool
    '''
    if len(S)<5: return False
    if S[0]=='(' and S[-1]==')' and isIntegerNum(S[1:-3]): return True
    return False

def isIntegerNumDotDecimalFraction(S):
    '''
    isIntegerNumDotDecimalFraction(S) iff S is an *integer numeral* followed by a decimal fraction.
    sting -> bool
    '''
    index = S.find('.')
    if index ==-1: return False
    return isIntegerNum(S[0:index]) and isDecimalFraction(S[index:])

def isDecimalNonRepeating(S):
    '''isDecimalNonRepeating(S) iff S is a numeral with a decimal franction but does not contain a repeating block
    sting->bool
    '''
    return isNumeral(S) and S.find('.')!=-1 and S.find('(')==-1

def repeatingBlockParameters(S):
    ''' If S A decimal fraction consisting of a decimal point, followed by digit string S1
    of length n, followed by a repeating block whose body S2 is of length p, then repeatingBlockParameters(S) is a list [S1,S2,p,n]
    otherwise []
    '''
    indexParen = S.find('(')
    indexPeriod = S[indexParen:].find('.') +indexParen
    if len(S[1:indexParen])==0:
        S1=0
        n=0
    else:
        S1=int(S[1:indexParen])
        n =len(str(S1))
    S2=int(S[indexParen+1:indexPeriod])
    p = len(str(S2))
    return [S1,S2,p,n]

def decimalFractionValue(S):
    '''S is A decimal fraction consisting of a decimal point, followed by digit string S1
    of length n, followed by a repeating block whose body S2 is of length p, then S is the decimal expansion of the following rational number:
    S1/10**n + S2/(10**p-1)*10**n
    '''
    [S1,S2,p,n] = repeatingBlockParameters(S)
    return Fraction(S1,10**n) + Fraction(S2,((10**p-1)*10**n))    

def numeralRepeatingValue(S):
    '''If S is a numeral with a decimal fraction that contains a repeating block, then numeralRepeatingValue(S) is the rational number of S
    '''
    # if isNumeral(S):
        # if not (isIntegerNum(S) or isDecimalNonRepeating(S)):
    if isDecimalFraction(S):
        return decimalFractionValue(S)
    else:
        index = S.find('.')
        return Fraction(int(S[0:index]))+decimalFractionValue(S[index:])
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
            return (AST('seq',[]),True)
    # <term>
    if S[0]=='<' and S[len(S)-1]=='>':
        (tree,flag)=parseTerms(S[1:len(S)-1])
        if flag: 
            if(isinstance(tree.tree,list) and tree.op()=='cstack'):
                return (AST('seq',tree.args()),True)
            else:
                return(AST('seq',[tree]),True)
 
    return (None,False)
    
# rule: set -> {  }  | { terms }
def parseSet(S):
    if len(S)<2:
        return (None,False)
    # {}
    if len(S)==2:
        if (S[0]=='{' and S[1]=='}'):
            return (AST('set',[]),True)
    # {term}
    if S[0]=='{' and S[len(S)-1]=='}':
        (tree,flag)=parseTerms(S[1:len(S)-1])
        if flag: 
            if(isinstance(tree.tree,list) and tree.op()=='cstack'):
                return (AST('set',tree.args()),True)
            else:
                return(AST('set',[tree]),True)
 
    return (None,False)

    
# rule: set -> | ( terms )
def parseTuple(S):
    if len(S)<2:
        return (None,False)
    # {term}
    if S[0]=='(' and S[len(S)-1]==')':
        (tree,flag)=parseTerms(S[1:len(S)-1])
        if flag: 
            if(isinstance(tree.tree,list) and tree.op()=='cstack'):
                return (AST('tuple',tree.args()),True)
            else:
                return(AST('tuple',[tree]),True)
 
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
            return(AST('intRange',[t1,t2]),True)
    return (None,False)

# rule: T0 -> { term pipe Stmt }
def parseTermPipeStmt(S):
    if len(S)<5:
        return (None,False)
    # {term}
    if S[0]=='{' and S[len(S)-1]=='}':
        # find the first index of '|' in S
        try:
            i = S.index('|')
        except ValueError:
            return (None,False)
        (t1,f1)= parseTerm(S[1:i])
        (t2,f2)=parseSentence(S[i+1:-1])
        if f1 and f2: 
            return(AST('setComp',[t1,t2]),True)
    return (None,False)
#print(parseTerms(tokens('2+2,3,x2')[0]))
#print(isIdentifier('2'))
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
# helper function for removeComments
This is a function definition: {def f(x) = {x}+{x+2} }
closeParentesis(S) finds the first } that does not match any { in S
'''
def closeParentesis(L,S):
    R = '}'
    if L=='{':
        R = '}'
    if L=='[':
        R = ']'
    if L =='(':
        R = ')'
    if L =='/':
        R == '/'
    S = list(S)
    #create an empty stack S
    index = 0
    stack = []
    while(len(S)>0):
        # read a character ch
        ch = S[0]
        #If ch is an opening paren (of any kind), push it onto stack
        if ch ==L:
            stack.append(ch)
        else:
            # If  ch  is a closing paren }, look at the top of stack.
            if ch==R:
                #If stack is empty at this point, retrun index.
                if len(stack)==0:
                    return index
                top = stack[-1]
                # If the top of stack is the opening paren that corresponds to {, 
                # then pop stack and continue, this paren matches OK.
                if top==L:
                    stack=stack[:-1]
                    S=S[1:]
                    index+=1
                    continue
                else:
                    return index   
        S=S[1:]
        index+=1 
    return None    

functionNames = {'TExp0':parseTExp0,
        'typeProduct':parseTypeProduct}
