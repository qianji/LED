######################################################################
# Parser

# Qianji Zheng
# July 2014
######################################################################

from Tokenizer import *
from LEDInterp import *
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

InfpredS0 = ['=','<','>','<=','>=']
def parseS0(S):
    for i in range(len(S)):
        for infpred in InfpredS0:
            if S[i]==infpred:
                (t1,f1)=parseTerm(S[0:i])
                (t2,f2)= parseTerm(S[i+1:])
                if f1 and f2: 
                    return ((infpred,[t1,t2]),True)    
    return (None,False)      

def parseTerm(S):
    return parseT4(S)

InfixT4 = ['+','-']
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

InfixT3 = ['*','/','mod']
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

InfixT1 = ['^']
def parseT1(S):
    for i in range(len(S)):
        for infix in InfixT1:
            if S[i]==infix:
                (t1,f1)=parseT0(S[0:i])
                (t2,f2)= parseT1(S[i+1:])
                if f1 and f2: 
                    return ((infix,[t1,t2]),True) 
    (tree,flag) = parseT0(S)
    if flag: 
        return (tree,True)    
    return (None,False) 
    
'''
# list(string) -> AST * bool
# if S is a list of string then parseT0(S) = (tree,True), where tree is the abstract syntax tree of S, if S complies to rule T0 of the grammar
# otherwise parseE0(S) = (None,False).
#rule 0: T0 -> numeral | identifier | (term) | pipe term pipe | floor(term) | ceil(term) | prefun(terms)
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
            if flag: return (('abs',[tree]),True)        
        # floor ( term )
        if S[0]=='floor' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[2:len(S)-1])
            if flag: return (('floor',[tree]),True)   
        # ceil ( term )
        if S[0]=='ceil' and S[1]=='(' and S[len(S)-1]==')':
            (tree,flag)=parseTerm(S[2:len(S)-1])
            if flag: return (('ceil',[tree]),True)
        # prefun (terms)
        if S[len(S)-1] ==')':
            (tree,flag) = parseUserDefinedFun(S)
            if flag: return (tree,True)
        if len(S)==1: 
            # numeral    
            if isNumeral(S[0]): return (eval(S[0]),True)
            # identifier
            if isIdentifier(S[0]): return (S[0],True)
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
