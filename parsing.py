from sly import Lexer
from sly import Parser
import os

class Lexer_part(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ,PRINT,NEXT,CLS,END,ENDIF,LTEQ}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    # Tokens
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
    PRINT =r'PRINT'
    ARROW = r'->'
    
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    
    a=[]
   
    
    LTEQ= r'<='
    EQEQ = r'=='
    
    @_(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)')
    def NUMBER(self, t):
        
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')

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
    
    @_('PRINT NUMBER')
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


if __name__ == '__main__':
    lexer = Lexer_part()
    parser = BasicParser()
    print("----------------------------------TINY PROGRAMMING LANGUAGE -------------------------------------")
    print("Parsing Phase")
    
    while True:
        try:
            text = input('--> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print("Tree Generated is as follows :")
            print(tree)
            