from antlr4 import *

from build.classes.GLSLListener import *
from build.classes.GLSLParser import GLSLParser
from Structs import *


class swizzleNameGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = list(name) #swizzle name
        self.lastVar = ""
        self.result = []

    # Enter a parse tree produced by GLSLParser#array_struct_selection.
    def enterArray_struct_selection(self, ctx:GLSLParser.Array_struct_selectionContext):
        if ctx.struct_specifier() is not None:
            for struct_specifier in ctx.struct_specifier():
                swizzle = list(struct_specifier.left_value_exp().left_value().getText())
                if all(elem in swizzle for elem in self.name):
                    if self.lastVar == "": print("NOOOO")
                    token = struct_specifier.DOT().getSymbol()
                    self.result.append((self.lastVar, srcPoint(token.line, token.column)))
                    self.lastVar = ""
                    break

    def enterLeft_value_exp(self, ctx:GLSLParser.Left_value_expContext):
        self.lastVar = ctx.left_value().getText()


class swizzleTypeGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name #swizzle name
        self.result = []

class declGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name #var name
        self.result = []
        
    def _getType(self, ctx:GLSLParser.Type_specifierContext):
        type = ctx.type_specifier_nonarray().getText()
        #is it array? buf. get ALL the array contexts to know the type
        #get directly the text (with the expression)?
        for ctxArraySpecifier in ctx.array_specifier():
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
        for ctxDeclarator in ctx.simple_declarator():
            if(ctxDeclarator.left_value().IDENTIFIER().getText() == self.name):
                token = ctxDeclarator.left_value().IDENTIFIER().getSymbol()
                type = self._getType(ctx.type_specifier())
                self.result.append((type,srcPoint(token.line, token.column)))
        pass
    
    

class storageGLSLListener(declGLSLListener):
#TODO: change names that refer to tokens to the actual
# GLSLParser.token type and check them
    def __init__(self, name, type):
        self.name = name #in, out
        self.type = type
        self.result = []
        
    def enterSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        #does the declaration have "out" or "in" storage qualifiers?
        if(ctx.type_qualifier() != None):
            ctxTypeQualifier = ctx.type_qualifier()
            storageCtxs = ctxTypeQualifier.storage_qualifier()
            pos = None
            type = None
            for ctxStorageQualifier in storageCtxs:
                token = ctxStorageQualifier.getChild(0).getSymbol()
                if(token.text == self.name):
                    pos = srcPoint(token.line, token.column)
                    break
                
            if(pos != None):
                #we have found a storage qualifier that matches
                if(self.type):
                    #store type using parent class getType function
                    type = self._getType(ctx.type_specifier())
                    self.result.append((type, pos))
                else:
                    #store the variable name
                    for ctxDeclarator in ctx.simple_declarator():
                        self.result.append((ctxDeclarator.getText(), pos))   
        pass
    
    #override parent listener
    def enterFunc_decl_member(self, ctx:GLSLParser.Func_decl_memberContext):
        pass
    
    
class storageNameGLSLListener(storageGLSLListener):
#TODO: change names that refer to tokens to the actual
# GLSLParser.token type and check them
    def __init__(self, name):
        self.name = name #in, out
        self.type = False
        self.result = []
        
        
class storageTypeGLSLListener(storageGLSLListener):
#TODO: change names that refer to tokens to the actual
# GLSLParser.token type and check them
    def __init__(self, name):
        self.name = name #in, out
        self.type = True
        self.result = []
        
        
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
    
    def enterType_specifier_nonarray(self, ctx:GLSLParser.Type_specifier_nonarrayContext):
        if(ctx.IDENTIFIER() != None):
            token = ctx.IDENTIFIER().getSymbol();
            if (self.name == token.text):
                self.result.append(srcPoint(token.line, token.column))
                
                
    def enterBasic_type_exp(self, ctx:GLSLParser.Basic_type_expContext):
        if(ctx.basic_type() is not None):
            token = None
            if(ctx.basic_type().scala_type() is not None):
                token = ctx.basic_type().scala_type().SCALA().getSymbol()
            elif(ctx.basic_type().vector_type() is not None):
                token = ctx.basic_type().vector_type().VECTOR().getSymbol()
            elif(ctx.basic_type().matrix_type() is not None):
                token = ctx.basic_type().matrix_type().MATRIX().getSymbol()
            if(token is not None and token.text == self.name):
                self.result.append(srcPoint(token.line, token.column))

