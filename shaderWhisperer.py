from antlr4 import *
from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from Singleton import Result
from Structs import *
from myGLSLListener import *

class shaderWhisperer():   
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

    def calls(self, funcName, fileName):
        #TODO: handle fileName not defined (try to define automatically on call?)
        tree = self._createTree(fileName)
        printer = callGLSLListener(funcName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return self._result.getValue()
    
    
    def sentences(self, sentenceName, fileName):
        #TODO: Do
        tree = self._createTree(fileName)
        printer = sentenceGLSLListener(sentenceName)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return self._result.getValue()
        
    
    