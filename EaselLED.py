############################################################################
# Easel_LED
# 
# by Nelson Rushton,
# Texas Tech Dept. of Computer Science
# July 16, 2014

import pygame

"""

This engine will operate game programs written in LED. To play a game,

  0. Download and install pygame using the link http://www.pygame.org/download.shtml
  1. Copy the LED game program into a folder, together with this
     engine, and the LED interpreter files.
  2. Run this program from IDLE.
  3. At the IDLE prompt enter the command play(<file>), where <file> is
     a string which is the name of the game program, without the .led file
     extension.

The LED game program must define *initialState*, *images*, *sounds* and
*transition*, as follows:

    a) initialState -- represents the starting state of the program
    b) transition: Input * State -> State -- transition(I,S) is the state resulting from the program accepting input I in state S.
    c) images: State ~> Sprite -- images(S) is a set of the images to be displayed in the program window when the program is in state S.
    d) sounds: Input * State ~> Set(Sound) -- sounds(I,S) is the set of sounds played when input I is accepted in state S.

Function bodies in an LED game program may use the constant symbols
*Gamma* and *click*, denoting the current game state and most recent
mouse click, respectively. The valuses of *initState* and *transition*  may be
any arbitrary LED objects. The value of *images* must be a screen
display, as defined below.
      
      
    *) A point is a pair (x,y) where 0 ≤  x ≤  1000 and 0 ≤ y ≤ 800
    *) A color is a triple (R,G,B) where 0 ≤ R,G,B ≤ 255
    *) An image is  a segment, circle, filled triangle, text image, or disc
        *) A segment is a four-tuple (`seg, p,q,C) where p and q are points, interpreted as the endpoints of the segment, and C is a color. 
        *) A circle is a four-tuple (`circ, p, r, C)  where p is a point, r is a positive integer, and C is a color. We interpret p and r as the center and radius of the circle, respectively.
        *) A filled triangle is a 5-tuple (`fTri, p, q, r, C) where p, q, and r are points and C is a color. The 5-tuple  (`fTri, p, q, r, C), where p, q, and r are noncollinear points and C is a color, represents the filled triangle with vertices p, q, and r, of color C. 
        *) A text image is  a 5-tuple (`txt, S, p, n, C) where S is a string, p a point, n integer in [4,100], and C is a color. The text image  (`txt, S, p, n, C)  represents the text string S, displayed with height n centered at p with  color C.
        *) Disc -- a four-tuple (`disc, p, r, C)   where p is a point, r is a positive integer, and C is a color. We interpret p and r as the center and radius of the circle, respectively.
    *) A sprite is a set of images
    *) A click is either a point or the atom `nil. 
    *) An input  is a pair (c,K) where c is a click and K is a set of single-character strings
    *) A sound  is one of the following five atoms: `ding, `bang, `boing, `clap, `click
    *) The game runs in a 600 by 500 window, with (0,0) as the lower left corner.

"""
from Expression import *
from LEDProgram import *
from Evaluater import *

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
# displaySize() is the size of the display window, (width, height)

def displaySize() : return (1000,800)

def isPoint(I):
    '''image -> bool
    '''
    # extact the tuple from the LED point
    if isinstance(I,tuple):
        tup,point = I
        if isinstance(point,tuple) and len(point)==2:
            # convert Fraction to int if point[0] or point[1] is a Fraction
            x=int(point[0])
            y=int(point[1])
            return tup=='tuple' and x in range(0,1001) and y in range(0,801)
    return False

def isColor(I):
    if isinstance(I,tuple):
        tup,color = I
        if isinstance(color,tuple) and len(color)==3:
            return all(c in range(0,256) for c in color)
    return False

def isSegment(I):
    if isinstance(I,tuple):
        tup,segment = I
        if isinstance(segment,tuple) and len(segment)==4:
            t,p,q,c=segment
            return t=="`seg" and isPoint(p) and isPoint(q) and isColor(c)
    return False

def isTriangle(I):
    if isinstance(I,tuple):
        tup,triangle = I
        if isinstance(triangle,tuple) and len(triangle)==5:
            t,p,q,r,c=triangle
            return t=="`fTri" and isNonCollinear(p,q,r) and isColor(c)
    return False

