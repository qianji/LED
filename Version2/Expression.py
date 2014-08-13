'''
A *variable* or an *identifier* is a nonempty string of letters and digits beginning with a letter.
A *number* is a nonempty string of digits
A *qutoed symbol* is an identifier preceded by a backquote, such as `x and `o.
An *Expression* is one of the following

  1. a number
  2. A pair (F,X) where F is an operator and X is a list of expressions.

'''
import numbers, math
class AST:
    # An AST is either a variable, a number, a quoted symbol, 
    # or a non-empty list, whose first element is an operator and whose remaining elements are AST's. 
    def __init__(self,F,args=[]):
        self.tree = None
        # if F is Expression of the form of a pair
        if isinstance(F,tuple):
            self.tree= AST(F[0],F[1]).tree
        if len(args)==0:
            if F in ['set','tuple','vector']:
                self.tree = [F]
            else:
                if isAtom(F):
                    self.tree = F
        else:
            astArgs = [AST(arg) if not isinstance(arg,AST) else arg for arg in args ]
            self.tree = [F]+astArgs
    # T is an atomic expression, i.e.,a variable or scalar
    def isAtom(self):
        return isAtom(self.tree)
    def isSet(self):
        return isSet(self.tree)
    def isTuple(self):
        return isTuple(self.tree)
    def isVector(self):
        return isVector(self.tree)
    #get the oparator of T, if T is not an atomic expression
    def op(self):
        if not isAtom(self.tree):
            return self.tree[0]
        return self.tree
    # get the argument list of T, if T is not an atomic expression
    def args(self):
        if not isAtom(self.tree):
            return self.tree[1:]
        return []
    # convert AST class to a string
    def __str__(self):
        return str(self.expression)
    # convert the class AST to an Expression
    # example, if t is the AST of x^2 then t.expression() = ('^',['x',2])
    def expression(self):
        if self.isAtom():
            return self.tree
        else:
            F,args = self.op(),self.args()
            # convert each of the AST in args to an expression
            eArgs = [x.expression() for x in self.args()]
            if isinstance(F,str): return (F,eArgs)
            else: return (F.expression(),eArgs)
    
def isNumber(E): return isinstance(E,numbers.Number)
def isScalar(E): return isNumber(E) or isSymbol(E) or isBool(E)
def isVector(x): return isinstance(x,tuple) and x[0] == 'vector'
def isSet(x): return isinstance(x,tuple) and x[0] == 'set'
def isTuple(x): return isinstance(x,tuple) and x[0]=='tuple'
def isSymbol(x): return False if x==None else isinstance(x,str) and len(x)>1 and x[0]=='`'  
def isVar(x): return isinstance(x,str) and not isSymbol(x)
def isBool(x): return isinstance(x,bool)
def isAtom(x): return False if x==None else isScalar(x) or isVar(x)


