LEDParser
=========

A parser for LED program using Python

The grammar of LED is as defined as follows

T0    → numeral | identifier | (term) | pipe term pipe | floor(term) | ceil(term) | prefun(terms) | vector | set | tuple | Pow (vector) | choose(vector) 

T1   →  T0     |    T0  ^  T1

Prefix2 →   -  |  +  

T2   →  T1   |  Prefix2  T2

Infix3 →    *    |   /     |   mod 

T3   →  T2   |   T3 Infix3 T2  

Infix4 →   +    |   -  

T4   →  T3   |    T4 Infix4 T3 

term  →   T4  

infpred →   =   |   <   |   >   |   <=   |   >=  

S0  →   term   infpred   term 

S2  →  S0   |  ~ S2

S3  →  S2     |   S3  &  S2

S4  → S3     |   S4  or  S3

S5  →   S4    |   S4 =>  S5

S6  →  S5    |   S5 <=>  S6



Function definitions have the following grammar: 

Dfn → identifier ( vars )  =   Expression 

var → identifier

vars →   var | var , vars


The definition f(x1,...,xn):= E is represented by the Python dictionary entry ('f',n) : ([x1,...,xn],E). For example, the following program

 	f(x) := x^2 

  g(x,y) := y+2*x   

would be represented by the following dictionary: 

	{('f',1):(['x'],('^',['x',2])) ,
 ('g',2):(['x','y'],('+',['y',('*',[2,'x'])])) }



	


Parsing calls to user defined functions

User-defined function calls are parsed using the rule

prefun  →  Identifier

T0    →  prefun (  terms  ) 

terms   →   term    |   term  , terms

terms is a nonterminal indicating one or more terms separated by commas. Even though multiple terms separated by commas do not form an expression, we will need to have an AST for them. We will take the AST for the terms  x1,...,xn , where n>1, to be ('cstack',[ t1,...,tn]) where each ti is the AST of xi. 



Generalization of function definitions to include conditionals

Dfn → identifier ( vars )  :=   funcBody 
funcBody  →  Expression  |  conditional

ifClause  → term if statement

ifClauses  → ifClause | ifClause ;  ifClauses

conditional  →  ifClauses | ifClauses ; term otherwise  




Example of function definitions: 

f(x) := x+3

f(x) :=
   x+1 if x<0;
   x-1 otherwise

f(x) := 
  3*x  if x<0;
  x-1  if x>=0 and x<5;
  x    if x>=5

The conditional function definition 

 f(x) := E1 if P1;...;En if Pn 

is stored in the program dictionary as

('f',1): ('cond',[('if',[P1,E1]),...,('if',[Pn,En])])

The conditional function definition 

 f(x) := E1 if P1;...;En if Pn; En+1 otherwise

is stored in the program dictionary as 

	('f',1):('cond')[('if',[P1,E1]),...,('if',[Pn,En]),('ow',[En+1])]



function definitions will be written with the infix ':=', as follows:

	Dfn --> funcDef | relDef
funcDef→ identifier ( vars )  :=   funcBody 
relDef -->  identifier ( vars ) iff   sentence

For example,



  f(x,y) :=
       33      if x < 1; 
       x*y     if x >=1 & y > 0;
       x+2*y   otherwise             

  g(x) := x^2+4

  even(n) iff |n| mod 2 = 0  

  negative(x) iff x < 0




Example program with comments

This is an example program. This text is documentary. The style is literate programming, meaning that comments are default and code is marked, rather than vice versa. A single definition consists of an open brace ({), followed by the keyword 'def', then a definition, and then a closing brace. Multiple definitions are written as an open brace, followed by 'defs', then two or more definitions. Examples are given below.

A single definition looks like this: 

{def  
  f(x,y) :=
         33      if x < 1; 
         x*y     if x >=1 & y > 0;
         x+2*y   otherwise             
}

Multiple definitions look like this:

{defs
  g(x)  := x^2+4
  h(x,y):= x+3*y   
}

and a single definition can appear on one line as well, like this:


{defs negative(x) iff x < 0 }





vectors

A vector is written as zero or more terms, separated by commas and enclosed in angle brackets. The grammar is


  vector  →     <  >  | <  terms >

The AST of the vector <x1,..,xn> is ('vector', [x1,..,xn])


The three operations on vectors are, length, concatenation, and subscripting.  The parser already handles the length operator, which is written like absolute value. For example, | <10,20,30> | = 3. The concatenation is written with +, so, for example <10,20> + <30,40> = <10,20,30,40>. 

Subscripting requires the following grammar rule: 

	T1   →  T0     |    T1  [ term  ]  |    T0  ^  T1



For example, the term <10,20,30>[2] has an AST of( 'sub', [('vector', [10,20,30]), 2]), and a value of 20.



A set is written as zero or more terms, separated by commas and enclosed in braces. The grammar for sets is

T0 --> { } | { terms } 

 The set {x1,...,xn} has AST ('set',[x1,..,xn]).

The following fuctions are defined for any object e and sets A,B:

e in A
A = B
A subeq m
A union B
A nrsec B
A \ B
A * B
|A|
Pow(A)
choose(A)

The only changes needed to the parser for the set operations are to add 'in' and 'subeq' to the InfpredS0's, 'union' and '\' to the InfixT4's, and 'nrsec' to the InfixT3's. The semantics of these operations are given in the LED(no types) document, page 2, except for 'choose'. choose(A) returns an element of set A, nondeterministically. 

With the introduction of sets, you will need to be able to find matching braces to properly detect comments, since a closing brace within a definition may close a set term and not the definition itself. A simple algorithm for doing this can be found here.

A tuple is written as two or more terms,  separated by commas and enclosed in parentheses. The grammar for tuples is

T0 -->  ( terms ) 

The tuple (x1,...,xn) has AST ('tuple',[x1,..,xn]). The following operations are defined for tuples s and t and integer i in {1,...,length(t)}:

t[i] 
s = t

No changes are needed to the parser for these operations, since subscripts are already used for lists and = is already an infpred.

