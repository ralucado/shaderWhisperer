from antlr4 import *
from GLSLParser import GLSLParser
import logging
if __name__ is not None and "." in __name__:
    from .build.classes.GLSLVisitor import *
    from .Structs import *
else:
    from build.classes.GLSLVisitor  import *
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
    
    def __init__(self, variables):
        self._variables = variables
        logging.debug(variables)
    
    def aggregateResult(self, aggregate, nextResult):
        if nextResult is not None:
            return nextResult
        return aggregate
    
     # Visit a parse tree produced by GLSLParser#sign.
    def visitSign(self, ctx:GLSLParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#addsub.
    def visitAddsub(self, ctx:GLSLParser.AddsubContext):
        #print("------- addsub of",ctx.expression(0).getText(),ctx.ADDSUB_OP().getText(),ctx.expression(1).getText())
        left = ctx.expression(0).accept(self)
        right = ctx.expression(1).accept(self)
        return str(left)+ctx.ADDSUB_OP().getText()+str(right)
    
    # Visit a parse tree produced by GLSLParser#muldiv.
    def visitMuldiv(self, ctx:GLSLParser.MuldivContext):
        #print("-------- muldiv of",ctx.expression(0).getText(),ctx.MULDIV_OP().getText(),ctx.expression(1).getText())
        left = ctx.expression(0).accept(self)
        right = ctx.expression(1).accept(self)
        return str(left)+ctx.MULDIV_OP().getText()+str(right)
    
    def visitLeft_value_exp(self, ctx:GLSLParser.Left_value_expContext):
        if(ctx.array_struct_selection() is not None):
            if ctx.array_struct_selection().struct_specifier() is not None:
                st = ctx.array_struct_selection().struct_specifier()[-1].accept(self)
                if len(st) == 1:
                    return "constant"
                elif len(st) == 2:
                    return "wrong"
        if(ctx.left_value().IDENTIFIER() is not None):
            return ctx.left_value().IDENTIFIER().getText()
        if(ctx.left_value().function_call() is not None):
            return "function call"
        return self.visitChildren(ctx.left_value())
    
    # Visit a parse tree produced by GLSLParser#constant_expression.
    def visitConstant_expression(self, ctx:GLSLParser.Constant_expressionContext):
        return"constant"
    
    # Visit a parse tree produced by GLSLParser#basic_type_exp.
    def visitBasic_type_exp(self, ctx:GLSLParser.Basic_type_expContext):
        spaces = []
        for exp in ctx.expression():
            spaces.append(exp.accept(self))
        return str(spaces)


class statementVisitor(ParseTreeVisitor):
    def __init__(self):
        super().__init__()
        self._lastId = 0
        init = programState(0)
        self.machineStates = {0: init}
        self.vars = [] #temporal testing
        
    def _newState(self):
        s = self.machineStates[self._lastId]
        ns = s.increment()
        self._lastId = ns.getID()
        self.machineStates[self._lastId] = ns
        return ns

    
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
        c = ctx.getChildren()
        res = []
        for child in c:
            s = self._newState()
            res.append(child.accept(self))
        return ("{",res,"}")
    
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
                    nameString = id.left_value().IDENTIFIER().getSymbol().text
                    typeString = type.getChild(0).getSymbol().text
                    state = self.machineStates[self._lastId]
                    if(id.assignment_expression() is not None):
                        vis = expressionVisitor(self.machineStates[self._lastId].vars)
                        v=vis.visitChildren(id.assignment_expression())
                        logging.debug(v)
                    state.vars[nameString] = (typeString, "object")
                    self.machineStates[self._lastId] = state
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
            expression = ""
            if ctx.assignment_expression() is not None:
                expression = ctx.assignment_expression().expression()
                #_overrideVar(targetVar, expression)
                vis = expressionVisitor(self.machineStates[self._lastId].vars)
                v = vis.visitChildren(ctx.assignment_expression())
                logging.debug(v)
            else:
                expression = ctx.arithmetic_assignment_expression().expression()
            return targetVar + " = " + expression.getText()
        return "assignment"
    
    # Visit a parse tree produced by GLSLParser#selection_statement.
    def visitSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        cond = ctx.getChild(2).accept(self)
        rest = ctx.getChild(4).accept(self)
        return ("if",cond,rest)
    
    # Visit a parse tree produced by GLSLParser#selection_rest_statement.
    def visitSelection_rest_statement(self, ctx:GLSLParser.Selection_rest_statementContext):
        first = ctx.statement(0).accept(self)
        second = ctx.statement(1)
        if(second is None):
            return [first]
        second = second.accept(self)
        return [first,second]
    
    
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
        cond = ctx.getChild(2).accept(self)
        stat = ctx.getChild(4).accept(self)
        return ("while", cond, stat)
            
    # Visit a parse tree produced by GLSLParser#do.
    def visitDo(self, ctx:GLSLParser.DoContext):
        stat = ctx.getChild(1).accept(self)
        cond = ctx.getChild(4).accept(self)
        return ("do", stat, "while", cond)

            
    # Visit a parse tree produced by GLSLParser#for.
    def visitFor(self, ctx:GLSLParser.ForContext):
        init = ctx.getChild(2).accept(self)
        cond = ctx.getChild(3).accept(self)
        post = ctx.getChild(4).accept(self)
        stat = ctx.getChild(6).accept(self)
    
        return ("for", init, cond, post, stat)
    
    def visitFor_init_statement(self, ctx:GLSLParser.For_init_statementContext):
        return ("init st.", self.visitChildren(ctx))
    
    
    def visitFor_cond_statement(self, ctx:GLSLParser.For_cond_statementContext):
        return ("condition", self.visitChildren(ctx))

    def visitFor_rest_statement(self, ctx:GLSLParser.For_rest_statementContext):
        return ("rest", self.visitChildren(ctx))
            
   # Visit a parse tree produced by GLSLParser#continue.
    def visitContinue(self, ctx:GLSLParser.ContinueContext):
        return  "cont."
    
    # Visit a parse tree produced by GLSLParser#break.
    def visitBreak(self, ctx:GLSLParser.BreakContext):
        return "break"

    # Visit a parse tree produced by GLSLParser#return.
    def visitReturn(self, ctx:GLSLParser.ReturnContext):
        return "return"
    
    
        # Visit a parse tree produced by GLSLParser#shift.
    def visitShift(self, ctx:GLSLParser.ShiftContext):
        return "shift op expr"


    # Visit a parse tree produced by GLSLParser#cmp.
    def visitCmp(self, ctx:GLSLParser.CmpContext):
        return "cmp op expr"


    # Visit a parse tree produced by GLSLParser#sign.
    def visitSign(self, ctx:GLSLParser.SignContext):
        return "sign op expr"


    # Visit a parse tree produced by GLSLParser#addsub.
    def visitAddsub(self, ctx:GLSLParser.AddsubContext):
        return "add or sub expr"


    # Visit a parse tree produced by GLSLParser#unary.
    def visitUnary(self, ctx:GLSLParser.UnaryContext):
        return "unary op expr"


    # Visit a parse tree produced by GLSLParser#eq.
    def visitEq(self, ctx:GLSLParser.EqContext):
        return "equality expr"


    # Visit a parse tree produced by GLSLParser#preIncrement.
    def visitPreIncrement(self, ctx:GLSLParser.PreIncrementContext):
        return "pre incr expr"


    # Visit a parse tree produced by GLSLParser#muldiv.
    def visitMuldiv(self, ctx:GLSLParser.MuldivContext):
        return "mul or div expr"


    # Visit a parse tree produced by GLSLParser#bitwise.
    def visitBitwise(self, ctx:GLSLParser.BitwiseContext):
        return "bitwise operator expr"


    # Visit a parse tree produced by GLSLParser#postIncrement.
    def visitPostIncrement(self, ctx:GLSLParser.PostIncrementContext):
        return "post inrement expr"


    # Visit a parse tree produced by GLSLParser#logic.
    def visitLogic(self, ctx:GLSLParser.LogicContext):
        return "logical expr"


    # Visit a parse tree produced by GLSLParser#ternary.
    def visitTernary(self, ctx:GLSLParser.TernaryContext):
        return "ternary expr"


    # Visit a parse tree produced by GLSLParser#primary.
    def visitPrimary(self, ctx:GLSLParser.PrimaryContext):
        return "primary expr"

        # Visit a parse tree produced by GLSLParser#basic_type.
    def visitBasic_type(self, ctx:GLSLParser.Basic_typeContext):
        return ctx.getText()
  