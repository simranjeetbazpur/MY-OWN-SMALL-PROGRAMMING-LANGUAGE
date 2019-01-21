from sly import Lexer
from sly import Parser
import os

class Lexer_part(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ,PRINT,NEXT,CLS,END,ENDIF,LTEQ}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    #Tokens
    IF = r'IF'
    THEN = r'THEN' 
    ENDIF=r'ENDIF'
    END='END'
    NEXT=r'NEXT'
    CLS=r'cls'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    
    TO = r'TO'
    PRINT =r'print'
    ARROW = r'->'
    
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    
    a=[]
   
    
    LTEQ= r'<='
    EQEQ = r'=='
    
    @_(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)')
    def NUMBER(self, t):
        t.value = int (t.value)
        return t

    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')
    
    
    @_(r'#.*')
    def COMMENT(self, t):
        pass

    

class BasicParser(Parser):
    tokens = Lexer_part.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, p):
        pass
    
    @_('PRINT statement')
    def statement(self, p):
        return (p.statement)
    

    
    @_('FOR var_assign TO expr NEXT statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('IF condition THEN statement ELSE statement ENDIF')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)
    

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)
    
    
    @_('expr LTEQ expr')
    def condition(self, p):
        return ('condition_lteq', p.expr0, p.expr1)
    
    

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)
    
    @_('NAME "=" NUMBER')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.NUMBER)

    @_('expr')
    def statement(self, p):
        return (p.expr)
    
    
    
    @_('PRINT STRING')
    def statement(self, p):
        return ('PRINT',p.STRING)
    
    @_('PRINT NAME')
    def statement(self, p):
        return ('var',p.NAME)
    
    @_('NUMBER')
    def statement(self, p):
        return ('num', p.NUMBER)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

   
    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    
    
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
    
    @_('CLS')
    def statement(self, p):
        return ('clear',os.system('cls'))
    @_('END')
    def statement(self, p):
        return('end',p.END)
    
    



class SyntaxDirected:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]
        if node[0] == 'end':
            print("End of program")
            quit()
            
        if node[0] == 'clear':
            print(" Screen Cleared")
            quit()
            
        if node[0] == 'PRINT':
            a=node[1]
            c=len(a)-1
            z=a[1:c]
            print(z)
             

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        
        if node[0] == 'condition_lteq':
            return self.walkTree(node[1]) <= self.walkTree(node[2])
        
        

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) // self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))


if __name__ == '__main__':
    lexer = Lexer_part()
    parser = BasicParser()
    print("---------------------------TINY PROGRAMMING LANGUAGE ----------------------------")
    env = {}
    while True:
        try:
            text = input('--> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            
            #print(tree)
            
            SyntaxDirected(tree, env)