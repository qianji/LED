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
from GlobalVars import Program 
from builtins import isinstance
def isNumber(E): return isinstance(E,numbers.Number)
def isScalar(E): return isNumber(E) or isAtom(E)
def isVector(x): return isinstance(x,tuple) and x[0] == 'vector'
def isSet(x): return isinstance(x,tuple) and x[0] == 'set'
def isTuple(x): return isinstance(x,tuple) and x[0]=='tuple'
def isAtom(x): return False if x==None else isinstance(x,str) and len(x)>1 and x[0]=='`'  
# If E is an expression, val(E) is the value of E.
def val(E):
    if isScalar(E): return E
    if isinstance(E,str) and (E,0) in Program: return valDefined(E,[])
    (Op,X) = E
    if Op in {'and','=>','some','all'}: Args=X  
    else: Args = [val(E) for E in X]
    if Op=='vector': return ('vector',Args)
    if Op=='set'   : return ('set',Args)
    if Op=='tuple' : return ('tuple',Args)
    #if Op=='some'  : return valSome(Args)
    #if Op=='all'   : return valAll(Args)
    if Op in builtIns : return valBuiltIn(Op,Args)
    if (Op,len(Args)) in Program : return valDefined(Op,Args)

# quantifiers
def valSome(Args):
    # The AST of some var  in  t : s  is ('some',[var, A, B]), where A and B are the respective AST's of t and s. 
    # [var, A, B] = X
    var,t,s = Args
    for i in val(t)[1]:
        if val(sub(i,var,s))==True:
            return True
    return False
def valAll(Args):
    # The AST of all var  in  t : s  is ('all',[var, A, B]), where A and B are the respective AST's of t and s. 
    # [var, A, B] = X
    var,t,s = Args
    for i in val(t)[1]:
        if not val(sub(i,var,s))==True:
            return False
    return True

    
def valBuiltIn(Op,Args):
        F = builtIns[Op]
        return F(Args)

def valDefined(Op,Args): 
        F=(Op,len(Args))
        params,funBody = Program[F]
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
    return len(a)==len(b) and all([valEq([a[i],b[i]]) for i in range(len(a))])
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
def valIntRange(X):
    s = []
    l,u = X
    for i in range(l,u+1):
        s.append(i)
    return ('set',s)
        
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

# dynamic overloading resolution
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
    if isAtom(a) and isAtom(b): return a==b
    return False
def valStar(X):
    if isNumber(X[0]) and isNumber(X[1]): return valMult(X)
    if isSet(X[0]) and isSet(X[1]): return valCrossProd(X)

# builtIns is a dictionary of the functions that evaluate each built-in
builtIns = {'+':valPlus, '-':valSubtract, '*':valStar, '/':valDiv, '^':valExp,
            '+1':valUnaryPlus, '-1':valUnaryMinus,
            'floor':valFloor, 'ceil':valCeil, 'pipes':valPipes, 'mod':valMod,
            '=':valEq, '<':valLess, '>':valGreater,'<=':valLesEq,'>=':valGreatEq,
            'and':valAnd,'or' :valOr,'~':valNot,'=>':valImplies,'<=>':valIff,
            'sub':valSub,
            'in':valIn,'subeq':valSubeq,'U':valUnion,'nrsec':valNrsec,'\\':valSetSubtr,
            'Pow':valPow,'choose':valChoose,'intRange':valIntRange,'some':valSome,'all':valAll}

# Added by Qianji
"""
Solution sets

A *binding* is a set of pairs (x,v) where x is a variable and v is a term. If E is an expression and b a binding, we write E.b for the term obtained from E by substituting v for the free occurrences of x in E whenever (x,v) in b. 
For example,  x+y+z+p.{(x,1), (y,3), (z,4)} is the term 1+3+4+p. 
Binding b is a solution of sentence S if S.b is true. 
For example, {(x,1)} is a solution of x^2 = 1 but {(x,5)} is not.

Bindings b1 and b2 are *inconsistent* if there are pairs of the form (x,c1) and (x,c2) such that (x,c1) ∈  b1, (x,c2) ∈  b2, and the statement c1=c2 is false. 
Two bindings that are not inconsistent are said to be consistent.

The solution set of a sentence p, written S(p), is defined as follows, provided it can be computed by finitely applications of the following rules.

1.If p is a false ground sentence, then S(p)is the empty set { }. 
2.If p is a true ground sentence, then S(p) = { { } }. 
3.If p is of the form x = c, where x is a variable and c a ground term, then S(p) = {{(x,c)}}.
4.If p is of the form (x1,...,xn) = (c1,...,cn) where n>1, the xi's are distinct variables and the ci's are ground terms, then S(p) = {{(x1,c1),...,(xn,cn)}}.
5.If p is of the form x in c, where x is a variable and c is a ground term with value {c1,...,cn}, then S(p) = {{(x,c1)},...,{(x,cn}}. 
    Note that, by this definition, if c is the empty set the value of S(p) is { }. 
6.If p is of the form p1 or p2,  then S(p) = S(p1) U S(p2).
7.If p is of the form p1 & p2, then S(p) = { b1 U b2 | b1 ∈ S(p1), b2 ∈ S(p2.b1), b1 consistent with b2 }.

The intuitive interpretation of the binding {(x1,c1),...,(xn,cn)} is x1=c1 &...&xn=cn. 
The intuitive interpretation of the solution set {b1,...,bn} is I(b1) or ... or I(bn), where I(b) is the interpretation of b. 
By this definition, the interpretation of the binding { } is true, the interpretation of the solution set { } is false, and the solution of the solution set { { } } is true.
"""
# AST -> bool
# isGround(E) iff t is a ground term
def isGround(E):
    if not isinstance(E,tuple) :
        if isNumber(E):
            return True
        if E in builtIns:
            return True
        if E in ['set','tuple','vector']:
            return True
        else:
            return False
    (Op,Args) = E
    if isGround(Op):
        return all(isGround(i) for i in Args)
    return False

