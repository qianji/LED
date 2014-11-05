
"Author: Qianji"
'''
This file provides the the data type for the LED Program 
'''
from Expression import * 
class LEDProgram:
    # A LEDProgram is a dictionary, 
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
    def __init__(self,s,p,b,g=AST(True),sign=None):
        self.symbol = s 
        self.parms = p 
        self.head = (s,len(p))
        #a body of a defintion is not a just expression but a 3 tuples,which includes params, AST of the expression and the gaurd condition
        self.body = (p,b,g,sign)
        self.expression=b
        self.signature = sign

    # convert defintion class to a string    
    def __str__(self):
        return '('+str(self.symbol)+','+str(self.parms)+','+str(self.head)+','+str([str(i) for i in self.body])
# define the global variable of Program 
# The definition f(x1,...,xn):= E is represented by the Python dictionary entry ('f',n) : ([x1,...,xn],E).
# For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
# {('f',1):(['x'],('^',['x',2])) , 
# ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
Program=LEDProgram()
