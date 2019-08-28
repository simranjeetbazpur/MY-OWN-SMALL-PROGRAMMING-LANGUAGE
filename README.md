
# My own programming language
Tiny programming language is a programming language created by us using sly library in Python
3.6. SLY provides two separate classes Lexer and Parser. The Lexer class is used to break input
text into a collection of tokens specified by a collection of regular expression rules. The Parser
class is used to recognize language syntax that has been specified in the form of a context free
grammar. The idea was to make a single line programming language.

<img src="https://cdncontribute.geeksforgeeks.org/wp-content/uploads/compilerDesign.jpg">


## Important Note:
<ul>
  <li>
The variable name can start with a name and an underscore. No special characters are
allowed except underscore. Arithmetic operations can be done on variables. EX: A=10,
    B=20 then A=A+B will result into A=30.</li>
  <li>
    The user can define comments using #. Example, #comments</li>
  <li>
    The keywords used in our language is IF, THEN, ELSE, FOR, FUN, TO, print, NEXT, ENDIF.</li>
<li> Keywords and identifiers are case sensitive in our language. The variable can contain an
  integer. For string and floating-point work is still in progress.</li>
</ul>

## Syntax:
<ul>
  <li>
Print statement is defined as
    print “hello world” will give hello world as output. </li>
  <li>
a=10 will declare a variable a with value a
  </li>
  <li>
print a can be used to output the value of a or writing a will also retrieve the same result.
  </li>
  <li>
IF-ELSE statement:IF condition THEN statement ELSE statement ENDIF
  </li>
<li>FOR loop:
FOR var_assign TO expr NEXT statement
Ex: FOR I=0 TO 5 NEXT print a </li>
<li>FUNCTIONS:
FUN function_name()->FOR i=0 TO 5 NEXT print a</li>
</ul>

## Steps to Execute:
<ol>
  <li>
    Install Python 3.6 and sly library.</li>
  <li>
Using anaconda prompt: Command pip -install sly can be used to install sly library.>/li>
  <li>Run tiny.py to execute the program(executed on Spyder).</li>
<li>For checking lexer and parsing phase result file “lexing.py” and “parsing.py” can be executed.</li>
  </ul>
  </ol>
