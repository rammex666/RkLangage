class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def interpret(self):
        for node in self.ast:
            self.execute(node)

    def execute(self, node):
        if node['type'] == 'print':
            print(self.evaluate(node['expr']))
        elif node['type'] == 'var_decl':
            self.variables[node['name']] = self.evaluate(node['value'])
        elif node['type'] == 'newline':
            print()  
        else:
            self.evaluate(node)

    def evaluate(self, node):
        if node['type'] == 'number':
            return node['value']
        elif node['type'] == 'string':
            return node['value'].encode().decode('unicode_escape')  # Interpret escape sequences
        elif node['type'] == 'identifier':
            if node['name'] in self.variables:
                return self.variables[node['name']]
            else:
                raise RuntimeError(f'Undefined variable: {node["name"]}')
        elif node['type'] == 'binary_op':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
            if node['op'] == 'PLUS':
                return left + right
            elif node['op'] == 'MINUS':
                return left - right
            elif node['op'] == 'MUL':
                return left * right
            elif node['op'] == 'DIV':
                return left / right
        raise RuntimeError(f'Unexpected node type: {node["type"]}')