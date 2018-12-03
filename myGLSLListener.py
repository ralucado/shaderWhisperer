# Generated from GLSL.g4 by ANTLR 4.7.1
from antlr4 import *
from GLSLParser import GLSLParser
if __name__ is not None and "." in __name__:
    from .build.classes.GLSLListener import *
    from .Structs import *
else:
    from build.classes.GLSLListener  import *
    from Structs import *

class insGLSLListener(GLSLListener):
    def __init__(self):
        self.r = []
    

class usesGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name
        self.result = []
        
    def enterLeft_value(self, ctx:GLSLParser.Left_valueContext):
        if(ctx.IDENTIFIER() != None):
            token = ctx.IDENTIFIER().getSymbol()
            if(token.text == self.name):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
class assigGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name
        self.result = []
        
    def enterAssignment_statement(self, ctx:GLSLParser.Assignment_statementContext):
        #Assignment_statement --> left_value
        if( ctx.left_value().IDENTIFIER() != None):
            token = ctx.left_value().IDENTIFIER().getSymbol()
            if(token.text == self.name):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
class declGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name
        self.result = []
    
    def enterFunc_decl_member(self, ctx:GLSLParser.Func_decl_memberContext):
        if(ctx.IDENTIFIER() != None):
            token = ctx.IDENTIFIER().getSymbol()
            if(token.text == self.name):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
    # Enter a parse tree produced by GLSLParser#simple_declaration.
    def enterSimple_declarator(self, ctx:GLSLParser.Simple_declaratorContext):
        #simple_declarator --> left_value
        if(ctx.left_value().IDENTIFIER() != None):
            token = ctx.left_value().IDENTIFIER().getSymbol()
            if(token.text == self.name):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
    
class callGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name
        self.result = []
            
    # Enter a parse tree produced by GLSLParser#function_call.
    def enterFunction_call(self, ctx:GLSLParser.Function_callContext):
        if(ctx.function_name().IDENTIFIER() != None):
            token = ctx.function_name().IDENTIFIER().getSymbol();
            if (self.name == token.text):
                self.result.append(srcPoint(token.line, token.column))
        pass
    
class sentenceGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name.strip().lower()
        self.result = []
            
    # switch
    def enterSwitch_statement(self, ctx:GLSLParser.Switch_statementContext):
        if(self.name == "switch" and ctx.SWITCH() != None):
            token = ctx.SWITCH().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
    # case, default
    def enterCase_label(self, ctx:GLSLParser.Case_labelContext):
        token = None
        if(self.name == "case" and ctx.CASE() != None):
            token = ctx.CASE().getSymbol()
        elif(self.name == "default" and ctx.DEFAULT() != None):
            token = ctx.DEFAULT().getSymbol()
        if(token != None):
            self.result.append(srcPoint(token.line, token.column)) 
        pass
    
    #if
    def enterSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        if(self.name == "if"  and ctx.IF() != None):
            token = ctx.IF().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
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
            self.result.append(srcPoint(token.line, token.column)) 
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
            self.result.append(srcPoint(token.line, token.column)) 
        pass
    