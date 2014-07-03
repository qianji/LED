######################################################################
# Tokenizer
######################################################################




# A character is *white* if it is a space, return, tab, or vertical tab.
def white(c): return c in [' ', '\r','\t','\v']


#  If S is a list of characters, remInitialWhite(S) removes initial white space chars
#  characters from S.

def remInitialWhite(S):
    while not S==[] and white(S[0]): S.pop(0)
    return S

# A *special token* is a string that is a member of the following list.

specialTokens = ['+','*','-','/','^','<','=','>','>=','<=',')','(',':-','|','&','~','=>','<=>','.',',']


# An *identifier* is a nonempty string of letters and digits
# beginning with a letter.

# A *numeral* is a nonempty string of digits

# A *token* is a numeral, identifier, or special token.


# munch: list(char) -> str*Bool
#
# If S begins with a token, munch(S) = (tok,True) where tok+S'=S and tok is
# the longest token that begins S. Otherwise, munch(S) = (chars,'False),
# where chars is as far as the algorithm got.

def munch(S):
    chars = []
    state = 'empty'
    while canPush(S,state):
        state = newState(state,S[0])
        chars +=  S.pop(0)
    if validToken(state): return (''.join(chars),True)
    else: return (chars,False)
        
def validToken(state): return state in ['id','num','spec1','lessgreat','equal','colon','digitsAndPoint']

# States are 'empty', 'id', 'num', 'lessgreat', or 'spec1'. Each state
# corresponds to an assertion about the stack. 

# empty: the stack is empty
# id   : the stack contains an identifier
# num  : the stack is a string of digits
# spec1: a special token that cannot be extended
# lessgreat: the stack is ['<'] or ['>'] 



# canPush(S,state) iff, in the current state S with the current stack stk,
# stk+[S[0]] is the beginning of a token.

def canPush(S,state):
    if S==[]: return False
    c=S[0]
    if state == 'empty': 
        if(len(S)>1 and S[0]==':'):
            return canPush(S[1:],'colon')
        else:
            return alphaNum(c) or beginsSpecial(c)
    if state=='id':return alphaNum(c)
    if state == 'num': return digit(c) or c=='.'
    if state == 'lessgreat': return c == '='
    if state =='colon' : return c=='-'
    if state == 'spec1' : return False
    if state == "equal": return c=='>'
    if state == 'digitsAndPoint': return digit(c)

    

# beginSpecial(c) iff c is the beginning of a special token that is not ":-"
def beginsSpecial(c): return any([c==x[0] and not x[0]==':' for x in specialTokens])

# If canpush(S,state) and c=S[0], the newState(state,c) is the
# state resulting from pushing c onto the stack.

def newState(state,c):
    if state == 'empty':
        return 'id' if alpha(c) else \
               'num' if digit(c) else \
               'lessgreat' if c in ['<','>'] else\
               'colon' if c==':' else\
               'equal' if c=='=' else\
               'digitsAndPoint' if c=='.' else\
               'spec1'  
    if state =='id':return 'id'
    if state == 'num': return 'digitsAndPoint' if c=='.' else 'num'
    if state == 'lessgreat': return 'equal' if c=='=' else\
                'spec1'
    if state == 'colon': return 'spec1'
    if state =='equal': return 'spec1'
    if state =='digitsAndPoint': return 'digitsAndPoint'


# alpha(c) means c is a letter. digit(c) means c is a digit. alphaNum(c) means
# it is one of the two.

def alpha(c): return 'A'<=c and c<='Z' or 'a'<=c and c<='z'
def digit(c): return '0'<=c and c<='9'
def alphaNum(c): return alpha(c) or digit(c)



# tokens: str -> list(str)*Bool
# destroys its argument
#
# If S is a valid string of tokens, tokens(S) =  (toks,True) where toks is a list
# of those tokens. Otherwise tokens(S) is (toks,False) where toks is as far as the
# maxmunch algorithm got.

# alters S

def tokens(S):
    S= list(S)
    toks = []
    while True:
        remInitialWhite(S)
        if S == [] :
            return (toks,True)
        else:
            tok,success = munch(S)
            if success: toks += [tok]
            else:       return (toks,False)
print(tokens('let h(x,y) = y+2*x'))
#print(tokens("2^3"))
#print(alpha("^"))
