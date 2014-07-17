# Tic Tac Toe
 
# This TPGE game plays a two-player game of tic tac toe.
# ‘x’ goes first, and the players take turns after that.
# The game is played on a 600 by 500 pixel window.
# The game board is a 300 by 300 pixel rectangle,
# whose bottom left coner is point (100,100) and upper right corner is point (400,400)
# The game board is divided into 9 boxes evenly and each box is 100 by 100 pixel.
# When the game is not over, the program says whose turn it is, which is centered at
# point (100,450) of height 15.
# When the game is over, the program says who won and
# a 'play again' button is displayed.
# The button is a rectangle whose bottom left corner is point (400,425)
# and upper right corner is point (500,475)
# If the button is clicked, the game restarts.
# This continues until the player(s) close the window.


"""
# DATA MODEL
 
A *cell* is an integer in [1,10).
A *state* is a pair of lists of cells.
A *player* is either 'x' or 'o'
 
The cells are visualized as corresponding to
squares on a 3x3 tic tac toe board as pictured
below:
 
  1  2  3
 
  4  5  6
 
  7  8  9
 
The game state (L1,L2) is visualized as the state in which
L1 lists the cells occupied by 'x' and L2 lists the the
cells occupied by 'o'
 
"""
 
 
#initialState : state
#InitialState() is the initial state of the program.
 
def initialState():  return([],[])
 
 
# successor: state x point  → state
# successor(S,p) is the state resulting from clicking point
# p in state S
 
def successor(S,p):
 
    # If the game is not over and an empty cell is clicked, return the game state
    # place an 'x' or 'o' in that cell, depending on whose turn it is in S.
    # Since we must do this for every cell, it uses a for-loop. You can think
    # of this as a short way of writing a separate if statement for each cell.
   
    for cell in range(1,10):
        if not over(S) and insideCell(p,cell) and empty(cell,S):
            return insert(turn(S),cell,S)
       
    # If the game is over and the playAgain buttton, return initial state.
   
    if over(S) and clickedPlayAgain(p): return initialState()
 
    # otherwise, return input S
    else: return S

# over: State -> bool
# over(S) means that the game is over in state S.

def over(S):
    # The game is over when either of the player won the game or all the cell are occupied
    return winner(S,'x') or winner (S,'o') or len(S[0])+len(S[1])==9

# insideCell : point x cell -> bool
# insideCell(p,C) means that point p is inside cell C on the board.

