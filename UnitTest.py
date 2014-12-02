
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
            if isinstance(v,Fraction):
                v = numeralValue(v)
            #v=tree.val()
            values.append(v)
        return values

    def expressionPrettyValues(self,L):
        #compile('test.led')
        values = []
        for e in L:
            e=tokens(e)[0]
            #v = val(parseExpression(e)[0])
            tree = parseExpression(e)[0]
            v = val(tree.expression())
            if isinstance(v,Fraction):
                v = numeralValue(v)
            #v=tree.val()
            values.append(prettyString(v))
        return values
#     def setUp(self):
        # compile('test.led')
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

        # performance test for function capture
        Fname = 'capture'
        ParamsL = [['(B,(10,10))','(0,1)','({(W,(10,12)),(W,(10,11)),(B,(10,13))},B,0,0)'],\
                ['(B,(10,10))','(1,0)','({(W,(10,11)),(W,(11,10)),(W,(12,10)),(B,(13,10))},B,0,0)']]
        actural = self.functionValues(F,Fname,ParamsL)
        expected = [True,True]
        self.assertEqual(expected,actural) 


    '''
    This function test the function tokens in Tokenizer.py
    '''
    
    def test_tokens(self):
        L = ['1.2', '1.', '1..3', '1.2..2','.3(145..)','0.(3..)','3.96(721..)','.(4..)',\
                '"hi mom"','"Go tell the Spartans\\rThou who passest by"','"John said \\"hello\\""']
        expected = [ ['1.2'] , ['1.'], ['1','..', '3'], ['1.2', '..', '2'],['.3(145..)'],['0.(3..)'],['3.96(721..)'],['.(4..)'],\
                ['"hi mom"'],['"Go tell the Spartans\\rThou who passest by"'],['"John said \\"hello\\""']]
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
        expected = [2,2,'0.2','4.2']
        self.assertEqual(expected,actural)

        # test for numeral arithmatic operations  
        expressions = ['1/2','1/3','1/7','1/9','1/17','3/7']
        actural = self.expressionValues(expressions)
        expected = ['0.5','0.(3..)','0.(142857..)','0.(1..)','0.(0588235294117647..)','0.(428571..)']
        self.assertEqual(expected,actural)


        # test for operators of tuple  
        expressions = ['(1,2)[1]']
        actural = self.expressionValues(expressions)
        expected = [1]
        self.assertEqual(expected,actural)

        # test for operator of list  
        expressions = ['<1,2>[1]','<2,3>+<4,5>']
        actural = self.expressionValues(expressions)
        expected = [1,('seq',[2,3,4,5])]
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
        
        # test for consecutive equals
        expressions = ['1=1=1','1=3=1','3/2=3/2=3/2']
        actural = self.expressionValues(expressions)
        expected = [True,False,True]
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

        # test for set union and tuple elements
        expressions = ['{1,2,3} U {4}','( {1,2,3} U {4}, {6} )','( ({1,2,3} U {4}), {6} )']
        actural = self.expressionValues(expressions)
        expected = [('set',[1,2,3,4]),('tuple',[('set',[1,2,3,4]),('set',[6])]),('tuple',[('set',[1,2,3,4]),('set',[6])])]
        self.assertEqual(expected,actural) 

        expressions = ['<1,2,3> + <4>','( {<1,2,3> + <4>,2,3} U {4}, {6} )','{(1,2),{1..9},|<1,2>+<3,4>|}',\
                '({1,2}U{3,4}U{5},((1,2),(3,4),<2,4>))','(2,g2(1),g2(1)+g2(2),3,g2(g2(1)))']
        actural = self.expressionPrettyValues(expressions)
        expected = ['<1,2,3,4>','({<1,2,3,4>,2,3,4},{6})','{(1,2),{1,2,3,4,5,6,7,8,9},4}','({1,2,3,4,5},((1,2),(3,4),<2,4>))','(2,5,13,3,29)']
        self.assertEqual(expected,actural) 

        # test for mutiple commas, performance test
        expressions = ['{(0,1), (1,1), (1,0), (1,1), (0,1), (1,1), (1, 0), (1,1)}']
        actural = self.expressionValues(expressions)
        expected = [('set', [('tuple', [0, 1]), ('tuple', [1, 1]), ('tuple', [1, 0]), ('tuple', [1, 1]), ('tuple', [0, 1]), ('tuple', [1, 1]), ('tuple', [1, 0]), ('tuple', [1, 1])])]
        self.assertEqual(expected,actural) 

        expressions = ['((1,(10,10)),(1,0),({(2,(11,10)),(2,(12,10)),(1,(13,10))},1,0,0))']
        actural = self.expressionValues(expressions)
        expected = [('tuple', [('tuple', [1, ('tuple', [10, 10])]), ('tuple', [1, 0]), ('tuple', [('set', [('tuple', [2, ('tuple', [11, 10])]), ('tuple', [2, ('tuple', [12, 10])]), ('tuple', [1, ('tuple', [13, 10])])]), 1, 0, 0])])]
        self.assertEqual(expected,actural) 
 
        ########################################
        # test for type expression
        ########################################
        
        # Nat, Bool,Int,Rat
        expressions = ['1:Nat','-1:Nat','1=1:Bool','2:Bool','-2:Int','2.2:Int','3.3(2..):Rat','{1..9}:Rat']
        actural = self.expressionValues(expressions)
        expected = [True,False,True,False,True,False,True,False]
        self.assertEqual(expected,actural)        
        
        # (T) where T is a type
        expressions = ['1:(Nat)','(1,2):(Int*Int)','(1,2,3):(Int*Int*Rat)','((1,2),3):((Int*Int)*Int)',
                '((1,2),3.3):(Int*Int)*Rat','((1,2),(3,4)): (Int*Int)*(Int*Int)','<1,2>:Seq','{1..9}:fSet']
        actural = self.expressionValues(expressions)
        expected = [True,True,True,True,True,True,True,True]
        self.assertEqual(expected,actural)  

        # Seq(T) and fSet(T), where T is a type
        expressions = ['{1..9}:fSet(Int)', '<1,2,3>:Seq(Int)','<(1,2),(2,3),(4,5)>:Seq(Int*Int*Int)','{((1,2),3.3), ((3,2),3.2),((3,4),1)}:fSet((Int*Int)*Rat)','{{1..9},{2,3}}:fSet(fSet(Int))']
        actural = self.expressionValues(expressions)
        expected = [True,True,True,True,True]
        self.assertEqual(expected,actural)  

        # expression of a set 
        expressions = ['1:{1,2}','(1,2):{(1,2),(3,2),2}','(1,2):{(1,3),(2,2)}']
        actural = self.expressionValues(expressions)
        expected = [True,True,False]
        self.assertEqual(expected,actural)  

        # S U T, where S and T are types 
        expressions = ['(1,2): (Int*Int) U Int','1:{1}U(Int*Int)','1>1:Bool U Int','{1..9}:Int U fSet(Int)','{1..9}:Int U fSet(Int) U (Int*Int)']
        actural = self.expressionValues(expressions)
        expected = [True,True,True,True,True]
        self.assertEqual(expected,actural)  

        # x: T1*...*Tn if x is a tuple (x1,...,xn) and xi:Ti for all i
        expressions = ['{1..9}:(Int*Int)','(1,2):Int*Int','(1,2):(Int*Int)','(1,2.3,3,(2,3),{1..9}):Int*Rat*Nat*(Int*Int)*fSet(Int)','(1,{1..9}):Int*fSet(Int)','(1,2.3,3,(2,3)):Int*Rat*Nat*(Int*Int)','(1,2.3,3):Int*Rat*Nat']
        actural = self.expressionValues(expressions)
        expected = [False,True,True,True,True,True,True]
        self.assertEqual(expected,actural)  

        # lambda
        expressions = ['lam x.x:Lambda','lam x y. x+y:Lambda']
        actural = self.expressionValues(expressions)
        expected = [True,True]
        self.assertEqual(expected,actural)  

        # user defined type symbols(T1-T8) is defined in test.lde
        expressions = ['1:T1','(2,3):T2','4:T3','{1..9}:T4','lam x y.x+y:T4','{(1,2),(3,4),(2,4)}:T5','{{1..9},{2,3}U{1,4}}:T8','((1,1.2),(1,2.3)):T6']
        actural = self.expressionValues(expressions)
        expected = [True,True,False,True,True,True,True,True]
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
    compile('test.led')
    unittest.main()   
