'''
Authour: Qianji Zheng, Texas Tech University
July 2014

This file contains all the shared global variables in LED
'''
# The definition f(x1,...,xn):= E is represented by the Python dictionary entry ('f',n) : ([x1,...,xn],E).
# For example, the following program f(x) := x^2  g(x,y) := y+2*x would be represented by the following dictionary: 
# {('f',1):(['x'],('^',['x',2])) , 
# ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) } 
from Utility import *
Program=LEDProgram()