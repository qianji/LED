"""
LED evaluator
Dr. Nelson Rushton, Texas Tech University
July, 2014

An *AST* is one of the following

  1. a number
  2. A pair (F,X) where F is an operator and X is a list of expressions.

In this program, the variable E will vary over AST's.
"""


import numbers, math

def isScalar(E): return isinstance(E,numbers.Number) 

builtIns = {'+',   '-',  '*',  '/',  '^',    '+1',   '-1',
            '=',  '<',  '>',  '<=',  '>=', 'and', 'or', '~', '=>', '<=>'}

# If E is an expression, val(E) is the value of E.
def val(E,Program, DefinedFuns):
    if isScalar(E): return E
    (Op,X) = E
    # Our nonstrict ops are 'and' and '=>'
    if Op in {'and','=>'}: Args=X  
    else: Args = [val(E,Program, DefinedFuns) for E in X]
    if Op in builtIns :
        F = builtIns[Op]
        return F(Args)
    if Op in DefinedFuns:
        F=(Op,len(Args))
        params,funBody = Program[F]
        return val( subAll(Args,params,funBody) , Program, DefinedFuns)

def subAll(Vals,Vars,E):
    a = E
    for i in range(len(Vals)):
        a = sub(Vals[i],Vars[i],a)
    return a

def sub(c,x,T):
    if isScalar(T): return T
    elif T==x     :  return c
    elif isinstance(T, str): return T
    (Op,Args) = T
    return ((sub(c,x,Op),[sub(c,x,A) for A in Args]))
    

# Each built-in operator is evaluated by a separate function.
# These functions assume argument X has been evaluated, except
# valNonStrictAnd and valNonStrictImplies.

# Arithmetic operators
def valAdd(X): return X[0]+X[1]
def valSubtract(X): return X[0]-X[1]
def valTimes(X): return X[0]*X[1]
def valDiv(X): return X[0] / X[1]
def valExp(X): return X[0]**X[1]
def valUnaryPlus(X): return X[0]
def valUnaryMinus(X): return -X[0]
def valFloor(X): return int(math.floor(X[0]))
def valCeil(X): return int(math.ceil(X[0]))
def valAbs(X): return abs(X[0])
def valMod(X): return X[0] % X[1]

# Arithmetic comparisons
def valEq(X): return X[0]==X[1]
def valLess(X): return X[0]< X[1]
def valGreater(X): return X[0] > X[1]
def valLesEq(X): return X[0]<=X[1]
def valGreatEq(X): return X[0]>=X[1]

# Boolean connectives
def valAnd(X):
    p = val(X[0])
    if p==False: return False
    return val(X[1])
def valOr(X): return X[0] or X[1]
def valNot(X): return not(X[0])
def valImplies(X):
    p = val(X[0])
    if p==False: return True
    return val(X[1])
def valIff(X): return X[0]==X[1]


# builtIns is a dictionary of the functions that evaluate each built-in

builtIns = {'+':valAdd, '-':valSubtract, '*':valTimes, '/':valDiv, '^':valExp,
            '+1':valUnaryPlus, '-1':valUnaryMinus,
            'floor':valFloor, 'ceil':valCeil, 'abs':valAbs, 'mod':valMod,
            '=':valEq, '<':valLess, '>':valGreater,'<=':valLesEq,'>=':valGreatEq,
            'and':valAnd,'or' :valOr,'~':valNot,'=>':valImplies,'<=>':valIff}


def testEval():
    global Program, DefinedFuns
    # f(x) = x^2
    # g(x,y) = y + 2*x
    Program = {('f',1):(['x'],('^',['x',2])) ,
           ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) }
    DefinedFuns = {'f','g'}
    E = ('f',[5])    # f(5)=25
    F = ('g',[3,5])  # g(3,5) = 11
    G = ('g',[E,F]) # g(E,F) = 61
    if val(G)==61: return 'passed test :)'
    return 'fail!'
