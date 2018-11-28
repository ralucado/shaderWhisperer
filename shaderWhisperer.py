from antlr4 import *
from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from myGLSLListener import *

class shaderWhisperer():
    
    def __init__(self):
        self.sources = {}
        
    def addSource(self, name, path):
        self.sources[name] = path;

    def calls(self, funcName, fileName):
        #TODO: handle fileName not defined (try to define automatically on call?)
        file = FileStream(self.sources[fileName])
        lexer = GLSLLexer(file)
        stream = CommonTokenStream(lexer)
        parser = GLSLParser(stream)
        tree = parser.prog()
        printer = callGLSLListener(funcName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)   
        return [1]
    
    def sentences(self, funcName, fileName):
        #TODO: Do
        file = FileStream(self.sources[fileName])
        lexer = GLSLLexer(file)
        stream = CommonTokenStream(lexer)
        parser = GLSLParser(stream)
        tree = parser.prog()
        printer = callGLSLListener(funcName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)   
        return [1]