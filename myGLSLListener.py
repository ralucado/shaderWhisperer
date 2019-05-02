from antlr4 import *
import logging

from build.classes.GLSLListener import *
from build.classes.GLSLParser import GLSLParser
from myGLSLVisitor import typeVisitor
from Structs import *
        
class variablesListener(GLSLListener):
    def __init__(self, setup):
        self.result = []
        self.variables = []
        self.setup = setup
        self.variables.append(setup.getBuiltins())

    def _getType(self, ctx:GLSLParser.Type_specifierContext):
        type = ctx.type_specifier_nonarray().getText()
        #is it array? buf. get ALL the array contexts to know the type
        #get directly the text (with the expression)?
        for ctxArraySpecifier in ctx.array_specifier():
            type += "[]"
        return type
    
    def _getExprType(self, expr):
        vis = typeVisitor(self.variables)
        return(expr.accept(vis))
    

    def enterStatement_list(self, ctx:GLSLParser.Statement_listContext):
        #add a new scope of variables
        self.variables.append({})
        pass

    def exitStatement_list(self, ctx:GLSLParser.Statement_listContext):
        #remove last scope of variables
        self.variables.pop()
        #print(self.variables.pop())
        pass

    def enterFunction_definition(self, ctx:GLSLParser.Function_definitionContext):
        returnType = self._getType(ctx.return_Type().type_specifier())
        funcName = ctx.function_name().IDENTIFIER().getText()
        #save function return type in global scope
        self.variables[0]["func."+funcName] = returnType
        params = {}
        for param in ctx.func_decl_member():
            params[param.IDENTIFIER().getText()] = self._getType(param.type_specifier())
        #save function parameters to add to the scope when function is called
        self.variables.append(params)
        pass

    def exitFunction_definition(self, ctx:GLSLParser.Function_definitionContext):
        self.variables.pop()
        pass

    # Enter a parse tree produced by GLSLParser#simple_declaration.
    def enterSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        #calculate the variables type
        type = self._getType(ctx.type_specifier())
        for ctxDeclarator in ctx.simple_declarator():
            #logging.debug(ctxDeclarator.getText())
            #store each variable in the declaration with the same type
            if(ctxDeclarator.left_value().IDENTIFIER() is not None):
                name = ctxDeclarator.left_value().IDENTIFIER().getText()
                #save in the innermost scope
                self.variables[-1][name] = type
        pass


class swizzleTypeGLSLListener(variablesListener):
    def __init__(self, params): #(name, setup)
        self.name = list(params[0]) #swizzle name
        self.lastValue = ""
        self.result = []
        super().__init__(params[1]) #pass the setup

    def addToResult(self, struct_specifier):
        type = self._getExprType(self.lastValue)
        token = struct_specifier.DOT().getSymbol()
        self.result.append((type, srcPoint(token.line, token.column)))
        self.lastValue = ""
        
    # Enter a parse tree produced by GLSLParser#array_struct_selection.
    def enterArray_struct_selection(self, ctx:GLSLParser.Array_struct_selectionContext):
        if ctx.struct_specifier() is not None:
            for struct_specifier in ctx.struct_specifier():
                swizzle = list(struct_specifier.left_value_exp().left_value().getText())
                if all(elem in swizzle for elem in self.name):
                    if self.lastValue == "": logging.debug("Swizzle could not find a variable to apply to.")
                    self.addToResult(struct_specifier)
                    break
        pass

    def exitLeft_value(self, ctx:GLSLParser.Left_valueContext):
        #save the last uppermost leftvalue visited in case of encountering a swizzle next
        self.lastValue = ctx
        pass

