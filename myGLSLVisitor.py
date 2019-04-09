import logging
from copy import deepcopy

from antlr4 import *
from antlr4.tree.Tree import TerminalNode

from build.classes.GLSLParser import GLSLParser
from build.classes.GLSLVisitor import *
from Setup import Setup
from Structs import *


class funcDefVisitor(ParseTreeVisitor):
    
    # Visit a parse tree produced by GLSLParser#statement_list.
    def visitStatement_list(self, ctx:GLSLParser.Statement_listContext):
        l = []
        for c in ctx.getChildren():
            x = self.visit(c) 
            if x is not None:
                l.append(x)
        return l

    # Visit a parse tree produced by GLSLParser#function_definition.
    def visitFunction_definition(self, ctx:GLSLParser.Function_definitionContext):
        L = (ctx.function_name().IDENTIFIER().getText(),ctx.statement_list())
        C = self.visitChildren(ctx)
        if C is not None:
            return L + C
        return L
    
class expressionVisitor(ParseTreeVisitor):
    
    def __init__(self, variables, setup):
        self._variables = variables
        logging.debug(variables)
        self._setup = setup
        
    def isTransform(self,space):
        return len(space.split('.')) > 1
    
    def getTransform(self,t):
        s = t.split('.')
        return [s[1],s[2]]
    
    def getTransformFrom(self,t):
        s = t.split('.')
        return s[1]
    
    def getTransformTo(self,t):
        s = t.split('.')
        return s[2]
    
    def resultingFromTransform(self, t, space):
        ret = "wrong"
        if self.getTransformFrom(t) == space:
            ret = self.getTransformTo(t)
        return ret
    
    #returns the resulting coordinate space between a binary operation op of variable sin coord spaces left and right
    def resultingSpace(self, left, right, op):
        ret = "wrong"
        #A transform matrix can't be on the right
        if(self.isTransform(right) and op =="/" and left == "clip" and self.getTransformTo(right) == "NDC"):
            ret = "NDC"
        elif(self.isTransform(right)):
            ret = "wrong"
        elif left == right:
            ret = left
        elif "unknown" in [left,right]:
            ret = "unknown"
        elif op == "*" and self.isTransform(left):
            ret =  self.resultingFromTransform(left,right)
        elif left == "constant":
            ret = right
        elif right == "constant":
            ret = left
        else: ret =  "wrong"
        logging.debug(str(left)+str(op)+str(right)+" ----> "+str(ret))
        return ret
    
    #pre: spaces contains only "model,world,eye,clip" and "constant"
    def resultingSpaceFromList(self, spaces):
        spaces = list(dict.fromkeys(spaces)) #remove duplicates
        ret = ""
        if("wrong" in spaces):
            ret = "wrong"
        elif("unknown" in spaces):
            ret = "unknown"
        elif len(spaces) > 2: #we cannot have more than 2 spaces: a valid (eye, world, clip, model) and a constant
            ret = "wrong"
        elif len(spaces) == 1:
            ret = spaces[0]
        elif spaces[0] == "constant":
            ret = spaces[1]
        else: ret = spaces[0]
        logging.debug(str(spaces)+" ----> "+str(ret))
        return ret
    
    def aggregateResult(self, aggregate, nextResult):
        if nextResult is not None:
            return nextResult
        return aggregate
    
     # Visit a parse tree produced by GLSLParser#sign.
    def visitSign(self, ctx:GLSLParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#addsub.
    def visitAddsub(self, ctx:GLSLParser.AddsubContext):
        left = ctx.expression(0).accept(self)
        right = ctx.expression(1).accept(self)
        return self.resultingSpace(str(left),str(right), ctx.ADDSUB_OP().getText())
    
    # Visit a parse tree produced by GLSLParser#muldiv.
    def visitMuldiv(self, ctx:GLSLParser.MuldivContext):
        left = ctx.expression(0).accept(self)
        right = ctx.expression(1).accept(self)
        return self.resultingSpace(str(left),str(right), ctx.MULDIV_OP().getText())
    
    def visitLeft_value_exp(self, ctx:GLSLParser.Left_value_expContext):
        leftValue = ctx.left_value()
        hasW = False
        if(ctx.array_struct_selection() is not None):
            if len(ctx.array_struct_selection().struct_specifier()) > 0:
                logging.debug(ctx.getText())
                st = ctx.array_struct_selection().struct_specifier()[-1].accept(self)
                if len(st) == 1:
                    if st[0] == "w":
                        #logging.debug("---------------------------hasW")
                        hasW = True
                    else: return "constant"
                elif len(st) == 2:
                    return "wrong"
        if(leftValue.IDENTIFIER() is not None):
            #coord space of the variable stored in the dictionary
            if leftValue.IDENTIFIER().getText() in self._variables:
                space = self._variables[leftValue.IDENTIFIER().getText()][1] 
                if hasW:
                    if space == "clip": return "transform.clip.NDC"
                    return "constant"
                return space
            else: return "constant"
        if(leftValue.function_call() is not None):
            return "unknown"
        return self.visitChildren(leftValue)
    
    # Visit a parse tree produced by GLSLParser#struct_specifier.
    def visitStruct_specifier(self, ctx:GLSLParser.Struct_specifierContext):
        return ctx.left_value_exp().getText()
    
    # Visit a parse tree produced by GLSLParser#constant_expression.
    def visitConstant_expression(self, ctx:GLSLParser.Constant_expressionContext):
        return self._setup.getConstantExpressionSpace()
    
    # Visit a parse tree produced by GLSLParser#basic_type_exp.
    def visitBasic_type_exp(self, ctx:GLSLParser.Basic_type_expContext):
        if(ctx.basic_type().vector_type() is not None or ctx.basic_type().matrix_type() is not None):
            spaces = []
            for exp in ctx.expression():
                space = exp.accept(self)
                if(space == "wrong" or space == "unknown"): return space
                elif self.isTransform(space): #transform matrix in there
                    return "wrong"
                spaces.append(space)
            return self.resultingSpaceFromList(spaces)
        
        return "constant"


class statementVisitor(ParseTreeVisitor):
    def __init__(self, setup):
        super().__init__()
        self._setup = setup
        self._lastId = 0
        self._currentState = programState(0)
        self._currentState.vars = self._setup.getDefaultVars()
        self.machineStates = [[self._currentState]]
        self.vars = [] #temporal testing
        
    def addVars(self, vars):
        self._currentState.vars.update(vars)
    
    def _newState(self, id):
        self._currentState = self.machineStates[0][-1].increment(id)
        self.machineStates[0].append(self._currentState)
        
    def visitFunction_definition(self, ctx:GLSLParser.Function_definitionContext):
        return

    
    def visitChildren(self, node):
        result = []
        n = node.getChildCount()
        for i in range(n):
            c = node.getChild(i)
            childResult = c.accept(self)
            if childResult is not None:
                result.append(childResult)
        if len(result) == 1:
            return result[0]
        return result
    
    # Visit a parse tree produced by GLSLParser#statement_list.
    def visitStatement_list(self, ctx:GLSLParser.Statement_listContext):
        logging.debug(str(ctx.getSourceInterval()))
        c = ctx.getChildren()
        res = []
        for child in c:
            if len(self.machineStates) > 1:
                originalStateContext = deepcopy(self.machineStates)
                resultingStateContext = []
                for i in range(0, len(originalStateContext)):
                    self.machineStates = [deepcopy(originalStateContext[i])]
                    res.append(child.accept(self))
                    resultingStateContext += deepcopy(self.machineStates)
                self.machineStates += resultingStateContext
            else:
                res.append(child.accept(self))
        return ("{",res,"}")
    
    def visitSimple_statement(self, ctx:GLSLParser.Simple_statementContext):
        self._newState(ctx.getSourceInterval()[0])
        return ("{",self.visitChildren(ctx),"}")

    
    def visitDeclaration_statement(self, ctx:GLSLParser.Declaration_statementContext):
        r = self.visitChildren(ctx)
        if r is None:
            return "declaration"
        return r
    
    # Visit a parse tree produced by GLSLParser#simple_declaration.
    def visitSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        type = ctx.type_specifier().type_specifier_nonarray()
        if type is not None and type.basic_type() is not None:
            basictype = type.basic_type()
            if basictype.matrix_type() is not None:
                type = basictype.matrix_type()
            elif basictype.vector_type() is not None:
                type = basictype.vector_type()
            else:
                type = None
            if type is not None: 
                decls = ctx.simple_declarator()
                for id in decls:
                    typeString = type.getChild(0).getSymbol().text
                    if(typeString != "vec2"):
                        nameString = id.left_value().IDENTIFIER().getSymbol().text
                        space = "unknown"
                        if(id.assignment_expression() is not None):
                            vis = expressionVisitor(self._currentState.vars, self._setup)
                            space = vis.visitChildren(id.assignment_expression())
                            logging.debug(id.assignment_expression().getText())
                            logging.debug(space)
                        self._currentState.vars[nameString] = (typeString, space)
                        self.vars.append((typeString, nameString))
        return self.visitChildren(ctx)

    def visitLeft_value(self, ctx:GLSLParser.Left_valueContext):
        if(ctx.IDENTIFIER() is not None):
            return ctx.IDENTIFIER().getText()
        return self.visitChildren(ctx)

    
    def visitExpression(self, ctx:GLSLParser.ExpressionContext):
        return "expression"
    
    def visitAssignment_statement(self, ctx:GLSLParser.Assignment_statementContext):
        targetVar = ctx.left_value()
        if(targetVar.IDENTIFIER() is not None):
            targetVar = targetVar.IDENTIFIER().getText()
            op = " = "
            if  targetVar in self._currentState.vars.keys():
                expression = ""
                space = self._currentState.vars[targetVar][1]
                if ctx.assignment_expression() is not None:
                    expression = ctx.assignment_expression().expression()
                    #_overrideVar(targetVar, expression)
                    vis = expressionVisitor(self._currentState.vars, self._setup)
                    space = vis.visitChildren(ctx.assignment_expression())
                    logging.debug(ctx.assignment_expression().getText())
                    logging.debug(space)
                else:
                    op = ctx.arithmetic_assignment_expression().ARITHMETIC_ASSIGNMENT_OP().getText()
                    expression = ctx.arithmetic_assignment_expression().expression()
                    vis = expressionVisitor(self._currentState.vars, self._setup)
                    right = vis.visitChildren(ctx.arithmetic_assignment_expression())
                    left = self._currentState.vars[targetVar][1]
                    space = vis.resultingSpace(left, right, op)
                    logging.debug(ctx.arithmetic_assignment_expression().getText())
                    logging.debug(space)
                self._currentState.vars[targetVar] = (self._currentState.vars[targetVar][0], space)
                return targetVar + op + expression.getText()
        return "assignment"
    
    # Visit a parse tree produced by GLSLParser#selection_statement.
    def visitSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        cond = ctx.expression().accept(self)
        body_statement = ctx.selection_rest_statement().statement(0)
        originalStates = deepcopy(self.machineStates)
        body_s = body_statement.accept(self)
        afterBodyStates = deepcopy(self.machineStates)
        afterElseStates = originalStates
        else_s = ""
        else_statement = ctx.selection_rest_statement().statement(1) #Might be None
        if(else_statement is not None):
            self.machineStates = originalStates
            else_s = else_statement.accept(self)
            afterElseStates = deepcopy(self.machineStates)
        self.machineStates = afterBodyStates + afterElseStates
            
        return ("if", cond, body_s, "else", else_s)
    
    # Visit a parse tree produced by GLSLParser#selection_rest_statement.
    def visitSelection_rest_statement(self, ctx:GLSLParser.Selection_rest_statementContext):
        first = ctx.statement(0).accept(self)
        second = ctx.statement(1)
        if(second is None):
            return [first]
        second = second.accept(self)
        return [first, "else", second]
    
    
    # Visit a parse tree produced by GLSLParser#switch_statement.
    def visitSwitch_statement(self, ctx:GLSLParser.Switch_statementContext):
        return "switch"
            
    # Visit a parse tree produced by GLSLParser#case.
    def visitCase(self, ctx:GLSLParser.CaseContext):
        return "case"
            
    # Visit a parse tree produced by GLSLParser#default.
    def visitDefault(self, ctx:GLSLParser.DefaultContext):
        return "default"
            
    # Visit a parse tree produced by GLSLParser#while.
    def visitWhile(self, ctx:GLSLParser.WhileContext):
        cond = ctx.expression().accept(self)
        body_statement = ctx.statement()
        originalStates = deepcopy(self.machineStates)
        body_s = body_statement.accept(self)
        afterBodyStates = deepcopy(self.machineStates)
        self.machineStates = afterBodyStates + originalStates
        return ("while", cond, body_s)
            
    # Visit a parse tree produced by GLSLParser#do.
    def visitDo(self, ctx:GLSLParser.DoContext):
        cond = ctx.expression().accept(self)
        body_statement = ctx.statement()
        originalStates = deepcopy(self.machineStates)
        body_s = body_statement.accept(self)
        afterBodyStates = deepcopy(self.machineStates)
        self.machineStates = afterBodyStates + originalStates
        return ("do", body_s, "while", cond)

            
    # Visit a parse tree produced by GLSLParser#for.
    def visitFor(self, ctx:GLSLParser.ForContext):
        #init = ctx.for_init_statement().accept(self)
        cond = ctx.for_cond_statement().accept(self)
        originalStates = deepcopy(self.machineStates)
        stat_s = ctx.statement().accept(self)
        afterBodyStates = deepcopy(self.machineStates)
        self.machineStates = afterBodyStates + originalStates
        #post = ctx.for_rest_statement()
        return ("for", stat)