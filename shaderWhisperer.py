from antlr4 import *
from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from Structs import *
from myGLSLListener import *

class shaderWhisperer():
    def __init__(self):
        self._sources = {}

    #TODO: handle fileName not defined (try to define automatically on call?)        
    def __callListener(self, listener, filename, name=None):
        file = FileStream(self._sources[filename])
        lexer = GLSLLexer(file)
        stream = CommonTokenStream(lexer)
        parser = GLSLParser(stream)
        tree = parser.prog()
        printer =  listener(name) if (name != None) else listener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return printer.result
        
        
    def addSource(self, name, path):
        self._sources[name] = path;
     
    #Para cada variable in, se proporciona una tupla que indica: (id, type, pos, used)   
    def inVars(self, file):
        #ins es [(name, type, srcPos), ...]
        ins = self.__callListener(insGLSLListener, filename)
        return ins
    
    def uses(self, name, file):
        return self.__callListener(usesGLSLListener, file, name)
        
    def assignments(self, name, file):
        return self.__callListener(assigGLSLListener, file, name)
    
    def declarations(self, name, file):
        return self.__callListener(declGLSLListener, file, name)
        
    def calls(self, name, file):
        return self.__callListener(callGLSLListener, file, name)
    
    def sentences(self, name, file):
        return self.__callListener(sentenceGLSLListener, file, name)
        
    
    