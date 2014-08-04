"Author: Qianji"
'''
This file provides the utilities for the LED 
'''

'''
# helper function
# char * int * str -> int
firstIndexBack(C, secondeI, S) searches backward from index of secondI of S to find the first C in S
'''        
def firstIndexBack(C,secondI,S):
    for i in range(secondI,-1, -1):
        if S[i]==C:
            return i
    return None

'''
# helper function
# str * list<str> -> int
# If Cs is a string and S is a list of string, firstIndex(Cs, S) is the first index of one of the member of Cs in S,
# otherwise firstIndex(Cs, S) = None

'''
def firstIndex(Cs, S):
    index = 0
    for i in range(len(S)):
        for C in Cs:
            if(S[i]==C):
                return i
    return None

'''
# helper function for removeComments
This is a function definition: {def f(x) = {x}+{x+2} }
closeParentesis(S) finds the first } that does not match any { in S
'''
def closeParentesis(L,S):
    R = '}'
    if L=='{':
        R = '}'
    if L=='[':
        R = ']'
    if L =='(':
        R = ')'
    if L =='/':
        R == '/'
    S = list(S)
    #create an empty stack S
    index = 0
    stack = []
    while(len(S)>0):
        # read a character ch
        ch = S[0]
        #If ch is an opening paren (of any kind), push it onto stack
        if ch ==L:
            stack.append(ch)
        else:
            # If  ch  is a closing paren }, look at the top of stack.
            if ch==R:
                #If stack is empty at this point, retrun index.
                if len(stack)==0:
                    return index
                top = stack[-1]
                # If the top of stack is the opening paren that corresponds to {, 
                # then pop stack and continue, this paren matches OK.
                if top==L:
                    stack=stack[:-1]
                    S=S[1:]
                    index+=1
                    continue
                else:
                    return index   
        S=S[1:]
        index+=1 
    return None    


