############################################################################
# Easel_LED
# 
# by Nelson Rushton,
# Texas Tech Dept. of Computer Science
# July 16, 2014

"""

This engine will operate game programs written in LED. To play a game,

  1. Copy the LED game program into a folder, together with this
     engine, graphics.py, and the LED interpreter files.
  2. Run this program from IDLE.
  3. At the IDLE prompt enter the command play(<file>), where <file> is
     a string which is the name of the game program, without the .led file
     extension.

The LED game program must define *init*, *display*, and
*update*, as follows:

  *) *init* is the initial state of the game.
  *) *display* is the screen display for the current game state
  *) *update* is the game state resulting from the current game
     state and the most recent mouse click.

Function bodies in an LED game program may use to the constant symbols
*Gamma* and *click*, denoting the current game state and most recent
mouse click, respectively. The valuses of *init* and *update*  may be
any arbitrary LED objects. The value of *display* must be a screen
display, as defined below.
      
      
  *) A *point* is an LED pair of integers.
  *) A *segment* is an LED pair of points. The segment (P,Q) represents
     the segment with endpoints P and Q.
  *) A *circle* is an LED pair (C,r) where C is a point and r is an integer.
  *) A *text* is an LED triple (C,h,A) where C is a point, h is an integer,
     and A is a vector of integers. C,h, and A represent the center, height
     and ascii codes of a text string displayed in the game window.
  *) An *image* is a segment, circle, or text.
  *) A *screenDisplay* is either a set of images, or a vector of images.

The game runs in a 600 by 500 window, with (0,0) as the lower left corner.


"""

from Compiler import compile
from Tokenizer import tokens
from Evaluater import val
from Parser import *
from GlobalVars import *
from graphics import *

# displaySize() is the size of the display window, (width, height)

def displaySize() : return (600,500)

# If x is an image, convert(x) is the corresponding graphics
# object from graphics.py

def convert(x):
    if isinstance(x[1][1],tuple): return convertSegment(x)
    if len(x[1])== 2 : return convertCircle(x)
    return convertText(x)
    
def convertSegment(L):
    # only works for lines now
    (tup,[(tup,[x1,y1]),(tup,[x2,y2])]) = L
    (W,H) = displaySize()
    p1 = Point(x1,H - y1)
    p2 = Point(x2,H - y2)
    return Line(p1,p2)


def convertCircle(C):
    (tup,[(tup,[x,y]),radius]) = C
    (W,H) = displaySize()
    center = Point(x,H-y)
    return Circle(center,radius)

def convertText(x):
    (tup,[center,height,string]) = x
    (tup,[x,y]) = center
    (lis, chars) = string
    (W,H) = displaySize()
    T = Text(Point(x,H-y),''.join([chr(x) for x in chars]))
    T.setSize(height)
    return T


# play(F) executes the game defined in LED file F. 

def play(F):
    global images, Gamma, click
    displayWindow = GraphWin("My game", displaySize()[0], displaySize()[1])
#     c = displayWindow.getMouse()
#     click = (c.getX(),displaySize()[1] - c.getY())
    Program.update({('click',0):[[],('tuple',[0,0])]})
    Program.update({('Gamma',0):[[],('set',[])]})
    compile(F+'.led')
    DefinedFuns = definedFuns(Program)
    # initialize the state in LED program memory
    Program.update({('Gamma',0):[[],val('init')]})
    images = [convert(x) for x in val('display')[1]]
    # Create a window to play in
    while(True):
        for x in images: x.draw(displayWindow)
        c = displayWindow.getMouse()
        click = (c.getX(),displaySize()[1] - c.getY())
        Program.update({('click',0):[[],('tuple',[click[0],click[1]])]})
        #print("state before click is ", Program[('newState',0)])
        Program.update({('Gamma',0):[[],val('newState')]})
        #print("state after click is ", Program[('newState',0)])
        for I in images: I.undraw()
        images = [convert(x) for x in val('display')[1]]
  
    

