LED Development
========
#LED 
The Language of Effective Definitions (LED) is a formal language for writing computable functions, designed by [Dr. Nelson Rushton](http://www.depts.ttu.edu/cs/faculty/faculty.php?name=J.%20Nelson%20Rushton) from Texas Tech University. 
LED can be used as a functional programming language, as a tool for teaching mathematics and functional programming, or as a medium for precise human-to-human communication of mathematical definitions. It is used as a teaching tool in Dr. Rushton's [CS 1382 Discrete Math](http://nelsonrushton.net/) class. The design goals of LED are rigor, imitation, and simplicity, defined as follows:
1. *rigor*: The syntax and semantics of the language are explicitly and precisely specified.
2. *imitation*: LED expressions denote traditional mathematical objects (numbers, symbols, sets, tuples, and functions) using notations customary in technical and educational literature, as closely as possible while writing plain text.
3. *simplicity*: Someone familiar with functional programming, or with the conventions of mathematical notation, can learn to read LED programs before breakfast, and learn to write them before lunch.
#Requirement
Python 3.4
#File Dependency
0. Tokenizer, called Tokenizer.py
1. *Expression* data type, called Expression.py
2. *Program* data type (depends on 1), called LEDProgram.py
3. Evaluater (depends on 1,2), called Evaluater.py
4. Parser (depends on 1, does not include program parser), called Parser.py
5. Compiler (that is, the program parser. depends on 1-4). 
6. Game engine (depends on 1 , 2, 3), called EaselLED.py
7. Interface (depends on 1-6), called IDE.py
