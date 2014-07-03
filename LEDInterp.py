"""
LED evaluator
Dr. Nelson Rushton, Texas Tech University
July, 2014


An *operator* is one of the following strings:
   '+'   '-'  '*'  '/'  '^'    '+1'   '-1'
   '='  '<'  '>'  '<='  '>='
   'and' 'or' '~' '=>' '<=>'

An *AST* is one of the following

  1. a number
  2. A pair (F,X) where F is an operator and X is a list of expressions.

In this program, the variable E will vary over AST's.
"""


import numbers, math

def isNumber(E): return isinstance(E,numbers.Number)

# If E is an expression, val(E) is the value of E.
def val(E):
    if isNumber(E): return E
    (Op,X) = E
    # Our nonstrict ops are 'and' and '=>'
    if Op in {'and','=>'}: Args=X  
    else: Args = [val(E) for E in X]
    F = builtIns[Op]
    return F(Args)

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
