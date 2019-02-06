import sys
from antlr4 import *
from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from Structs import *
from myGLSLListener import *
from myGLSLVisitor import *

class shaderWhisperer():
    def __init__(self):
        self._sources = {}

    
    #TODO: handle fileName not defined (try to define automatically on call?)        
    def __getTree(self, filename):
        try:
            file = FileStream(self._sources[filename])
        except FileNotFoundError:
            sys.stderr.write("FileNotFoundError: No such file or directory: "+str(self._sources[filename])+"\n")
            return [srcPoint(-1,-1)]
        except KeyError:
            sys.stderr.write("KeyError: Not defined source: "+str(filename)+"\n")
            return [srcPoint(-1,-1)]
        lexer = GLSLLexer(file)
        stream = CommonTokenStream(lexer)
        parser = GLSLParser(stream)
        tree = parser.prog()
        return tree
    
    def __callListener(self, listener, filename, name=None):
        tree = self.__getTree(filename)
        printer =  listener(name) if (name != None) else listener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return printer.result
    
    def __callVisitor(self, filename, name=None):
        tree = self.__getTree(filename)
        visitor = funcDefVisitor()
        functions = visitor.visit(tree)
        mainCtx = None
        for (foo, st_list) in functions:
            if foo == "main":
                mainCtx = st_list
        if mainCtx is None:
            sys.stderr.write("Error: No main function: "+str(self._sources[filename])+"\n")
            return NULL
        
        visitor = statementVisitor()
        ret = mainCtx.accept(visitor)
        print(visitor.vars)
        return ret
    
    def __uses(self, file, name):
        allInstances = self.__callListener(usesGLSLListener, file, name)
        decls = self.declarations(name, file)
        assigs = self.assignments(name, file)
        return [x for x in [y for y in allInstances if y not in [item[1] for item in decls]] if x not in assigs]
        
    
    def __storage(self, file, storage):
        #ins es [(name, type, srcPos), ...]
        ins = self.__callListener(storageGLSLListener, file, storage)
        res = []
        for (name, type, pos) in ins:
            #for inVars we search for usage, outVars we search for assignemnt
            usesOrAssigns = self.uses(name, file) if storage == "in" else self.assignments(name, file)
            usedOrAssigned = len(usesOrAssigns) > 0
            res.append((name, type, pos, usedOrAssigned))
        return res
        
    def addSource(self, name, path):
        #TODO: when working with glsl & Cpp store
        #type of file in addition to path
        #and call the appropriate listener for each language
        self._sources[name] = path;
     
    #Para cada variable in, se proporciona una tupla que indica: (id, type, pos, used)   
    def outVars(self, file):
        return self.__storage(file, "out")
        
    def inVars(self, file):
        return self.__storage(file, "in")   
    
    def uses(self, name, file):
        return self.__uses(file, name)
        
    def assignments(self, name, file):
        return self.__callListener(assigGLSLListener, file, name)
    
    def declarations(self, name, file):
        return self.__callListener(declGLSLListener, file, name)
        
    def calls(self, name, file):
        return self.__callListener(callGLSLListener, file, name)
    
    def sentences(self, name, file):
        return self.__callListener(sentenceGLSLListener, file, name)
    
    def expressions(self, name, file):
        return self.__callListener(expressionGLSLListener, file, name)
    
    def tryVisitor(self, name, file):
        return self.__callVisitor(file, name)
    
        
    
    