def isNonCollinear(p,q,r):
    if isPoint(p) and isPoint(q) and isPoint(r):
        return not slope(p,q)==slope(q,r)
    return False

def slope(p,q):
    if isPoint(p) and isPoint(q):
        (tup,[px,py])=p
        (tup,[qx,qy])=q
        if not px-qx==0:
            return (py-qy)/(px-qx)
        else:
            return None

def isCircle(I):
    if isinstance(I,tuple):
        tup,circle = I
        if isinstance(circle,tuple) and len(circle)==4:
            t,p,r,c=circle
            return t=="`circ" and isPoint(p) and isinstance(r,int) and r>0 and isColor(c)
    return False

def isDisc(I):
    if isinstance(I,tuple):
        tup,circle = I
        if isinstance(circle,tuple) and len(circle)==4:
            t,p,r,c=circle
            return t=="`disc" and isPoint(p) and isinstance(r,int) and r>0 and isColor(c)
    return False

def isText(I):
    if isinstance(I,tuple):
        tup,text = I
        if isinstance(text,tuple) and len(text)==5:
            t,s,p,n,c=text
            return t=="`txt" and isinstance(s,tuple) and s[0]=='string' and isPoint(p) and isColor(c) and isinstance(n,int) and n in range(4,101)
    return False

def isClick(C):
    return isPoint(C) or C=="`nil"

def drawSegment(screen,L):
    (tup,[tup,(tup,[x1,y1]),(tup,[x2,y2]),(tup,color)]) = L
    W,H=displaySize()
    p1 = [x1,H-y1]
    p2 = [x2,H-y2]
    pygame.draw.line(screen, tuple(color), p1,p2, 5)

def drawCircle(screen,C):
    (tup,[tup,(tup,[x,y]),radius,(tup,color)]) = C
    x=int(x)
    y=int(y)
    center = [x,H-y]
    pygame.draw.circle(screen, tuple(color), center, radius,1)

def drawDisc(screen,C):
    (tup,[tup,(tup,[x,y]),radius,(tup,color)]) = C
    x=int(x)
    y=int(y)
    W,H=displaySize()
    center = [x,H-y]
    pygame.draw.circle(screen, tuple(color), center, radius,0)

def drawText(screen,Text):
    (tup,[t,string,center,fontSize,(tup,color)]) = Text
    (tup,[x,y]) = center
    # (0,0) is left botton
    W,H=displaySize()    
    y=H-int(y)
    string = prettyString(string)
    T = string[1:-1]
    if pygame.font:
        font = pygame.font.Font(None, fontSize)
        text = font.render(T, 1, color)
        textpos = text.get_rect(centerx=int(x),centery=int(y))
        #screen.blit(text, [x,y])
        screen.blit(text, textpos)

def drawTriangle(screen,Tri):
    (tup,[tup,(tup,p),(tup,q),(tup,r),(tup,color)]) = Tri
    W,H=displaySize()
    #x or y might be Franction(12,1) instead of 12
    p=(int(p[0]),int(H-p[1]))
    q=(int(q[0]),int(H-q[1]))
    r=(int(r[0]),int(H-r[1]))
    pygame.draw.polygon(screen, tuple(color), [p,q,r], 0)

def drawImages(screen,images):

    # Define the colors we will use in RGB format

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.
     
    # Clear the screen and set the screen background
    screen.fill(WHITE)
    #print(images)
    for x in images:
        #draw segment
        #print(x)
        if isSegment(x): drawSegment(screen,x)
        # draw circle
        elif isCircle(x): drawCircle(screen,x)
        elif isDisc(x): drawDisc(screen,x)
        elif isText(x): drawText(screen,x)
        elif isTriangle(x): drawTriangle(screen,x)

    ## Draw a rectangle outline
    #pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)
     
    ## Draw a solid rectangle
    #pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
     
    ## Draw an ellipse outline, using a rectangle as the outside boundaries
    #pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2) 

    ## Draw an solid ellipse, using a rectangle as the outside boundaries
    #pygame.draw.ellipse(screen, RED, [300, 10, 50, 20])   

