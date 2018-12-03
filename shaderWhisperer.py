from antlr4 import *
from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from Singleton import Result
from Structs import *
from myGLSLListener import *

class shaderWhisperer():
    #TODO: write wrapper for each function that passes the appropriate
    # listener class to a single implementation of the parsing function 
    
    def __init__(self):
        self._sources = {}
        self._result = Result()
        
    def _createTree(self, fileName):
        file = FileStream(self._sources[fileName])
        lexer = GLSLLexer(file)
        stream = CommonTokenStream(lexer)
        parser = GLSLParser(stream)
        return(parser.prog())
        
    def addSource(self, name, path):
        self._sources[name] = path;
        
    #TODO: handle fileName not defined (try to define automatically on call?)        
    def declarations(self, varName, fileName):
        tree = self._createTree(fileName)
        printer = declGLSLListener(varName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return self._result.getValue()
        
    def calls(self, funcName, fileName):
        tree = self._createTree(fileName)
        printer = callGLSLListener(funcName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return self._result.getValue()
    
    def sentences(self, sentenceName, fileName):
        tree = self._createTree(fileName)
        printer = sentenceGLSLListener(sentenceName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return self._result.getValue()
        
    
    