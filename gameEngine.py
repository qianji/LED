############################################################################
# MY SILLY GAME
#
# You can move the diagonal line from one box to another by clicking 
# inside the boxes.

from Compiler import compile
from Tokenizer import tokens
from Evaluater import val
from Parser import *
from GlobalVars import *

def load(F):
    compile(F+'.led')
    DefinedFuns = definedFuns(Program)
    


######################################################################
######################################################################
# TPGE GAME ENGINE
#
# Student code is linked with this code to create a game.


######################################################################
# These three functions need to call the LED interpreter after
# loading a LED game program.

def init():return val('init')

def display(): return [toEasel(x) for x in val('display')[1]]

def toEasel(I):
    # A line segment is a 4-tuple (x1,y1,x2,y2) of integers where 0 ≤ x1, x2 ≤ 600 and 0≤ y1, y2≤ 500. 
    # Intuitively, it is the line segment connecting the points (x1,y1) and (x2,y2) in the coordinate system whose origin is the lower left corner of the display screen. 
    # In LED a line segment is represented as a tuple ('set',[x1,y1,x2,y2]),  
    return ( tuple(I[1]) ) #if len(I)==2 and len(I[1])==4 and I[0]=='tuple' else\
           
    

def newState(): return val('newState')


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




# The main loop
#
# Set the state, draw the display, get a mouse click, set the new state,
# and repeat until the user closes the window.

Gamma = None
click = None
images = None

def playGame():
    global images, Gamma, click
    Program.update({('Gamma',0):[[],val('init')]})
    images = [convert(toEasel(x)) for x in val('display')[1]]
    # Create a window to play in
    displayWindow = GraphWin("My game", displaySize()[0], displaySize()[1])
    while(True):
      for x in images: x.draw(displayWindow)
      c = displayWindow.getMouse()
      click = (c.getX(),displaySize()[1] - c.getY())
      Program.update({('click',0):[[],('tuple',[click[0],click[1]])]})
      Program.update({('Gamma',0):[[],val('newState')]})
      for I in images: I.undraw()
      images = [convert(toEasel(x)) for x in val('display')[1]]
  
    

