import logging
import sys

from antlr4 import *

from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from myGLSLListener import *
from myGLSLVisitor import *
from Setup import Setup
from Structs import *


def R(text, val):
    print(text+":",val)

class shaderWhisperer():
    def __init__(self, paths):
        self._sources = paths
        self._setup = Setup()

    
    #TODO: handle fileName not defined (try to define automatically on call?)        
    def __getTree(self, source):
        try:
            file = FileStream(source,self._setup.getEncoding())
        except FileNotFoundError:
            logging.error("FileNotFoundError: No such file or directory: "+str(source)+"\n")
            return [srcPoint(-1,-1)]
        lexer = GLSLLexer(file)
        stream = CommonTokenStream(lexer)
        parser = GLSLParser(stream)
        tree = parser.prog()
        return tree
    
    def __callListener(self, listener, param=None, joinResult=True):
        result = []
        for source in self._sources:
            #logging.debug("-------- Source: " + source + "----------")
            tree = self.__getTree(source)
            printer =  listener(param) if (param != None) else listener()
            walker = ParseTreeWalker()
            walker.walk(printer, tree)
            if joinResult: result += printer.result
            else: result.append(printer.result)
        return result
    
    def __spaces(self, name=None):
        result = []
        for source in self._sources:
            tree = self.__getTree(source)
            logging.info("Testing source "+source)
            visitor = funcDefVisitor()
            functions = visitor.visit(tree)
            mainCtx = None
            for (foo, st_list) in functions:
                if foo == "main":
                    mainCtx = st_list
            if mainCtx is None:
                logging.error("Error: No main function: "+str(source)+"\n")
                return None
            
            visitor = statementVisitor(self._setup)
            visitor.visit(tree)
            vars = self.__filterVars(visitor._currentState.vars)
            visitor = statementVisitor(self._setup)
            visitor.addVars(vars)
            mainCtx.accept(visitor)
            ret = {}
            for stateList in visitor.machineStates:
                for state in stateList:
                    vars = self.__filterVars(state.vars)
                    v = vars.get(name,None)
                    if v is not None:
                        visitedState = ret.get(state.getID(),[])
                        if(v[1] not in visitedState):
                            visitedState.append(v[1])
                            ret[state.getID()] = visitedState
            result += [ret[k] for k in sorted(ret.keys())]
        return result
    
    def __uses(self, name):
        result = []
        allInstances = self.__callListener(usesGLSLListener, name, joinResult=False)
        assigs = self.__callListener(assigGLSLListener, name, joinResult=False)
        decls = self.__callListener(declGLSLListener, name, joinResult=False)
        for i in range(0,len(self._sources)):
            result += [x for x in [y for y in allInstances[i] if y not in [item[1] for item in decls[i]]] if x not in assigs[i]]
        return result
        
    
    def __storage(self, storage, types):
        #ins es [[(name, type, srcPos), ...], [...], ...]
        listener = storageNameGLSLListener
        if(types): listener = storageTypeGLSLListener
        ins = self.__callListener(listener, storage)
        #to calc uses or assigns
        '''for i in range(0,len(self._sources)): 
            for (name, type, pos) in ins[i]:
                #for inVars we search for usage, outVars we search for assignemnt
                usesOrAssigns = self.uses(name) if storage == "in" else self.assignments(name)
                usedOrAssigned = len(usesOrAssigns) > 0
                res.append((name, type, pos, usedOrAssigned))
            result += res '''
        return ins
     
    
    #Para cada variable in, se proporciona una tupla que indica: (type, pos)   
    def outTypes(self):
        return self.__storage("out", True)
        
    def inTypes(self):
        return self.__storage("in", True)   
    
    def outNames(self):
        return self.__storage("out", False)
        
    def inNames(self):
        return self.__storage("in", False)   
    
    def uses(self, name):
        return self.__uses(name)
        
    def assignments(self, name):
        return self.__callListener(assigGLSLListener, name)
    
    def declarations(self, name):
        return self.__callListener(declGLSLListener, name)
        
    def calls(self, name):
        return self.__callListener(callGLSLListener, name)
    
    def sentences(self, name):
        return self.__callListener(sentenceGLSLListener, name)
    
    def param(self, name, i=1):
        return self.__callListener(paramNameGLSLListener, (name, i, self._setup))
    
    def paramType(self, name, i=1):
        return self.__callListener(paramTypeGLSLListener, (name, i, self._setup))
    
    def coordSpaces(self, name):
        return self.__spaces(name)
    
    def fieldSelectors(self, name):
        return self.__callListener(swizzleNameGLSLListener, (name, self._setup))

    def fieldSelectorsTypes(self, name):
        return self.__callListener(swizzleTypeGLSLListener, (name, self._setup))
    
    
    
    
    def numOutTypes(self):
        return len(self.outTypes())
        
    def numInTypes(self):
        return len(self.inTypes())
    
    def numOutNames(self):
        return len(self.outNames())
        
    def numInNames(self):
        return len(self.inNames()) 
    
    def numUses(self, name):
        return len(self.uses(name))
        
    def numAssignments(self, name):
        return len(self.assignments(name))
    
    def numDeclarations(self, name):
        return len(self.declarations(name))
        
    def numCalls(self, name):
        return len(self.calls(name))
    
    def numSentences(self, name):
        return len(self.sentences(name))
    
    def numParam(self, name, i=1):
        return len(self.param(name, i))
    
    def numParamType(self, name, i=1):
        return len(self.paramType(name, i))
    
    def numCoordSpaces(self, name):
        return len(self.coordSpaces(name))
    
    
    
    def setConstantCoordSpace(self, space):
        self._setup.setConstantExpressionSpace(space)
        
    def __filterVars(self, vars):
        defaultVars = self._setup.getDefaultVars()
        for varname in defaultVars.keys():
            vars.pop(varname, None)
        return vars
