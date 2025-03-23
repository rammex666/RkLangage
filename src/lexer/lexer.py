import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.token_specification = [
            ('NUMBER',   r'\d+'),            # Integer
            ('PRINT',    r'print'),          # Print keyword
            ('STRING',   r'"[^"]*"'),        # String literal
            ('PLUS',     r'\+'),             # Addition operator
            ('MINUS',    r'-'),              # Subtraction operator
            ('MUL',      r'\*'),             # Multiplication operator
            ('DIV',      r'/'),              # Division operator
            ('LPAREN',   r'\('),             # Left Parenthesis
            ('RPAREN',   r'\)'),             # Right Parenthesis
            ('SEMI',     r';'),              # Semicolon
            ('NEWLINE',  r'\n'),             # Newline
            ('SKIP',     r'[ \t]+'),         # Skip over spaces and tabs
            ('LET',      r'var'),            # Variable declaration
            ('EQUALS',   r'='),              # Assignment operator
            ('ID',       r'[A-Za-z_]\w*'),   # Identifiers
            ('MISMATCH', r'.'),              # Any other character
        ]

    def tokenize(self):
        for mo in re.finditer('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specification), self.source_code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'STRING':
                value = value[1:-1]  # Remove quotes
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected')
            self.tokens.append((kind, value))
        return self.tokens

    def get_tokens(self):
        return self.tokens