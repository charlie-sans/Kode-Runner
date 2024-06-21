# custon testting framework language lexer and parser

# language lexer and parser

"""
demo goes as follows to connect to a server and run tests

when the server is running, the client can connect to the server and run tests


::: langtest.tst :::
$NAME: test1
$DESC: test1 description
#DEFINE CONNECT(WEBSOCKET_URL, PORT)
#DEFINE SEND(WBSOCKET_MESSAGE)
#DEFINE contents
$CODE{
    CONNECT("localhost", 8080)
    IF [CONNECTED()]
    {
        SEND("{message: 'hello'}")
        RECEIVE() > contents
        
        IF [contents == "hello"]
        {
            PRINT("Test Passed")
        }
        ELSE
        {
            PRINT("Test Failed")
        } 
        
    }
    ELSE
    {
        PRINT("Failed to connect")
    }
}
"""

import re
import sys
import os
import json

class Lexer():
    def __init__(self):
        self.tokens = []
        self.keywords = ["$NAME", "$DESC", "$CODE", "#DEFINE", "IF", "ELSE", "PRINT", "CONNECT", "SEND", "RECEIVE"]
        self.operators = ["==", ">", "<", "<=", ">=", "!="]
        self.delimiters = ["{", "}", "(", ")", "[", "]"]
        self.operators = ["+", "-", "*", "/"]
        self.punctuation = [",", ";", ":"]
        self.string = ["'", '"']
        self.action = ["#"]
        self.comment = ["//", "/*", "*/"]
        self.whitespace = [" ", "\n", "\t"]
        self.identifiers = []
        
        
            # lexer function

    def lex(self,source_code):
        token_patterns = [
        ('NUMBER', r'\d+'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('OPERATOR', r'[+\-*/]'),
        ('WHITESPACE', r'\s+'),
        ('STRING', r'\".*?\"'),
        ('STRING', r'\'.*?\''),
        ('PUNCTUATION', r'[,;:]'),
        ('DELIMITER', r'[()\[\]\{\}]'),
        ('COMMENT', r'//.*?$'),
        ('COMMENT', r'/\*.*?\*/'),
        ('UNKNOWN', r'.')
        ]
        
        while source_code:
            for token_type, pattern in token_patterns:
                regex = re.compile(pattern)
                match = regex.match(source_code)
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':  # Skip whitespace
                        self.tokens.append((token_type, value))
                    source_code = source_code[match.end():]  # Move past this token
                    break
            else:
                print('Syntax Error:', source_code)
                sys.exit(1)
        return self.tokens


class Parser():
    def __init__(self):
        self.tokens = []
        self.tree = []
        self.keywords = ["$NAME", "$DESC", "$CODE","$TEST","#DEFINE", "IF", "ELSE", "PRINT", "CONNECT", "SEND", "RECEIVE"]
        self.operators = ["==", ">", "<", "<=", ">=", "!="]
        self.delimiters = ["{", "}", "(", ")", "[", "]"]
        self.operators = ["+", "-", "*", "/"]
        self.punctuation = [",", ";", ":"]
        self.string = ["'", '"']
        self.action = ["#"]
        self.comment = ["//", "/*", "*/"]
        self.whitespace = [" ", "\n", "\t"]
        self.identifiers = []
        
    def parse(self, tokens):
        self.tokens = tokens
        self.tree = self.parse_codeblock()
        return self.tree
    
    def parse_codeblock(self):
        
    
if __name__ == "__main__":
    # test the lexer
    lexer = Lexer()
    code = """
    $NAME: test1
    $TEST: WEBSOCKET
$DESC: test1 description
#DEFINE CONNECT(WEBSOCKET_URL, PORT)
#DEFINE SEND(WBSOCKET_MESSAGE)
#DEFINE contents
$CODE{
    CONNECT("localhost", 8080)
    IF [CONNECTED()]
    {
        SEND("{message: 'hello'}")
        RECEIVE() > contents
        
        IF [contents == "hello"]
        {
            PRINT("Test Passed")
        }
        ELSE
        {
            PRINT("Test Failed")
        } 
        
    }
    ELSE
    {
        PRINT("Failed to connect")
    }
}
"""

contents = lexer.lex(code)
for token in contents:
    print(token)
    print("\n")
    
    
#     # test the parser
# parser = Parser()
# parser.parse(contents)
# print(parser.tree)


# # test the interpreter
# interpreter = Interpreter()
# interpreter.interpret(parser.tree)
# print(interpreter.tree)
# print(interpreter.variables)