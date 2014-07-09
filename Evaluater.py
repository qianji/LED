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
import Compiler
def isNumber(E): return isinstance(E,numbers.Number)
def isScalar(E): return isNumber(E)
def isVector(x): return isinstance(x,tuple) and x[0] == 'vector'
def isSet(x): return isinstance(x,tuple) and x[0] == 'set'
def isTuple(x): return isinstance(x,tuple) and x[0]=='tuple'

# If E is an expression, val(E) is the value of E.
def val(E):
    if isScalar(E): return E
    (Op,X) = E
    # Our nonstrict ops are 'and' and '=>'
    if Op in {'and','=>'}: Args=X  
    else: Args = [val(E) for E in X]
    if Op=='vector': return ('vector',Args)
    if Op=='set'   : return ('set',Args)
    if Op=='tuple' : return ('tuple',Args)
    if Op in builtIns : 
        F = builtIns[Op]
        return F(Args)
    # get the defined functions in the Program
    DefinedFuns = {Def[0] for Def in Compiler.Program}
    if Op in DefinedFuns:
        F=(Op,len(Args))
        params,funBody = Compiler.Program[F]
        groundBody = subAll(Args,params,funBody)
        return DefVal( groundBody)


def DefVal(fbody):
    if not isinstance(fbody,tuple):
        return fbody
    if not fbody[0] == 'cond' :
        return val(fbody)
    # function body is a conditional
    for clause in fbody[1]:
        (op,Args) = clause
        if op == 'if':
            [guard,term] = Args
            guardValue = val(guard)
            if guardValue: return val(term)
        if op == 'ow':
            term = Args[0]
            return val(term)

    
    

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

# Arithmetic ops                   
def valAdd(X): return(X[0]+X[1])
def valSubtract(X): return X[0]-X[1]
def valMult(X): return X[0]*X[1]
def valDiv(X): return X[0] / X[1]
def valExp(X): return X[0]**X[1]
def valUnaryPlus(X): return X[0]
def valUnaryMinus(X): return -X[0]
def valFloor(X): return int(math.floor(X[0]))
def valCeil(X): return int(math.ceil(X[0]))
def valAbs(X):return abs(X[0])
def valMod(X): return X[0] % X[1]
def valLess(X): return X[0]< X[1]
def valGreater(X): return X[0] > X[1]
def valLesEq(X): return X[0]<=X[1]
def valGreatEq(X): return X[0]>=X[1]

# respective equality
def respEqual(X):
    (t1,a),(t2,b) = X
    return len(a)==len(b) and all([valEq(a[i],b[i]) for i in range(len(a))])
# vector functions
def valCat(X): return ('vector', X[0][1]+X[1][1])
def valLen(X): return len(X[0][1])
def valSub(X):
    L = X[0][1]
    index = X[1]
    return L[index-1]

# set operations
def valIn(X): return any({valEq([X[0],Y]) for Y in X[1][1]})
def valSetEq(X): return valSubeq([X[0],X[1]]) and valSubeq([X[1],X[0]])
def valSubeq(X):return  all(  {valIn([e,X[1]]) for e in X[0][1]}  )
def valUnion(X): return ('set', X[0][1] + [e for e in X[1][1] if not valIn([e,X[0]])])
def valNrsec(X): return ('set',[e for e in X[0][1] if valIn([e,X[1]])])
def valSetSubtr(X): return ('set',[e for e in X[0][1] if not valIn([e,X[1]])])
def valCrossProd(X): return ('set',[('tuple',[a,b]) for a in X[0][1] for b in X[1][1]])
def valCardinal(X):
    Arg = X[0]
    elts = Arg[1]
    return len([i for i in range(len(elts)) if not valIn([ elts[i], ('set',elts[i+1:]) ])])
def valPow(X):
    [Arg] = X
    elts = Arg[1]
    if elts ==[] : return ('set',[('set',[])])
    head = elts[0]
    tail = elts[1:]
    S = valPow([('set',tail)])
    a=[]
    for e in S[1]:
        a = a + [('set',[head]+e[1])]
    return ('set',S[1] + a)
        
def valChoose(X): return X[0][1][0]

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

# dynamic overloadeding resolutiom
def valPlus(X):
    if isNumber(X[0]) and isNumber(X[1]): return valAdd(X)
    if isVector(X[0]) and isVector(X[1]): return valCat(X)
def valPipes(X):
    if isNumber(X[0]): return valAbs(X)
    if isVector(X[0]): return valLen(X)
    if isSet(X[0])   : return valCardinal(X)
def valEq(X):
    [a,b] = X
    if isSet(a) and isSet(b) : return valSetEq(X)
    if isVector(a) and isVector(b): return respEqual(X)
    if isTuple(a) and isTuple(b): return respEqual(X)
    if isNumber(a) and isNumber(b): return a==b
    return False
def valTimes(X):
    if isNumber(X[0]) and isNumber(X[1]): return valMult(X)
    if isSet(X[0]) and isSet(X[1]): return valCrossProd(X)

# builtIns is a dictionary of the functions that evaluate each built-in
builtIns = {'+':valPlus, '-':valSubtract, '*':valTimes, '/':valDiv, '^':valExp,
            '+1':valUnaryPlus, '-1':valUnaryMinus,
            'floor':valFloor, 'ceil':valCeil, 'abs':valPipes, 'mod':valMod,
            '=':valEq, '<':valLess, '>':valGreater,'<=':valLesEq,'>=':valGreatEq,
            'and':valAnd,'or' :valOr,'~':valNot,'=>':valImplies,'<=>':valIff,
            'sub':valSub,
            'in':valIn,'subeq':valSubeq,'union':valUnion,'nrsec':valNrsec,'\\':valSetSubtr,
            'Pow':valPow,'choose':valChoose}




def testEval():
    global Program, DefinedFuns
    # f(x) = x^2
    # g(x,y) = y + 2*x
    # h(x) = 3 if x>0; 55 if x<-2; 1 otherwise
    G1 = ('>',['x',0])
    G2 = ('<',['x',-2])
    Program = {('f',1):(['x'],('^',['x',2])) ,
               ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])),
               ('h',1):(['x'],('cond',[('if',[G1,3]),('if',[G2,55]),('ow',[1])]))  }
    DefinedFuns = {'f','g','h'}
    E = ('f',[5])    # f(5)=25
    F = ('g',[3,5])  # g(3,5) = 11
    G = ('g',[E,F]) # g(E,F) = 61
    for j in range(-4,4): print(val(('h',[j]),Program,DefinedFuns))
    if val(G,Program,DefinedFuns)==61: return 'passed test :)'
    return 'fail!'

#print(val(Parser.parseExpression('x >=1 & y > 0')[0]))
