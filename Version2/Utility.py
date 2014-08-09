"Author: Qianji"
'''
This file provides the utilities for the LED 
'''
      
class LEDProgram:
    # A Program is a dictionary, 
    # whose key is a pair (s, n), 
    # where s is a string representing the name of definition d, and n is arity of d, 
    # and whose value is the body of d 
    def __init__(self):
        self.definitions={}
    #if def is a Definition, then add def to P
    def update(self,d):
        self.definitions.update({d.head:d.body})
    # if P contains a definition of a function symbol f with arity n, then body(f,n) is the body of that definition.
    def body(self,f,n):
        head = (f,n)
        return self.definitions[head]
    #true iff P contains a definition of a function symbol f with arity n.
    def defined(self,f,n):
        head = (f,n)
        d = self.definitions.get(head)
        return not d==None
    #a set of all definition names in P
    def definedSymbols(self):
        return [s[0] for s in self.definitions.keys()]
    # if P contains a definition of a function symbol f with arity n, then definition(f,n) is the definition
    def definition(self,f,n):
        head = (f,n)
        return self.definitions.get(head)

class Definition:
    # A Definition is a 4-tuple (s, p, b,g), 
    # where g is an AST representing the guard condition of the definition, 
    # s is a string representing the name of defined function, p is a list of variables representing the parameters of the definition and b is an AST representing the body the definition. 
    # example: if d is the definition of f(x) := x^2, tree is the AST of x^2
    # then symbol = 'f', parms =['x'], head = ('f',1), body = (['x'],tree,True)
    def __init__(self,s,p,b,g=True):
        self.symbol = s 
        self.parms = p 
        self.head = (s,len(p)) 
        self.body = (p,b,g)
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