def insideCell(p,C):
    (x,y)=p

    lowerBound = 100+100*((C-1)%3)
    upperBound = 200+100*((C-1)%3)
    xInCell = lowerBound<x<upperBound

    lowerBound = 300-100*((C-1)//3)
    upperBound = 400-100*((C-1)//3)
    yInCell = lowerBound<y<upperBound
    
    return xInCell and yInCell
 
 
# empty: cell x state -> bool
# empty(C,S) means that cell C is empty in state S.

def empty(C,S):
    return not C in S[0] and not C in S[1]
 
# turn : state -> player
# If S is a state occurring in a game that is not over,
# then turn(S) is 'x' if it is x's turn in state S, and
# 'o' if it is o's turn in S.

def turn(S):
    # If the the number of movs of 'x' is equal to that of 'o', it is x's turn
    if len(S[0])==len(S[1]): return 'x'
    
    #otherwise it is o's turn
    else: return 'o'
 
 
# insert : player x cell x state -> state
# If it is player p's turn and cell c is empty in state S,
# then insert(p,c,S) is the state resulting from player p
# moving in cell c in state S.

def insert(p,c,S):
    # If it is x's turn, append the cell to the first list 
    if p=='x':
        S[0].append(c)
        return (S[0],S[1])

    # otherwise, append the cell to the second list
    else:
        S[1].append(c)
        return (S[0],S[1])
 
   
# displayImages: state  → imageList -- displayImages(S) is a list
# containing the images to be displayed on the screen in program
# state S. Images occurring later in the list overwrite images that
# occur earlier if they overlap.
 
def displayImages(S):
    List = gameBoard() + playerTokens(S)
    # If the game is over, display the game board, play agian button
    # and the text message about who won the game
    if over(S): List = List + playAgainButton() + winnerMessage(S)

    # Otherwise, display the game board
    # and the text message about whose turn it is in the state S
    else: List=List + turnMessage(S)
    
    return List
 
# gameBoard : imageList
# gameBoard() is a list of eight line segments, which are the hash marks
# of the tic tac toe board.

def gameBoard():
    # The game board is a 300 by 300 pixel rectangle,
    # whose bottom left coner is point (100,100) and upper right corner is point (400,400)
    # The game board is divided into 9 boxes evenly and each box is 100 by 100 pixel.
    
    board=[]
    # Line1 to Line4 are horizontal lines starting from the top to the bottom
    for i in range(4):
        x1 = 100
        y1 = 400-100*i
        x2 = 400
        y2 = 400-100*i
        board+=[(x1,y1,x2,y2)]
        
    #Line5 to Line9 are vertical lines starting from left to right
    for j in range(4):
        x1 = 100+100*j
        y1 = 400
        x2 = 100+100*j
        y2 = 100
        board+=[(x1,y1,x2,y2)]
    return board
        
 
# playerTokens: State -> imageList
# playerTokens(S) is a list of images, one for each mark ('x' or 'o') on
# the board in state S.

def playerTokens(S):
    tokens=[]
    for i in S[0]:
        tokens+=playerInCell('x',i)
    for j in S[1]:
        tokens+=playerInCell('o',j)
    return tokens
        
# playerInCell: player x cell -> imageList
# If the cell is occupied by player p,
# then playerInCell(player,cell) is a list, whose only element is a displayText of the player
# displayed at the center of the cell

def playerInCell(p,cell):

    x = 150+100*((cell-1)%3)
    y = 350-100*((cell-1)//3)
    fontSize = 15
    
    return [(p, x, y, fontSize)]

# playAgainButton: imageList
# playAgainButton() is a list of images for a box in the upper right
# corner containing the text "Play Again".

def playAgainButton():
    # The button box is a rectangle whose bottom left corner is point (400,425)
    # and upper right corner is point (500,475)
    buttonBox=[(400,475,500,475)]+[(400,425,500,425)]+[(400,475,400,425)]+[(500,475,500,425)]
    
    # The button box is a image of the text 'Play Again' centered at the point (450,450) of height 15 in pixel
    buttonText=[('Play Again',450,450,15)]
    
    return buttonBox+buttonText

# clickedPlayAgain: point -> bool
# clickedPlayAgain(p) is ture when the point is in the 'Play Again'button box, otherwise false.
def clickedPlayAgain(p):
    (x,y)=p
    # The button box is a rectangle whose bottom left corner is point (400,425)
    # and upper right corner is point (500,475)
    return 400<x<500 and 425<y<475

# turnMessage: state -> imageList
# turnMessage(S) is a list, whose only element is the text message about whose turn it is in game state S.
# The text message is centered at point (100,450) of height 15 in pixel

def turnMessage(S):
    if turn(S)=='x': return [("player x's turn",100,450,15)]
    else: return [("player o's turn",100,450,15)]

# winnerMessage(S) : state -> imageList
# If S is a state in which the game is over, winnerMessage(S) is
# a list whose only element is a text message in the upper left corner
# of the screen, saying who won the game (or that the cat won if it is
# a tie).

def winnerMessage(S):
    if   winner(S,'x'): return [('x won the game',100,450,15)]
    elif winner(S,'o'): return [('o won the game',100,450,15)]
    else:               return [('cat won the game',100,450,15)]

# winner: state x player -> bool
# winner(S,P) returns True if player P has won the game in game state Sand False otherwise.
def winner(S,P):
    return controls_row(S, P) or \
    controls_column(S, P) or \
    controls_diagonal(S, P)

# controls_row: state x player -> bool
# controls_row(S,player) returns True if player P occupies an entire row of the game board in S and False otherwise.
def controls_row(S,player):
    return player=='x' and (1 in S[0] and 2 in S[0] and 3 in S[0] \
                            or 4 in S[0] and 5 in S[0] and 6 in S[0] \
                            or 7 in S[0] and 8 in S[0] and 9 in S[0])\
        or player=='o' and (1 in S[1] and 2 in S[1] and 3 in S[1] \
                            or 4 in S[1] and 5 in S[1] and 6 in S[1] \
                            or 7 in S[1] and 8 in S[1] and 9 in S[1])
                    
# controls_column: state x player -> bool
# controls_column(S,player) returns True if player P occupies an entire column of the game board in S and False otherwise.
def controls_column(S, player):
    return player=='x' and (1 in S[0] and 4 in S[0] and 7 in S[0]\
                            or 2 in S[0] and 5 in S[0] and 8 in S[0] \
                            or 3 in S[0] and 6 in S[0] and 9 in S[0])\
        or player=='o' and (1 in S[1] and 4 in S[1] and 7 in S[1]\
                            or 2 in S[1] and 5 in S[1] and 8 in S[1] \
                            or 3 in S[1] and 6 in S[1] and 9 in S[1])\

# controls_diagonal: state x player -> bool
# controls_diagonal(S,player) returns True if player P occupies an entire diagonal of the game board in S and False otherwise.
def controls_diagonal(S, player):
    return player=='x' and ( 1 in S[0] and 5 in S[0] and 9 in S[0]\
                            or 3 in S[0] and 5 in S[0] and 7 in S[0])\
        or player=='o' and ( 1 in S[1] and 5 in S[1] and 9 in S[1]\
                            or 3 in S[1] and 5 in S[1] and 7 in S[1])\
     
######################################################################
######################################################################
# TPGE GAME ENGINE
#
# Student code is linked with this code to create a game.

# displaySize() is the size of the display window, (width, height)

def displaySize() : return (600,500)
from graphics import *

# If x is an image, imageKind(x) is the type of image x is:
# 'circle', 'text', or 'lineSegment'

def imageKind(x):
    if len(x)==3 : return 'circle'
    elif type(x[0])== str :return 'text'
    else : return 'lineSegment'

    
# If x is an image, convert(x) is the corresponding image in the
# graphics.py library. We turn the screen upside down so that the origin
# is in the lower left corner, so it matches what they learn in algebra
# class.

def convert(x):
    if imageKind(x)=='circle': return convertCircle(x)
    elif imageKind(x)=='lineSegment': return convertLine(x)
    elif imageKind(x)=='text' : return convertText(x)


def convertLine(x):
    (W,H) = displaySize()
    P1 = Point(x[0],H - x[1])
    P2 = Point(x[2],H - x[3])
    return Line(P1,P2)

def convertText(x):
    (W,H) = displaySize()
    center = Point(x[1],H-x[2])
    string = x[0]
    size = x[3]
    T = Text(center,string)
    T.setSize(size)
    return T

def convertCircle(x):
    (W,H) = displaySize()
    center = Point(x[0],H-x[1])
    radius = x[2]
    return Circle(center,radius)

# Create a window to play in
display = GraphWin("Tic Tac Toe", displaySize()[0], displaySize()[1])


# The main loop
#
# Set the state, draw the display, get a mouse click, set the new state,
# and repeat until the user closes the window.

S = initialState()
images = [convert(x) for x in displayImages(S)]

while(True):
    for x in images: x.draw(display)
    c = display.getMouse()
    click = (c.getX(),displaySize()[1] - c.getY())
    S = successor(S,click)
    for I in images: I.undraw()
    images = [convert(x) for x in displayImages(S)]
  
