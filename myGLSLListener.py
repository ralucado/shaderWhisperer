# Generated from GLSL.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .build.classes.GLSLListener import *
    from .Singleton import Result
    from .Structs import *
else:
    from build.classes.GLSLListener  import *
    from Singleton  import Result
    from Structs import *

class callGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name
        self.r = Result()
            
    # Enter a parse tree produced by GLSLParser#function_call.
    def enterFunction_call(self, ctx:GLSLParser.Function_callContext):
        token = ctx.function_name().IDENTIFIER().getSymbol();
        if (self.name == token.text):
            self.r.addValue(srcPoint(token.line, token.column))
        pass
    
class sentenceGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name.strip().lower()
        self.r = Result()
            
    # switch
    def enterSwitch_statement(self, ctx:GLSLParser.Switch_statementContext):
        if(self.name == "switch" and ctx.SWITCH() != None):
            token = ctx.SWITCH().getSymbol()
            if(token != None):
                self.r.addValue(srcPoint(token.line, token.column)) 
        pass
    
    # case, default
    def enterCase_label(self, ctx:GLSLParser.Case_labelContext):
        token = None
        if(self.name == "case" and ctx.CASE() != None):
            token = ctx.CASE().getSymbol()
        elif(self.name == "default" and ctx.DEFAULT() != None):
            token = ctx.DEFAULT().getSymbol()
        if(token != None):
            self.r.addValue(srcPoint(token.line, token.column)) 
        pass
    
    #if
    def enterSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        if(self.name == "if"  and ctx.IF() != None):
            token = ctx.IF().getSymbol()
            if(token != None):
                self.r.addValue(srcPoint(token.line, token.column)) 
        pass
    
    #while, do, for    
    def enterIteration_statement(self, ctx:GLSLParser.Iteration_statementContext):
        token = None
        if(self.name == "while" and ctx.WHILE() != None):
            token = ctx.WHILE().getSymbol()
        elif(self.name == "for" and ctx.FOR() != None):
            token = ctx.FOR().getSymbol()
        elif(self.name == "do"  and ctx.DO() != None):
            token = ctx.DO().getSymbol()
        if(token != None):
            self.r.addValue(srcPoint(token.line, token.column)) 
        pass
    
    #continue, break, return
    def enterJump_statement(self, ctx:GLSLParser.Jump_statementContext):
        token = None
        if(self.name == "continue" and ctx.CONTINUE() != None):
            token = ctx.CONTINUE().getSymbol()
        elif(self.name == "break" and ctx.BREAK() != None):
            token = ctx.BREAK().getSymbol()
        elif(self.name == "return" and ctx.RETURN() != None):
            token = ctx.RETURN().getSymbol()
        if(token != None):
            self.r.addValue(srcPoint(token.line, token.column)) 
        pass
    