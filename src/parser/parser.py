class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            self.skip_newlines()
            if self.pos < len(self.tokens):
                statements.append(self.statement())
        return statements

    def statement(self):
        token = self.tokens[self.pos]
        if token[0] == 'LET':
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'EQUALS':
                self.pos += 1
                expr = self.expr()
                self.skip_newlines()
                if self.tokens[self.pos][0] == 'SEMI':
                    self.pos += 1
                    return {'type': 'var_decl', 'name': var_name, 'value': expr}
                else:
                    raise RuntimeError('Missing semicolon')
            else:
                raise RuntimeError('Missing equals sign')
        elif token[0] == 'PRINT':
            self.pos += 1
            expr = self.expr()
            self.skip_newlines()
            if self.tokens[self.pos][0] == 'SEMI':
                self.pos += 1
                return {'type': 'print', 'expr': expr}
            else:
                raise RuntimeError('Missing semicolon')
        elif token[0] == 'NEWLINE':
            self.pos += 1
            return {'type': 'newline'}
        else:
            expr = self.expr()
            self.skip_newlines()
            return expr

    def expr(self):
        self.skip_newlines()
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            token = self.tokens[self.pos]
            self.pos += 1
            node = {'type': 'binary_op', 'op': token[0], 'left': node, 'right': self.term()}
        return node

    def term(self):
        self.skip_newlines()
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('MUL', 'DIV'):
            token = self.tokens[self.pos]
            self.pos += 1
            node = {'type': 'binary_op', 'op': token[0], 'left': node, 'right': self.factor()}
        return node

    def factor(self):
        self.skip_newlines()
        token = self.tokens[self.pos]
        self.pos += 1
        if token[0] == 'NUMBER':
            return {'type': 'number', 'value': token[1]}
        elif token[0] == 'STRING':
            return {'type': 'string', 'value': token[1]}
        elif token[0] == 'ID':
            return {'type': 'identifier', 'name': token[1]}
        elif token[0] == 'LPAREN':
            node = self.expr()
            if self.tokens[self.pos][0] == 'RPAREN':
                self.pos += 1
                return node
            else:
                raise RuntimeError('Missing closing parenthesis')
        raise RuntimeError(f'Unexpected token: {token}')

    def skip_newlines(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'NEWLINE':
            self.pos += 1