class swizzleNameGLSLListener(swizzleTypeGLSLListener):

    def addToResult(self, struct_specifier):
        token = struct_specifier.DOT().getSymbol()
        self.result.append((self.lastValue.getText(), srcPoint(token.line, token.column)))
        self.lastValue = ""


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
            token = ctx.function_name().IDENTIFIER().getSymbol()
            if (self.name == token.text):
                self.result.append(srcPoint(token.line, token.column))
        pass
    
    def enterType_specifier_nonarray(self, ctx:GLSLParser.Type_specifier_nonarrayContext):
        if(ctx.IDENTIFIER() != None):
            token = ctx.IDENTIFIER().getSymbol()
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

    # Enter a parse tree produced by GLSLParser#postIncrement.
    def enterPostIncrement(self, ctx:GLSLParser.PostIncrementContext):
        if(self.name == ctx.INCREMENT_OP().getText()):
            token = ctx.INCREMENT_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#preIncrement.
    def enterPreIncrement(self, ctx:GLSLParser.PreIncrementContext):
        if(self.name == ctx.INCREMENT_OP().getText()):
            token = ctx.INCREMENT_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass
                
    # Enter a parse tree produced by GLSLParser#sign.
    def enterSign(self, ctx:GLSLParser.SignContext):
        if(self.name == ctx.ADDSUB_OP().getText()):
            token = ctx.ADDSUB_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#unary.
    def enterUnary(self, ctx:GLSLParser.UnaryContext):
        if(self.name == ctx.UNARY_OP().getText()):
            token = ctx.UNARY_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#muldiv.
    def enterMuldiv(self, ctx:GLSLParser.MuldivContext):
        if(self.name == ctx.MULDIV_OP().getText()):
            token = ctx.MULDIV_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#addsub.
    def enterAddsub(self, ctx:GLSLParser.AddsubContext):
        if(self.name == ctx.ADDSUB_OP().getText()):
            token = ctx.ADDSUB_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#shift.
    def enterShift(self, ctx:GLSLParser.ShiftContext):
        if(self.name == ctx.SHIFT_OP().getText()):
            token = ctx.SHIFT_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#cmp.
    def enterCmp(self, ctx:GLSLParser.CmpContext):
        if(self.name == ctx.COMPARE_OP().getText()):
            token = ctx.COMPARE_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#eq.
    def enterEq(self, ctx:GLSLParser.EqContext):
        if(self.name == ctx.EQUAL_OP().getText()):
            token = ctx.EQUAL_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#bitwise.
    def enterBitwise(self, ctx:GLSLParser.BitwiseContext):
        if(self.name == ctx.BITWISE_OP().getText()):
            token = ctx.BITWISE_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass

    # Enter a parse tree produced by GLSLParser#logic.
    def enterLogic(self, ctx:GLSLParser.LogicContext):
        if(self.name == ctx.LOGIC_OP().getText()):
            token = ctx.LOGIC_OP().getSymbol()
            self.result.append(srcPoint(token.line, token.column))
        pass
                
class paramTypeGLSLListener(variablesListener):
    def __init__(self, params): #params = (name, i, setup)
        self.name = params[0] #name of function
        self.i = params[1] - 1 #parameter number, startin from 0
        self.result = []
        super().__init__(params[2])
    
    def updateResult(self, ctx):
        type = self._getExprType(ctx)
        self.result.append(type)

    # Enter a parse tree produced by GLSLParser#function_call.
    def enterFunction_call(self, ctx:GLSLParser.Function_callContext):
        if(ctx.function_name().IDENTIFIER() != None):
            token = ctx.function_name().IDENTIFIER().getSymbol()
            if (self.name == token.text):
                expression = ctx.expression(self.i)
                if expression is not None:
                    self.updateResult(expression)
        pass
    
    def enterSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        super().enterSimple_declaration(ctx)
        fname = ctx.type_specifier()
        if(self.i == 0 and fname is not None):
            fname = fname.type_specifier_nonarray()
            if(fname is not None and fname.IDENTIFIER() is not None):
                token = fname.IDENTIFIER().getSymbol()
                if (self.name == token.text):
                    self.updateResult(ctx.simple_declarator(0).left_value().expression())
        pass        
                
    def enterBasic_type_exp(self, ctx:GLSLParser.Basic_type_expContext):
        if(ctx.basic_type() is not None):
            if(ctx.basic_type().getText() == self.name):
                expression = ctx.expression(self.i)
                if(expression is not None):
                    self.updateResult(expression)
        pass

    #unary functions, only one parameter
    def enterPostIncrement(self, ctx:GLSLParser.PostIncrementContext):
        if(self.i == 0 and self.name == ctx.INCREMENT_OP().getText()):
            self.updateResult(ctx.expression())
        pass

    def enterPreIncrement(self, ctx:GLSLParser.PreIncrementContext):
        if(self.i == 0 and self.name == ctx.INCREMENT_OP().getText()):
            self.updateResult(ctx.expression())
        pass
                
    def enterSign(self, ctx:GLSLParser.SignContext):
        if(self.i == 0 and self.name == ctx.ADDSUB_OP().getText()):
            self.updateResult(ctx.expression())
        pass

    def enterUnary(self, ctx:GLSLParser.UnaryContext):
        if(self.i == 0 and self.name == ctx.UNARY_OP().getText()):
            self.updateResult(ctx.expression())
        pass

    #Binary functions
    def enterMuldiv(self, ctx:GLSLParser.MuldivContext):
        if(self.name == ctx.MULDIV_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass

    def enterAddsub(self, ctx:GLSLParser.AddsubContext):
        if(self.name == ctx.ADDSUB_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass

    def enterShift(self, ctx:GLSLParser.ShiftContext):
        if(self.name == ctx.SHIFT_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass

    def enterCmp(self, ctx:GLSLParser.CmpContext):
        if(self.name == ctx.COMPARE_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass

    def enterEq(self, ctx:GLSLParser.EqContext):
        if(self.name == ctx.EQUAL_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass

    def enterBitwise(self, ctx:GLSLParser.BitwiseContext):
        if(self.name == ctx.BITWISE_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass

    def enterLogic(self, ctx:GLSLParser.LogicContext):
        if(self.name == ctx.LOGIC_OP().getText()):
            self.updateResult(ctx.expression(self.i))
        pass
    
               
class paramNameGLSLListener(paramTypeGLSLListener):
    def updateResult(self, ctx):
        self.result.append(ctx.getText())


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
