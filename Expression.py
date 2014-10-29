'''
A *variable* or an *identifier* is a nonempty string of letters and digits beginning with a letter.
A *number* is a nonempty string of digits
A *qutoed symbol* is an identifier preceded by a backquote, such as `x and `o.
An *Expression* is one of the following

  1. a number
  2. A pair (F,X) where F is an operator and X is a list of expressions.

'''
import numbers, math
from fractions import Fraction
BuiltInTypes = ['Bool','Nat','Int','Rat']
class AST:
    # An AST or Abstract Expression is either a variable, a number, a quoted symbol, an atom 
    # or a non-empty list, whose first element is an operator and whose remaining elements are AST's.
	
	# F can be either a varible, a number, a quoted symbol, an expression or an operator.
	# args is a list of AST's
    def __init__(self,F,args=[]):
        self.tree = None
        # if F is an Expression of the form of a pair
        if isinstance(F,tuple):
            self.tree= AST(F[0],F[1]).tree
        if len(args)==0:
			# deal with empty set, tuple or vector
            if F in ['set','tuple','seq']:
                self.tree = [F]
            else:
                if isAtom(F) or isQuotedString(F):
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
    def isQuotedString(self):
        return isQuotedString(self.tree)
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
        return str(self.expression())
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
    
def isNumber(E): return isinstance(E,numbers.Number) or isinstance(E,Fraction)
def isScalar(E): return isNumber(E) or isSymbol(E) or isBool(E) or isQuotedString(E)
def isVector(x): return isinstance(x,tuple) and x[0] == 'seq'
def isSet(x): return isinstance(x,tuple) and x[0] == 'set'
def isTuple(x): return isinstance(x,tuple) and x[0]=='tuple'
def isSymbol(x): return False if x==None else isinstance(x,str) and len(x)>1 and x[0]=='`'  
def isVar(x): return isinstance(x,str) and not isSymbol(x)
def isBool(x): return isinstance(x,bool)
def isAtom(x): return False if x==None else isScalar(x) or isVar(x) or isLambda(x)
def isLambda(x): return isinstance(x,tuple) and x[0]=='lambda'
def isBuiltInType(E): return E in BuiltInTypes
def isQuotedString(x): return isinstance(x,str) and len(x)>1 and x[0]=='"' and x[-1]=='"'

def prettyString(E):
    if isNumber(E) or isAtom(E): return(str(E))
    if isSet(E): return('{' + prettyStack(E[1]) + '}')
    if isVector(E): return( '<' + prettyStack(E[1]) + '>')
    if isTuple(E): return( '(' + prettyStack(E[1]) + ')')

    
def prettyStack(elts):
    Str = ''
    if not elts==[]:
        Str += prettyString(elts[0])
        for e in elts[1:]:
            Str += ',' + prettyString(e)
    return Str  

# if Args is a list of Expressions, then prettyArgs(Args) is the string concentated with each arg in Args, sepereated with comma
# For example, if Args = [2,('tuple',[2,3]),3,('seq',[1,2])] then prettyArgs(Args) = '2, (2,3), 3, and [1,2]'
def prettyArgs(elts):
    Str = ''
    if not elts==[]:
        Str += prettyString(elts[0])
        for e in elts[1:]:
            if e == elts[-1]:
                Str += ' and ' + prettyString(e)
            else:
                Str += ',' + prettyString(e)
    return Str  
   
def numeralValue(F):
    '''If F is Fraction instance
    '''
    x = F.numerator    
    y = F.denominator
    if x%y==0:
        return x//y
    whole_part = x//y
    x = x%y
    processed = {}
    result = []
    idx = 0
    x= x*10
    numeral=''
    while not x in processed:
        processed[x] = idx 
        while(x!= 0 and x<y):
            x = x*10
            result.append(0)
            idx+=1
            processed[x] = idx
        result.append(x//y)
        x = (x - (x//y)*y)*10
        idx+=1

    numeral += str(whole_part)
    numeral +='.'

    for c in range(processed[x]):
        numeral +=str(result[c])
    if(len(result) - processed[x]  ==1 and result[processed[x]] == 0):
        return numeral
    numeral+='('

    for c in range(processed[x],len(result)):
        numeral +=str(result[c])
    numeral += "..)"
    return numeral
