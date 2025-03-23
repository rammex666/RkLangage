from interpreter.interpreter import Interpreter
from parser.parser import Parser
from lexer.lexer import Lexer

class Main:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.interpreter = None

    def run(self, source_code):
        self.lexer = Lexer(source_code)
        tokens = self.lexer.tokenize()
        
        self.parser = Parser(tokens)
        ast = self.parser.parse()
        
        self.interpreter = Interpreter(ast)
        self.interpreter.interpret()

if __name__ == "__main__":
    with open('rk/main.rk', 'r') as file:
        source_code = file.read()
    main = Main()
    main.run(source_code)