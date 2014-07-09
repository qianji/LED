
import unittest
from IDE import functionValues, expressionValues
class ParserTest(unittest.TestCase):
    
    def test_file(self):
        '''
        # copy and fill in the values for the parameters to test the functions in the program
        
        Fname = ''
        ParamsL = [[]]
        actural = functionValues(F,Fname,ParamsL)
        expected = []
        self.assertEqual(expected,actural)

        '''
        # test for function f
        F = 'test' # name of the test file
        Fname = 'f' # name of the function
        ParamsL = [ [2,3],[0,0],[0,1],[0,-1],[-1,0]] # f(2,3), f(0,0), f(0,1) ......
        actural = functionValues(F,Fname,ParamsL)
        # expected value of function calls
        expected = [6,0,2,-2,-1]    
        self.assertEqual(expected,actural)
        
        # test for g2
        Fname = 'g2' # name of the function
        ParamsL = [ [-1],[0],[1],[2]] # f(2,3), f(0,0), f(0,1) ......
        actural = functionValues(F,Fname,ParamsL)
        # expected value of function calls
        expected = [5,4,5,8]    
        self.assertEqual(expected,actural)
        
        # test for g3
        Fname = 'g3'
        ParamsL = [[]]
        actural = functionValues(F,Fname,ParamsL)
        expected = []
        self.assertEqual(expected,actural)        
        
        # test for 
        Fname = 'divisor'
        ParamsL = [[2,4],[2,0],[3,2]]
        actural = functionValues(F,Fname,ParamsL)
        expected = [True,True,False]
        self.assertEqual(expected,actural)  
        
        # test for 
        Fname = 'even'
        ParamsL = [[2],[3]]
        actural = functionValues(F,Fname,ParamsL)
        expected = [True,False]
        self.assertEqual(expected,actural)  
        
        Fname = 'negative'
        ParamsL = [[-1],[1],[0]]
        actural = functionValues(F,Fname,ParamsL)
        expected = [True,False,False]
        self.assertEqual(expected,actural)
        
        Fname = 'prime'
        ParamsL = [[1],[2],[3],[4],[5]]
        actural = functionValues(F,Fname,ParamsL)
        expected = [False,True,True,False,True]
        self.assertEqual(expected,actural)

        Fname = 'perfect'
        ParamsL = [[1],[28]]
        actural = functionValues(F,Fname,ParamsL)
        expected = [False,True]
        self.assertEqual(expected,actural)

        Fname = 'sumDivisors'
        ParamsL = [[8,0,5]]
        actural = functionValues(F,Fname,ParamsL)
        expected = [7]
        self.assertEqual(expected,actural)   
        
    def test_evaluater(self):  
        # test for operators of tuple  
        expressions = ['(1,2)[1]']
        actural = expressionValues(expressions)
        expected = [1]
        self.assertEqual(expected,actural)

        # test for operator of list  
        expressions = ['<1,2>[1]','<2,3>+<4,5>']
        actural = expressionValues(expressions)
        expected = [1,('vector',[2,3,4,5])]
        self.assertEqual(expected,actural)
        
        # test for operator of set   
        expressions = ['{1,2}[0]','{2,3}+{4,3}+{4}']
        actural = expressionValues(expressions)
        expected = [1,{2,3,4}]
        self.assertEqual(expected,actural)
        
if __name__ == '__main__':
    unittest.main()   