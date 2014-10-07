
import unittest
from Tokenizer import tokens
from Parser import *
from Evaluater import *
from Compiler import *
class ParserTest(unittest.TestCase):
    '''
    # This function is used for UnitTest
    # str * str * list<list<num> -> list<>
    # If F is the name of the file of the program, FunN is one of the functions in F and 
    # ParamsL is a list of valid parameters of FunN
    # then self.functionValues(F,FunN,ParamsL) is the value of the FunN(ParamsL) in F
    '''
    def functionValues(self,F,FunN,ParamsL):        
        #compile(F+'.led')
        values = []
        for Params in ParamsL:        
            # construct the params for the expression
            paramsStr = ''
            for i in range(len(Params)):
                if not i == len(Params)-1:
                    paramsStr += str(Params[i])+','
                else:
                    paramsStr += str(Params[i])
            # check for constant definition g = 12
            if paramsStr=='':
                e = FunN
            else:
                e = FunN + '(' + paramsStr + ')'
            expression,eFlag = tokens(e)
            if eFlag:
                tree, tFlag = parseExpression(expression)
                if tFlag:
                    values.append(val(tree.expression()))
        return values      

    '''
    list<str> -> list<int>
    This is a helper function for testing evaluater
    If L is a list of expressions, then self.expressionValues(L) is a list of values corresponds to L
    '''
    def expressionValues(self,L):
        #compile('test.led')
        values = []
        for e in L:
            e=tokens(e)[0]
            #v = val(parseExpression(e)[0])
            tree = parseExpression(e)[0]
            v = val(tree.expression())
            #v=tree.val()
            values.append(v)
        return values
    def setUp(self):
        compile('test.led')
    def test_file(self):
        '''
        # copy and fill in the values for the parameters to test the functions in the program
        
        Fname = ''
        ParamsL = [[]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = []
        self.assertEqual(expected,actural)

        '''
        # test for function f
        F = 'test' # name of the test file
        Fname = 'f' # name of the function
        ParamsL = [ [2,3],[0,0],[0,1],[0,-1],[-1,0]] # f(2,3), f(0,0), f(0,1) ......
        actural = self.functionValues(F,Fname,ParamsL)
        # expected value of function calls
        expected = [6,0,2,-2,-1]    
        self.assertEqual(expected,actural)
        
        # test for g2
        Fname = 'g2' # name of the function
        ParamsL = [ [-1],[0],[1],[2]] # f(2,3), f(0,0), f(0,1) ......
        actural = self.functionValues(F,Fname,ParamsL)
        # expected value of function calls
        expected = [5,4,5,8]    
        self.assertEqual(expected,actural)      
        
        # test for g3
        Fname = 'g3' # name of the function
        ParamsL = [ [-1],[0],[1],[2]] 
        actural = self.functionValues(F,Fname,ParamsL)
        # expected value of function calls
        expected = [5,8,13,20]    
        self.assertEqual(expected,actural)      
        
        # test for 
        Fname = 'divisor'
        ParamsL = [[2,4],[2,0],[3,2]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [True,True,False]
        self.assertEqual(expected,actural)  
        
        # test for 
        Fname = 'even'
        ParamsL = [[2],[3]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [True,False]
        self.assertEqual(expected,actural)  
        
        Fname = 'negative'
        ParamsL = [[-1],[1],[0]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [True,False,False]
        self.assertEqual(expected,actural)
        
        Fname = 'prime'
        ParamsL = [[1],[2],[3],[4],[5]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [False,True,True,False,True]
        self.assertEqual(expected,actural)

        Fname = 'perfect'
        ParamsL = [[1],[28]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [False,True]
        self.assertEqual(expected,actural)

        Fname = 'sumDivisors'
        ParamsL = [[8,0,5]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [7]
        self.assertEqual(expected,actural)  
        
        Fname = 'g'
        ParamsL = [[],[],[]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [12,12,12]
        self.assertEqual(expected,actural) 
        
        Fname = 'Z'
        ParamsL = [[],[],[]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [0,0,0]
        self.assertEqual(expected,actural)      
        
        Fname = 'e'
        ParamsL = [[],[],[]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [2,2,2]
        self.assertEqual(expected,actural)      
        
        Fname = 'positiveTen'
        ParamsL = [[0],[3],[10],[11]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [False,True,True,False]
        self.assertEqual(expected,actural)      
        
        Fname = 'gridDisplay'
        ParamsL = [[]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [('set', [('tuple', [('tuple', [200, 100]), ('tuple', [200, 400])]), ('tuple', [('tuple', [300, 100]), ('tuple', [300, 400])]), ('tuple', [('tuple', [100, 200]), ('tuple', [400, 200])]), ('tuple', [('tuple', [100, 300]), ('tuple', [400, 300])])])]
        self.assertEqual(expected,actural)      


        Fname = 'currentPlayer'
        ParamsL = [[]]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = ['`x']
        self.assertEqual(expected,actural)      
    '''
    This function test the function tokens in Tokenizer.py
    '''
    
    def test_tokens(self):
        L = ['1.2', '1.', '1..3', '1.2..2']
        expected = [ ['1.2'] , ['1.'], ['1','..', '3'], ['1.2', '..', '2'] ]
        for i in range(len(L)):
            actural = tokens(L[i])[0]
            self.assertEqual(expected[i],actural)   
    
#     def test_parseRange(self):
#         S = tokens('{1..23}')[0]
#         actural = (('intRange', [1, 23]), True)
#         expected =parseRange(S)
#         self.assertEqual(expected,actural) 
#         
#         S = tokens('{-1..2}')[0]
#         actural = (('intRange', [('-1', [1]), 2]), True)
#         expected =parseRange(S)
#         self.assertEqual(expected,actural)
     
    def test_evaluater(self):  

        # test for arithmatic operations  
        expressions = ['2','002','0.2','2+2.2']
        actural = self.expressionValues(expressions)
        expected = [2,2,Fraction('0.2'),Fraction('4.2')]
        self.assertEqual(expected,actural)


        # test for operators of tuple  
        expressions = ['(1,2)[1]']
        actural = self.expressionValues(expressions)
        expected = [1]
        self.assertEqual(expected,actural)

        # test for operator of list  
        expressions = ['<1,2>[1]','<2,3>+<4,5>']
        actural = self.expressionValues(expressions)
        expected = [1,('vector',[2,3,4,5])]
        self.assertEqual(expected,actural)
        
        # test for quantifier some and all
        expressions = ['some x in {2,3,4}.x>2 ', 'some x in {0,1,2}.x<0','all x in {2,3,4}.x>2','all x in {2,3,4}.x>1' ,\
                       'some R in {{2,3,4},{0,1},{5,6,7}}. all c in R.c>2','all R in {{2,3,4},{0,1},{5,6,7}}. all c in R. c>2']
        actural = self.expressionValues(expressions)
        expected = [True,False,False,True,True,False]
        self.assertEqual(expected,actural)
      
        # test for consecutive less than
        expressions = ['1<2<3','1<2<=3<4','1<2<=3<4<=5<6','1<=2<1','1<2<=3<4<=5<1']
        actural = self.expressionValues(expressions)
        expected = [True,True,True,False,False]
        self.assertEqual(expected,actural) 
    
        # test for consecutive greater than
        expressions = ['3>2>1','4>3>=3>2','6>=5>4>=3>=2','1>2>=3','1>3>3>=3']
        actural = self.expressionValues(expressions)
        expected = [True,True,True,False,False]
        self.assertEqual(expected,actural) 
        
        # test for set comprehension 
        expressions = ['{x|x in {1..9} & 1<x<3}',  '{x | x in {-2..2} & nonnegative(x)}' , '{x | x in {-2..2} & nonnegative(x) & even(x)}']
        actural = self.expressionValues(expressions)
        expected = [('set',[2]), ('set',[0,1,2]),('set',[0,2])]
        self.assertEqual(expected,actural) 
        
        # test for Sum
        expressions = ['Sum[i in {1..10} & even(i) ] i^2', 'Sum[x=1]^[9]x', 'Sum[x=1]^[9](x+1)']
        actural = self.expressionValues(expressions)
        expected = [220,45,54]
        self.assertEqual(expected,actural) 
        
        # test for Nrsec
        # g2 = x^2+4
        expressions = ['Nrsec[x in {1..3}]{y|y in {1..x} & y<4}', 'Union[k in {1,2,3} & k<=2] {k+1}']
        
        actural = self.expressionValues(expressions)
        expected = [('set',[1]),('set',[2,3])]
        self.assertEqual(expected,actural) 
        
        # test for Union
        expressions = ['Union[x in {1..3}]{y|y in {1..x} & y<4}']
        actural = self.expressionValues(expressions)
        expected = [('set',[1, 1, 2, 1, 2, 3])]
        self.assertEqual(expected,actural) 
        
    def test_solutionSet(self):
        S = 'x in {1,2} U {3,4}'
        expected = [[('x', 1)], [('x', 2)], [('x', 3)], [('x', 4)]]
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 
        
        S = 'x = 5 & y=10 & z = 20'
        expected = [[('x', 5), ('y', 10), ('z', 20)]]
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 

        S = 'x in {2,3} & y in {10,20} & x*y < 40'
        expected = [[('x', 2), ('y', 10)], [('x', 3), ('y', 10)]]
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 

        S = 'x in {1..10} & x < 1'
        expected = []
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 
        
        S = '(x,y,z) = (10,20,30) & x=z'
        expected = []
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 
        
        S = 'x=2 & x in {3,4}'
        expected = []
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 
        
        S = 'x in {1,2} & x in {2,3}'
        expected = [[('x', 2)]]
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 
        
        S = 'x=2 & x=3'
        expected = []
        t = tokens(S)[0]
        ast = parseExpression(t)[0]
        actural = solutionSet(ast.expression())
        self.assertEqual(expected,actural) 
            
if __name__ == '__main__':
    unittest.main()   
