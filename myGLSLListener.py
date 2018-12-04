# Generated from GLSL.g4 by ANTLR 4.7.1
from antlr4 import *
from GLSLParser import GLSLParser
if __name__ is not None and "." in __name__:
    from .build.classes.GLSLListener import *
    from .Structs import *
else:
    from build.classes.GLSLListener  import *
    from Structs import *



class declGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name #var name
        self.result = []
        
    def _getType(self, ctx:GLSLParser.Type_specifierContext):
        type = ctx.type_specifier_nonarray().getText()
        #is it array? buf. get ALL the array contexts to know the type
        #get directly the text (with the expression)?
        arrayCtxs = ctx.getTypedRuleContexts(GLSLParser.Array_specifierContext)
        for ctxArraySpecifier in arrayCtxs:
            type += "[]"
            
        return type
        
    def enterFunc_decl_member(self, ctx:GLSLParser.Func_decl_memberContext):
        if(ctx.IDENTIFIER() != None):
            token = ctx.IDENTIFIER().getSymbol()
            if(token.text == self.name):
                type = self._getType(ctx.type_specifier())
                self.result.append((type, srcPoint(token.line, token.column))) 
        pass
    
    # Enter a parse tree produced by GLSLParser#simple_declaration.
    def enterSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        #simple_declarator --> left_value
        #store the variable name
         
        declaratorCtxs = ctx.getTypedRuleContexts(GLSLParser.Simple_declaratorContext)
        for ctxDeclarator in declaratorCtxs:
            if(ctxDeclarator.getText() == self.name):
                token = ctxDeclarator.getChild(0).getChild(0).getSymbol()
                type = self._getType(ctx.type_specifier())
                self.result.append((type,srcPoint(token.line, token.column)))
        pass
    
    

class storageGLSLListener(declGLSLListener):
#TODO: change names that refer to tokens to the actual
# GLSLParser.token type and check them
    def __init__(self, name):
        self.name = name #in, out
        self.varName = None
        self.pos = None
        self.type = None
        self.result = []
        
    def enterSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        #does the declaration have "out" or "in" storage qualifiers?
        if(ctx.type_qualifier() != None):
            ctxTypeQualifier = ctx.type_qualifier()
            storageCtxs = ctxTypeQualifier.getTypedRuleContexts(GLSLParser.Storage_qualifierContext)
            for ctxStorageQualifier in storageCtxs:
                token = ctxStorageQualifier.getChild(0).getSymbol()
                if(token.text == self.name):
                    self.pos = srcPoint(token.line, token.column)
                    break
                
            if(self.pos != None):
                #we have found a storage qualifier that matches
                #store type using parent class getType function
                self.type = self._getType(ctx.type_specifier())
                
                #store the variable name
                declaratorCtxs = ctx.getTypedRuleContexts(GLSLParser.Simple_declaratorContext)
                for ctxDeclarator in declaratorCtxs:
                    self.result.append((ctxDeclarator.getText(), self.type, self.pos))
                    
                self.pos = None
                self.type = None     
        pass
    
    #override parent listener
    def enterFunc_decl_member(self, ctx:GLSLParser.Func_decl_memberContext):
        pass
    
    
class usesGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name #var name
        self.result = []
        
    def enterLeft_value(self, ctx:GLSLParser.Left_valueContext):
        if(ctx.IDENTIFIER() != None):
            token = ctx.IDENTIFIER().getSymbol()
            if(token.text == self.name):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
class assigGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name #var name
        self.result = []
        
    def enterAssignment_statement(self, ctx:GLSLParser.Assignment_statementContext):
        #Assignment_statement --> left_value
        if( ctx.left_value().IDENTIFIER() != None):
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
    