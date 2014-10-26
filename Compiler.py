'''
Qianji Zheng
July 2014
'''

from Expression import *
from LEDProgram import *
from Parser import *
from Tokenizer import *
'''    
string -> 
If F is the name of the file containing the function definitions of LED with .led as its extension, then compile(F) compile the functions in the file 
and update the content of the program in the global variable "Program"
otherwise 
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
def compile(F):
    global Program
    try:
        file = open(F)
        programText = open(F).read()
        file.close()
    except FileNotFoundError as e:
        print(e)
        return
    print('parsing the program ...........')
    # read the file as a string
    t = removeComments(programText)
    #tokenize the file
    text,tokenF = tokens(t)
    #print(text)
    #text,tokenF = tokens(programText)
    if tokenF:
        # get a list of function definitions from text
        funcs= parseProgram(text)
        for i in range(len(funcs)):    
            d,defFlag = parseDfn(funcs[i])
            if defFlag:
                #print('parsing #',i,"function successfully",' '.join(funcs[i]))
                Program.update(d)
            else:
                print("Failed to parse #",i," function: ", ' '.join(funcs[i]))
                return
        print('Parsed program ', F, " successfully")
        # TODO:  Write program to log.txt instead of printing.
        # Separate the functions by line breaks.
    else:
        #print("Failed to tokenize the program")
        print('Failed to tokenize the program. The last 10 valid tokens are',text[-10:])

'''
str -> str
If S is a string, then removeComments(S) is a string that does not have any comments in S
'''
def removeComments(FS):
    S = FS
    allFunctionsText = ''
    while len(S)>0:
        # find the head of the function definition  /--
        funcHead = firstFuncHead(S)
        if funcHead == None:
            S= []
        else:
            head = funcHead[1]
            # find the end of the function definition  --/
            funcEnd = firstFuncEnd(S[head:])
            if funcEnd ==None:
                S=[]
            else:
                end = funcEnd[0] + head
                allFunctionsText += S[head: end] + '  '
                S = S[end+1:]
    return allFunctionsText

'''
This is an function for parsing an alternative way of definition using := in a program. For example, f(x):= x+2 is a definition.
# string -> list< list<string> >
# if S is a string of the program that has f1, f2, ... fn functions, then parseProgram(S)=([L1, L2, ... Ln],True), where L1... Ln 
# are lists of corresponding function to f1, f2,... fn.
'''
def parseProgram(S):
    allFunctions = []
    separators = ['iff',':=']
    lpI = 0
    while len(S)>0:
        # find the first iff or := in S
        firstI = firstIndex(separators,S)
        if firstI ==None:
            allFunctions.append(S)
            S=[]
        else:
            # find the second iff or := in S
            secondI = firstIndex(separators,S[firstI+1:])
            # if there is only one iff or :=
            if secondI==None:
                allFunctions.append(S)
                S=[]
            else:
                # secondeI is the index-1 of the second iff or := in S
                secondI += firstI
                # if there are no '(' or ')'  in the function head
                if not S[secondI] ==')':
                    lpI =secondI+1
                else:
                    # search backward from secondI to find the first '('
                    lpI = firstIndexBack('(',secondI,S)
                # try to find the first 'If' 
                
                ifIndex = firstIndexBack('If',lpI,S)
                # find the end of the first function definition
                if ifIndex == None or ifIndex==0:
                    end = lpI -2 
                else:
                    end = ifIndex-1
                eachFunc = S[:end+1]
                allFunctions.append(eachFunc)
                if end+1==0:
                    S = []
                else:
                    S = S[end+1:]
    return allFunctions

'''
# string -> list< list<string> >
# if S is a string of the program that has f1, f2, ... fn functions, then parseProgram(S)=([L1, L2, ... Ln],True), where L1... Ln 
# are lists of corresponding function to f1, f2,... fn.
'''
def parseProgramLet(S):
    allFunctions = []
    separators = ['let']
    lpI = 0
    while len(S)>0:
        # find the first 'let' in S
        firstI = firstIndex(separators,S)
        if firstI ==None:
            allFunctions.append(S)
            S=[]
        else:
            # find the second 'let' in S
            secondI = firstIndex(separators,S[firstI+1:])
            # if there is only one 'let'
            if secondI==None:
                allFunctions.append(S)
                S=[]
            else:
                # secondeI is the index-1 of the second 'let' in S
                secondI += firstI
                # try to find the first 'If'  
                ifIndex = firstIndexBack('If',secondI,S)
                # find the end of the first function definition
                if ifIndex == None or ifIndex==0:
                    end = secondI
                else:
                    end = ifIndex-1
                eachFunc = S[:end+1]
                allFunctions.append(eachFunc)
                if end+1==0:
                    S = []
                else:
                    S = S[end+1:]
    return allFunctions

'''
string -> dict * bool
If S is a string of the function definitions of funcDef or relDef defined in LED, then parseDfn(S) = (dict,True), where dict is a dictionary 
otherwise parseDfn(S) = (None,False)
For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
{('f',1):(['x'],('^',['x',2])) , 
('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
'''
'''
# rule: Dfn -> funcDef | relDef | ifThenDef | whereDef | guardWhereDef
'''
def parseDfn(S):
    whereIndex = firstIndex(['where'],S)
    thenIndex = firstIndex(['then'],S)
    if not whereIndex==None:
        if not thenIndex==None:
            def5,flag5 = parseGuardWhereDef(S)
            if flag5:
                return(def5,True)
        else:
            def4,flag4 = parseWhereDef(S)
            if flag4:
                return(def4,True)
    else:
        if not thenIndex==None:
            def3,flag3 = parseIfThenDef(S)
            if flag3:
                return (def3,True)
        else:
            def1,flag1 = parseRelDef(S)
            if flag1:
                return (def1,True)
            def2,flag2 = parseFuncDef(S)
            if flag2:
                return (def2,True)
    return (None,False) 

'''
string -> dict * bool
If S is a string of the function definitions of IfThenDef defined in LED, then parseIfThenDef(S) = (dict,True), where dict is a dictionary 
otherwise parseIfThenDef(S) = (None,False)
For example, the following program If x=2 & y=3 then h := x+y  would be represented by the following dictionary: 
{('h',0):([],('+',[2,3]))} 
#rule: Guard -> If sentence then funcDef
'''
def parseIfThenDef(S):
    try:
        i = S.index('If')
        j= S.index('then')
    except ValueError:
        return(None,False)
    t,f1 = parseSentence(S[i+1:j])
    if f1:
        (p,f2)= parseFuncDef(S[j+1:])
        if f2: 
            #put the content in the dictionary
            key,value = p.head,p.body
            d = Definition(key[0], value[0], p.body[1],t)
            return(d,True)    
        else:
            print('cannot parse then statement definition: ',' '.join(S[j+1:])) 
    else:
            print('cannot parse if statement definition: ',' '.join(S[i+1:j])) 
    return (None,False)

'''
string -> dict * bool
If S is a string of the function definitions of IfThenDef defined in LED, then parseIfThenDef(S) = (dict,True), where dict is a dictionary 
otherwise parseIfThenDef(S) = (None,False)
For example, the following program If x=2 & y=3 then h := x+y  would be represented by the following dictionary: 
{('h',0):([],('+',[2,3]))} 
#rule: guard -> If sentence then funcDef
'''
def parseIfThenDefLet(S):
    try:
        i = S.index('If')
        j = S.index('let')
        #j= S.index('then')
    except ValueError:
        return(None,False)
    t,f1 = parseSentence(S[i+1:j])
    if f1:
        (p,f2)= parseFuncDef(S[j:])
        if f2: 
            #put the content in the dictionary
            key,value = p.head,p.body
            d = Definition(key[0], value[0], p.body[1],t)
            return(d,True)    
        else:
            print('cannot parse then statement definition: ',' '.join(S[j+1:])) 
    else:
            print('cannot parse if statement definition: ',' '.join(S[i+1:j])) 
    return (None,False)

def parseWhereDef(S):
    '''
    string -> dict * bool
    If S is a string of the function definitions of whereDef defined in LED, then parseWhereDef(S) = (dict,True), where dict is a dictionary 
    otherwise parseWhereDef(S) = (None,False)
    For example, the following program h := x+y where x=2 & y=3 would be represented by the following dictionary: 
    {('h',0):([],('+',[2,3]))} 
    #rule: whereDef -> funcDef whereClause
    '''
    for i in range(len(S)):
        if S[i]=='where':
            t,f1 = parseWhereClause(S[i:])
            if f1:
                p,f2 = parseFuncDef(S[0:i])
                if f2:
                    key,value = p.head,p.body
                    d=Definition(key[0],value[0],p.body[1],t)
                    return(d,True)
                else:
                    print('cannot parse definition: ',' '.join(S[0:i])) 
            else:
                print('cannot parse where statement definition: ',' '.join(S[i:])) 
    return(None,False)
                
def parseGuardWhereDef(S):
    '''
    string -> dict * bool
    If S is a string of the function definitions of whereDef defined in LED, then parseGuardWhereDef(S) = (dict,True), where dict is a dictionary 
    otherwise parseGuardWhereDef(S) = (None,False)
    For example, the following program If x=2 then h := x+y where y=3 would be represented by the following dictionary: 
    {('h',0):([],('+',[2,3]))} 
    #rule: guardWhereDef -> ifThenDef whereClause
    '''
    for i in range(len(S)):
        if S[i]=='where':
            t,f1 = parseWhereClause(S[i:])
            if f1:
                p,f2 = parseIfThenDef(S[0:i])
                if f2:
                    key,value= p.head,p.body
                    d=Definition(key[0],value[0],p.body[1],AST('and',[t,p.body[2]]))
                    return(d,True)
                else:
                    print('cannot parse definition: ',' '.join(S[0:i])) 
            else:
                print('cannot parse where statement definition: ',' '.join(S[i:])) 
    return(None,False)

                
def parseFuncDef(S):
    '''
    string -> dict * bool
    If S is a string of the function definitions of funcDef defined in LED, then parseFuncDef(S) = (dict,True), where dict is a dictionary 
    otherwise parseFuncDef(S) = (None,False)
    For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
    {('f',1):(['x'],('^',['x',2])) , 
    ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
    #rule: funcDef -> identifier ( vars )  :=   funcBody
    '''
    for i in range(len(S)):
        if S[i]==':=':
            t1,f1 = parseLHS(S[0:i])
            if f1:
                (fName,fParams)=parseLHS(S[0:i])[0]
                paramNumber = len(fParams)
                (t2,f2)= parseFuncBody(S[i+1:])
                if f2: 
                    #put the content in the dictionary
                    d = Definition(fName, fParams, t2, AST(True))
                    return(d,True)    
                else:
                    print('cannot parse function definition right side: ',' '.join(S[i+1:])) 
            else:
                    print('cannot parse function definition left side: ',' '.join(S[0:i])) 
    return (None,False)     

def parseFuncDeflet(S):
    '''
    string -> dict * bool
    If S is a string of the function definitions of funcDef defined in LED, then parseFuncDef(S) = (dict,True), where dict is a dictionary 
    otherwise parseFuncDef(S) = (None,False)
    For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
    {('f',1):(['x'],('^',['x',2])) , 
    ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
    #rule: funcDef -> identifier ( vars )  :=   funcBody
    '''
    for i in range(len(S)):
        if S[i]=='=':
            t1,f1 = parseLHS(S[1:i])
            if f1:
                (fName,fParams)=parseLHS(S[1:i])[0]
                paramNumber = len(fParams)
                (t2,f2)= parseFuncBody(S[i+1:])
                if f2: 
                    #put the content in the dictionary
                    d = Definition(fName, fParams, t2, AST(True))
                    return(d,True)    
                else:
                    print('cannot parse function definition right side: ',' '.join(S[i+1:])) 
            else:
                    print('cannot parse function definition left side: ',' '.join(S[0:i])) 
    return (None,False)  

# relDef -> identifier ( vars ) iff   sentence
# duplicate with parseFuncDef. To be refactored soon
def parseRelDef(S):
    for i in range(len(S)):
        if S[i]=='iff':
            t1,f1 = parseLHS(S[0:i])
            if f1:
                (fName,fParams)=parseLHS(S[0:i])[0]
                paramNumber = len(fParams)
                (t2,f2)= parseSentence(S[i+1:])
                if f2: 
                    #put the content in the dictionary
                    d = Definition(fName, fParams, t2, AST(True))
                    return(d,True)    
                else:
                    print('cannot parse function definition right side: ',' '.join(S[i+1:])) 
            else:
                    print('cannot parse function definition left side: ',' '.join(S[0:i]))    
    return (None,False) 

# relDef -> identifier ( vars ) iff   sentence
# duplicate with parseFuncDef. To be refactored soon
def parseRelDefLet(S):
    for i in range(len(S)):
        if S[i]=='iff':
            t1,f1 = parseLHS(S[1:i])
            if f1:
                (fName,fParams)=parseLHS(S[1:i])[0]
                paramNumber = len(fParams)
                (t2,f2)= parseSentence(S[i+1:])
                if f2: 
                    #put the content in the dictionary
                    d = Definition(fName, fParams, t2, AST(True))
                    return(d,True)    
                else:
                    print('cannot parse function definition right side: ',' '.join(S[i+1:])) 
            else:
                    print('cannot parse function definition left side: ',' '.join(S[0:i]))    
    return (None,False) 

# helper function for removeComments

# A character is *white* if it is a space, return, tab, or vertical tab.
def white(c): return c in [' ', '\r','\t','\v','\n']

# canPushHead(S,state) iff, in the current state S with the current stack stk,
# stk+[S[0]] is the beginning of a token.
def canPushHead(S,state):
    if S==[]: return False
    if state =='success': return False
    if state == 'spec1' : return False
    c=S[0]
    if state == 'empty': 
        return c == '/'
    if state == 'slash': return c=='-'
    if state == 'dash': return True
    if state == 'white': return True
    if state == 'lb': return c=='d' or white(c)
    if state=='d': return 'e'
    if state == 'e': return c=='f'
    if state == 'f': return white(c) or c == 's'
    if state == 's': return white(c)
    if state =='w1' : return c=='d' or white(c)
    if state == 'w2' : return 'w2'
    return False
'''
# helper function for removeComments
# If newStateHead(S,state) and c=S[0], the newState(state,c) is the
# state resulting from pushing c onto the stack.
'''
def newStateHead(state,c):
    if state == 'empty':
        return 'slash' if c=='/' else \
               'spec1'
    if state == 'slash': return 'dash' if c=='-' else 'spec1'
    if state == 'dash': return 'dash' if c=='-' else 'white' if white(c) else 'success'
    if state =='white': return 'white' if white(c) else 'success'  
    if state =='lb':return 'd' if c =='d' else 'lb' if white(c) else 'spec1'
    if state == 'd': return 'e' if c=='e' else 'spec1'
    if state == 'e': return 'f' if c=='f' else 'spec1'
    if state == 'f': return 's' if c=='s' else 'w2' if white(c) else 'spec1'
    if state == 's': return 'w2' if white(c) else 'spec1'
    if state =='w2': return 'w2' if white(c) else 'success'

'''
# helper function for removeComments
# If S is a string, then firstFuncHead(S)=(s,e), where s is the first index of / 
# followed by 1 or more - and e is the first non white space character after that
# For example, if S = '/-- daf--/' then firstFuncHead(S) = (0,4)
'''
def firstFuncHead(S):
    for i in range(len(S)):
        if S[i]=='/':
            state = 'empty'
            temp = list(S[i:])
            end = i
            while canPushHead(temp,state):
                state = newStateHead(state,temp[0])
                temp.pop(0)
                end= end +1
            if state == 'success':
                return (i,end-1)
    return None

'''
# helper function for removeComments
# If S is a string, then firstFuncEnd(S)=(s,e), where s is the first index of - 
# followed by 0 or more - and followed by /, e is the index of / above
# For example, if S = '/-- daf--/' then firstFuncEnd(S) = (7,9)
'''
def firstFuncEnd(S):
    for i in range(len(S)):
        if S[i]=='-':
            state = 'empty'
            temp = list(S[i:])
            end = i
            while canPushEnd(temp,state):
                state = newStateEnd(state,temp[0])
                temp.pop(0)
                end= end +1
            if state == 'success':
                return (i,end-1)
    return None

# helper function for removeComments
# canPushEnd(S,state) iff, in the current state S with the current stack stk,
# stk+[S[0]] is the beginning of a token.
def canPushEnd(S,state):
    if S==[]: return False
    if state == 'spec1' : return False
    c=S[0]
    if state == 'empty': 
        return c == '-'
    if state == 'success': return False
    if state == 'dash': return c=='-' or c=='/'
    return False
'''
# helper function for removeComments
# If canPushEnd(S,state) and c=S[0], the newState(state,c) is the
# state resulting from pushing c onto the stack.
'''
def newStateEnd(state,c):
    if state == 'empty':
        return 'dash' if c=='-' else \
               'spec1'
    if state == 'dash': return 'dash' if c=='-' else 'success' if c=='/' else 'spec1'

#compile('cp.txt')
#run()
#print(parseProgram(tokens('f(x) := x^2 g(x,y) := y+2*x')[0]))
#compile('conditional_program_test.txt')
