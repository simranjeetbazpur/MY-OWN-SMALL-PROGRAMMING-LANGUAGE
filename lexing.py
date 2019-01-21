# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 17:06:39 2018

@author: Simranjeet
"""

from sly import Lexer
class Lexer_part(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ,PRINT,NEXT,CLS,END,ENDIF,LTEQ}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    # Define tokens
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




if __name__ == '__main__':
    lexer = Lexer_part()
    env = {}
    print("---------------------------TINY PROGRAMMING LANGUAGE ----------------------------")
    print(" Lexical Phase ")
    while True:
        
        try:
            text = input('--> ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                
                print(token)