# AST -> set(bindings)
def solutionSet(E):
    """if E is an AST of a sentence p, then solutionSet(E) is the solution set of p """
    slonSet = []
    solution = []
    if isGround(E):
        if val(E)==False:
            return []
        if val(E) == True:
            return [[]]
    else:
        Op,Args = E
        if Op=='=' and isGround(Args[1]):
            if isinstance(Args[1],tuple) and val(Args[1])[0] =='tuple':
                C = val(Args[1])[1]
                if isinstance(Args[0],tuple) and Args[0][0]=='tuple':
                    X = Args[0][1]
                    if len(X)==len(C):
                        solution = []
                        for i in range(len(X)):
                            solution.append((X[i],C[i]))
                        slonSet.append(solution)
                        return slonSet
            else:
                solution.append((Args[0],Args[1]))
                slonSet.append(solution)
                return slonSet
        if Op =='in' and isGround(Args[1]):
            if isinstance(Args[0],str):
                x = Args[0]
                if isinstance(Args[1],tuple) and val(Args[1])[0] =='set':
                    C = val(Args[1])[1]
                    for i in range(len(C)):
                        solution = []
                        solution.append((x,C[i]))
                        slonSet.append(solution)
                    return slonSet
        if Op =='or':
            p1 = Args[0]
            p2 = Args[1]
            Sp1 = solutionSet(p1)
            Sp2 = solutionSet(p2)
            return unionSlonSets(Sp1, Sp2)
        
        if Op =='and':
            p1 = Args[0]
            p2 = Args[1]
            Sp1 = solutionSet(p1)
            #Sp2 = solutionSet(p2)
            slonSet = []
            for i in range(len(Sp1)):
                b1 = Sp1[i]
                Sp2_b1 = solutionSet(subExpression(p2,b1))
                for j in range(len(Sp2_b1)):
                    b2 = Sp2_b1[j]
                    if areConsistent(b1, b2):
                        union = unionBindings(b1,b2)
                        slonSet.append(union)
            return slonSet
                        
                    
"""
 If E is an expression and b a binding, we write E.b for the term obtained from E by substituting v for the free occurrences of x in E whenever (x,v) in b. 
 For example,  x+y+z+p.{(x,1), (y,3), (z,4)} is the term 1+3+4+p. 
"""            
# AST * list(tuple) -> AST
def subExpression(E,b): 
    params = [ i[0] for i in b]
    vals = [val(i[1]) for i in b]
    sub =subAll(vals,params,E)
    #if val(sub)==True:
    #    return sub
    #return ('=',[1,0])
    return sub
#solution set * solution set -> solution set
def unionSlonSets(Sp1,Sp2):
    slonSet =[]
    slonSet = Sp1.copy()
    for i in range(len(Sp2)):
        if not Sp2[i] in slonSet:
            slonSet.append(Sp2[i])
    return slonSet

# binding * binding -> binding
def unionBindings(b1,b2):
    b=[]
    b = b1.copy()
    for i in range(len(b2)):
        if not b2[i] in b:
            b.append(b2[i])
    return b
#list(tuple) * list(tuple) -> bool
# If b1 and b2 are bindings, areConsistent(b1,b2) iff b1 is consistent with b2
def areConsistent(b1,b2):                
    for i in range(len(b1)):
        for j in range(len(b2)):
            if(b1[0]==b2[0]):
                if not val(b1[1]) == val(b2[1]):
                    return False
    return True

#dot(t,b) is a Python expression whose value represents t.b. 
def dot(t,b):
    e = subExpression(t,b)
    return val(e)

#The value of {t|p} is ('set',[val(dot(t,b)) for b in SolutionSet(p)]).
def valSetComp(t,p):
    return ('set',[val(dot(t,b)) for b in solutionSet(p)])

# The value of Union[p] T is ('set', [x for b in S(p) for x in val(dot(T,b))[1]]
def valBigUnion(t,p):
    return ('set', [x for b in solutionSet(p) for x in val(dot(t,b))[1]])