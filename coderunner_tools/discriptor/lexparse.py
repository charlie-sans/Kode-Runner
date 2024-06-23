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

        
        while source_code:
            # check for whitespace
            if source_code[0] in self.whitespace:
                source_code = source_code[1:]
                
            # check for keywords
            elif source_code[:6] in self.keywords:
                self.tokens.append((source_code[:6], "KEYWORD"))
                source_code = source_code[6:]
                
            # check for operators
            elif source_code[:2] in self.operators:
                self.tokens.append((source_code[:2], "OPERATOR"))
                source_code = source_code[2:]
                
            # check for delimiters
            elif source_code[0] in self.delimiters:
                self.tokens.append((source_code[0], "DELIMITER"))
                source_code = source_code[1:]
                
            # check for punctuation
            elif source_code[0] in self.punctuation:
                self.tokens.append((source_code[0], "PUNCTUATION"))
                source_code = source_code[1:]
                
            # check for string
            elif source_code[0] in self.string:
                string = ""
                for char in source_code[1:]:
                    if char != source_code[0]:
                        string += char
                    else:
                        break
                self.tokens.append((string, "STRING"))
                source_code = source_code[len(string)+2:]
                
            # check for action
            elif source_code[0] in self.action:
                self.tokens.append((source_code[0], "ACTION"))
                source_code = source_code[1:]
                
            # check for comment
            elif source_code[:2] in self.comment:
                if source_code[:2] == "//":
                    comment = ""
                    for char in source_code[2:]:
                        if char != "\n":
                            comment += char
                        else:
                            break
                    self.tokens.append((comment, "COMMENT"))
                    source_code = source_code[len(comment)+2:]
                else:
                    comment = ""
                    for char in source_code[2:]:
                        if char != "*/":
                            comment += char
                        else:
                            break
                    self.tokens.append((comment, "COMMENT"))
                    source_code = source_code[len(comment)+4:]
                
            # check for identifiers
            else:
                identifier = ""
                for char in source_code:
                    if char not in self.whitespace+self.keywords+self.operators+self.delimiters+self.punctuation+self.string+self.action+self.comment:
                        identifier += char
                    else:
                        break
                self.tokens.append((identifier, "IDENTIFIER"))
                source_code = source_code[len(identifier):]
    
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
        self.action = ["#","$"]
        self.comment = ["//", "/*", "*/"]
        self.whitespace = [" ", "\n", "\t"]
        self.identifiers = []
        

def parse(self, tokens):
        self.tokens = tokens
        if self.tokens[0][0] == "$NAME":
            self.tree.append(("NAME", self.tokens[1][0]))
            self.tokens = self.tokens[2:]
        if self.tokens[0][0] == "$DESC":
            self.tree.append(("DESC", self.tokens[1][0]))
            self.tokens = self.tokens[2:]
        if self.tokens[0][0] == "$CODE":
            self.tree.append(("CODE", self.tokens[1][0]))
            self.tokens = self.tokens[2:]
        if self.tokens[0][0] == "$TEST":
            self.tree.append(("TEST", self.tokens[1][0]))
            self.tokens = self.tokens[2:]
        while self.tokens:
            if self.tokens[0][0] == "#DEFINE":
                self.tree.append(("DEFINE", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] == "IF":
                self.tree.append(("IF", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] == "ELSE":
                self.tree.append(("ELSE", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] == "PRINT":
                self.tree.append(("PRINT", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] == "CONNECT":
                self.tree.append(("CONNECT", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] == "SEND":
                self.tree.append(("SEND", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] == "RECEIVE":
                self.tree.append(("RECEIVE", self.tokens[1][0]))
                self.tokens = self.tokens[2:]
            elif self.tokens[0][0] in self.identifiers:
                self.tree.append(("IDENTIFIER", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.operators:
                self.tree.append(("OPERATOR", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.delimiters:
                self.tree.append(("DELIMITER", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.punctuation:
                self.tree.append(("PUNCTUATION", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.string:
                self.tree.append(("STRING", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.action:
                self.tree.append(("ACTION", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.comment:
                self.tree.append (("COMMENT", self.tokens[0][0]))
                self.tokens = self.tokens[1:]
            elif self.tokens[0][0] in self.whitespace:
                self.tokens = self.tokens[1:]
            else:
                self.tokens = self.tokens[1:]
        return self.tree
    
class Interpreter():
    def __init__(self):
        self.tree = []
        self.variables = {}
        self.functions = {}
        self.keywords = ["$NAME", "$DESC", "$CODE","$TEST","#DEFINE", "IF", "ELSE", "PRINT", "CONNECT", "SEND", "RECEIVE"]
        self.operators = ["==", ">", "<", "<=", ">=", "!="]
        self.delimiters = ["{", "}", "(", ")", "[", "]"]
        self.operators = ["+", "-", "*", "/"]
        self.punctuation = [",", ";", ":"]
        self.string = ["'", '"']
        self.action = ["#","$"]
        self.comment = ["//", "/*", "*/"]
        self.whitespace = [" ", "\n", "\t"]
        self.identifiers = []
        
    def interpret(self, tree):
        self.tree = tree
        for node in self.tree:
            if node[0] == "DEFINE":
                self.functions[node[1]] = []
            elif node[0] == "IF":
                if self.variables[node[1]]:
                    self.interpret(self.functions[node[1]])
            elif node[0] == "ELSE":
                self.interpret(self.functions[node[1]])
            elif node[0] == "PRINT":
                print(self.variables[node[1]])
            elif node[0] == "CONNECT":
                pass
            elif node[0] == "SEND":
                pass
            elif node[0] == "RECEIVE":
                pass
            elif node[0] == "IDENTIFIER":
                self.variables[node[1]] = None
            elif node[0] == "OPERATOR":
                pass
            elif node[0] == "DELIMITER":
                pass
            elif node[0] == "PUNCTUATION":
                pass
            elif node[0] == "STRING":
                pass
            elif node[0] == "ACTION":
                pass
            elif node[0] == "COMMENT":
                pass
            elif node[0] == "WHITESPACE":
                pass
            else:
                pass
        return self.variables
    

        
    
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
    parser = Parser()
    parser.parse(contents)
    print(parser.tree)


    # # test the interpreter
    # interpreter = Interpreter()
    # interpreter.interpret(parser.tree)
    # print(interpreter.tree)
    # print(interpreter.variables)