class paramGLSLListener(GLSLListener):
    def __init__(self, param):
        self.name = param[0]
        self.i = param[1]
        self.result = []       
    
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
    
    #if
    def enterSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        if(self.name == "if"  and ctx.IF() != None):
            token = ctx.IF().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
    #while, do, for 
     # Enter a parse tree produced by GLSLParser#case.
    def enterCase(self, ctx:GLSLParser.CaseContext):
        if self.name == "case":
            token = ctx.CASE().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass

    # Enter a parse tree produced by GLSLParser#default.
    def enterDefault(self, ctx:GLSLParser.DefaultContext):
        if self.name == "default":
            token = ctx.DEFAULT().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass

    # Enter a parse tree produced by GLSLParser#while.
    def enterWhile(self, ctx:GLSLParser.WhileContext):
        if self.name == "while":
            token = ctx.WHILE().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass

     # Enter a parse tree produced by GLSLParser#do.
    def enterDo(self, ctx:GLSLParser.DoContext):
        if self.name == "do":
            token = ctx.DO().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass

 # Enter a parse tree produced by GLSLParser#for.
    def enterFor(self, ctx:GLSLParser.ForContext):
        if self.name == "for":
            token = ctx.FOR().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass
    
    def enterContinue(self, ctx:GLSLParser.ContinueContext):     
        if self.name == "continue":
            token = ctx.CONTINUE().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass

    # Enter a parse tree produced by GLSLParser#break.
    def enterBreak(self, ctx:GLSLParser.BreakContext):     
        if self.name == "break":
            token = ctx.BREAK().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass


    # Enter a parse tree produced by GLSLParser#return.
    def enterReturn(self, ctx:GLSLParser.ReturnContext):     
        if self.name == "return":
            token = ctx.RETURN().getSymbol()
            if(token != None):
                self.result.append(srcPoint(token.line, token.column)) 
        pass

    
class expressionGLSLListener(GLSLListener):
    def __init__(self, name):
        self.name = name #var name
        self.result = []
        self.tabstack = []
            
       # switch
    def enterSwitch_statement(self, ctx:GLSLParser.Switch_statementContext):
        token = ctx.SWITCH().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"return", token.line, token.column)
        pass
    
    #if
    def enterSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        token = ctx.IF().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"if", token.line, token.column)
        pass
    #else
    def enterSelection_rest_statement(self, ctx:GLSLParser.Selection_rest_statementContext):
        token = ctx.ELSE().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"else", token.line, token.column)
        pass

    #while, do, for 
     # Enter a parse tree produced by GLSLParser#case.
    def enterCase(self, ctx:GLSLParser.CaseContext):
        token = ctx.CASE().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"case", token.line, token.column)
        pass

    # Enter a parse tree produced by GLSLParser#default.
    def enterDefault(self, ctx:GLSLParser.DefaultContext):
        token = ctx.DEFAULT().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"default", token.line, token.column)
        pass

    # Enter a parse tree produced by GLSLParser#while.
    def enterWhile(self, ctx:GLSLParser.WhileContext):
        token = ctx.WHILE().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"while", token.line, token.column)
        pass

     # Enter a parse tree produced by GLSLParser#do.
    def enterDo(self, ctx:GLSLParser.DoContext):
        token = ctx.DO().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"do", token.line, token.column)
        pass

 # Enter a parse tree produced by GLSLParser#for.
    def enterFor(self, ctx:GLSLParser.ForContext):
        token = ctx.FOR().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"for", token.line, token.column)
        pass
    
    def enterContinue(self, ctx:GLSLParser.ContinueContext):     
        token = ctx.CONTINUE().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"continue", token.line, token.column)
        pass

    # Enter a parse tree produced by GLSLParser#break.
    def enterBreak(self, ctx:GLSLParser.BreakContext):     
        token = ctx.BREAK().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"break", token.line, token.column)
        pass


    # Enter a parse tree produced by GLSLParser#return.
    def enterReturn(self, ctx:GLSLParser.ReturnContext):     
        token = ctx.RETURN().getSymbol()
        if(token != None):
            print(''.join(self.tabstack),"return", token.line, token.column)
        pass
    
    def enterStatement_list(self, ctx:GLSLParser.Statement_listContext):
        print(''.join(self.tabstack),"{")
        self.tabstack.append("    ")
        pass
    
    def exitStatement_list(self, ctx:GLSLParser.Statement_listContext):
        del self.tabstack[-1]
        print(''.join(self.tabstack),"}")
        pass
