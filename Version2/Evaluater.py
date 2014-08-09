"""
LED evaluator
Dr. Nelson Rushton, Texas Tech University
July, 2014

An *Expression* is one of the following

  1. a number
  2. A pair (F,X) where F is an operator and X is a list of expressions.

In this program, the variable E will vary over Expression's.
"""
import numbers, math
from GlobalVars import Program 
from builtins import isinstance
from _functools import reduce

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
    # if vals is a list of terms and vars is a list of variables, 
    # sub(vals, vars) is the AST of substituting vars[i] with vals vals[i], 0<=i<len(vals)
    def sub(self,vals,vars):
        if isAtom(self.tree):
            return subAll(vals,vars,self.tree)
        else:
            return subAll(vals,vars,self.expression())
    #get the value of T
    def val(self):
        if isAtom(self.tree):
            return val(self.tree)
        else: 
            
            return val(self.expression())
    # convert AST class to a string
    def __str__(self):
        if self.isAtom():
            return str(self.tree)
        else:
            return str ([self.op()]+[str(x) for x in self.args()])     
                  
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

# If E is an expression, val(E) is the value of E.
def val(E):
    #print("Program is ",Program)
    #E=self.tree
    #print(E)
    if isScalar(E): return E
    if isinstance(E,str) and Program.defined(E,0) : return valDefined(E,[])
    (Op,X) = E
    if Op in {'and','=>','some','all','setComp','Union','Sum','Prod','Nrsec'}: Args=X  
    else: 
        #print(E)
        Args = [val(E) for E in X]
    if Op=='vector': return ('vector',Args)
    if Op=='set'   : return ('set',Args)
    if Op=='tuple' : return ('tuple',Args)
    #if Op=='some'  : return valSome(Args)
    #if Op=='all'   : return valAll(Args)
    if Op in builtIns : return valBuiltIn(Op,Args)
    if Program.defined(Op,len(Args)): return valDefined(Op,Args)

def valBuiltIn(Op,Args):
        F = builtIns[Op]
        return F(Args)

def valDefined(Op,Args): 
        F=(Op,len(Args))
        params,funBody,g = Program.body(Op,len(Args))
        groundBody = subAll(Args,params,funBody.expression())
        return DefVal( groundBody)

def DefVal(fbody):
    #print(fbody)
    if not isinstance(fbody,tuple):
        # function body is a user defined constant
        if Program.defined(fbody,0):
            return val(fbody)
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
    if isSymbol(a) and isSymbol(b): return a==b
    return False
def valStar(X):
    if isNumber(X[0]) and isNumber(X[1]): return valMult(X)
    if isSet(X[0]) and isSet(X[1]): return valCrossProd(X)

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

# Big Operations

#The value of {t|p} is ('set',[val(dot(t,b)) for b in SolutionSet(p)]).
def valSetComp(Args):
    t= Args[0]
    p= Args[1]
    return ('set',[val(dot(t,b)) for b in solutionSet(p)])

# The value of Union[p] T is ('set', [x for b in S(p) for x in val(dot(T,b))[1]]
def valBigUnion(Args):
    t= Args[1]
    p= Args[0]
    return ('set', [x for b in solutionSet(p) for x in val(dot(t,b))[1]])
#     slonSet = solutionSet(p)
#     #print(slonSet)
#     d = [[x for x in val(dot(t,b))[1]] for b in solutionSet(p)]
#     #print(Args)
#     #print(d)
#     return ('set',list(set(d[0]).union(*d)))
    
def valBigSum(Args):
    t= Args[1]
    p= Args[0]
    return sum([val(dot(t,b)) for b in solutionSet(p)])

from operator import mul
def valBigProd(Args):
    t= Args[1]
    p= Args[0]
    l = [val(dot(t,b)) for b in solutionSet(p)]
    return reduce(mul, l)

def valBigNrsec(Args):
    t= Args[1]
    p= Args[0]
    slonSet = solutionSet(p)
    d = [[x for x in val(dot(t,b))[1]] for b in solutionSet(p)]
    return ('set',list(set(d[0]).intersection(*d)))
# builtIns is a dictionary of the functions that evaluate each built-in
builtIns = {'+':valPlus, '-':valSubtract, '*':valStar, '/':valDiv, '^':valExp,
            '+1':valUnaryPlus, '-1':valUnaryMinus,
            'floor':valFloor, 'ceil':valCeil, 'pipes':valPipes, 'mod':valMod,
            '=':valEq, '<':valLess, '>':valGreater,'<=':valLesEq,'>=':valGreatEq,
            'and':valAnd,'or' :valOr,'~':valNot,'=>':valImplies,'<=>':valIff,
            'sub':valSub,
            'in':valIn,'subeq':valSubeq,'U':valUnion,'nrsec':valNrsec,'\\':valSetSubtr,
            'Pow':valPow,'choose':valChoose,'intRange':valIntRange,'some':valSome,'all':valAll,'setComp':valSetComp,
            'Union':valBigUnion,'Sum':valBigSum,'Prod':valBigProd,'Nrsec':valBigNrsec}

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
        if isScalar(E):
            return True
        if E in builtIns:
            return True
        if E in ['set','tuple','vector']:
            return True
        if Program.defined(E,0):
            return True
        else:
            return False
    (Op,Args) = E
    # special case for some/all var in term: sentence 
    if Op in ['some','all']:
        return True
    if isGround(Op) or Program.defined(Op,len(Args)):
        return all(isGround(i) for i in Args)
    return False

# AST -> set(bindings)
def solutionSet(E):
    """if E is an AST of a sentence p, then solutionSet(E) is the solution set of p """
    slonSet = []
    solution = []
    if isGround(E):
        #case 1
        #print(E,"is a ground term")
        #print(E)
        if val(E)==False:
            return []
        #case 2
        if val(E) == True:
            return [[]]
    else:
        Op,Args = E
        #case 3
        if Op =='=' and isinstance(Args[0],str) and isGround(Args[1]) :
            solution.append((Args[0],val(Args[1])))
            slonSet.append(solution)
            return slonSet
        # case 4
        if Op=='=' and isinstance(Args[0],tuple) and Args[0][0]=='tuple' and isGround(Args[1]) and val(Args[1])[0]=='tuple':
            C = val(Args[1])[1]
            X = Args[0][1]
            if len(X)==len(C):
                solution = []
                for i in range(len(X)):
                    solution.append((X[i],C[i]))
                slonSet.append(solution)
                return slonSet
        #case 5    
        if Op =='in' and isinstance(Args[0],str) and isGround(Args[1]) and val(Args[1])[0] =='set' :
            x = Args[0]
            C = val(Args[1])[1]
            for i in range(len(C)):
                solution = []
                solution.append((x,C[i]))
                slonSet.append(solution)
            return slonSet
        #case 6
        if Op =='or':
            p1 = Args[0]
            p2 = Args[1]
            Sp1 = solutionSet(p1)
            Sp2 = solutionSet(p2)
            return unionSlonSets(Sp1, Sp2)
        
        # case 7
        if Op =='and':
            p1 = Args[0]
            p2 = Args[1]
#             if p1 ==('all', ['c', 'gameBoard', ('~', [('moveMade', ['c'])])]):
#                 print(p1)
            #print(p1)
            Sp1 = solutionSet(p1)
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
    if b==None: return E
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
