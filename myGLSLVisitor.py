from antlr4 import *
from GLSLParser import GLSLParser
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
    
class statementVisitor(ParseTreeVisitor):
    
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
        return ("{",self.visitChildren(ctx),"}")
    
    def visitDeclaration_statement(self, ctx:GLSLParser.Declaration_statementContext):
        return "declaration"
    
    def visitExpression(self, ctx:GLSLParser.ExpressionContext):
        return "expression"
    
    def visitAssignment_statement(self, ctx:GLSLParser.Assignment_statementContext):
        return "assignment"
    
    # Visit a parse tree produced by GLSLParser#selection_statement.
    def visitSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        cond = ctx.getChild(2).accept(self)
        rest = ctx.getChild(4).accept(self)
        return ("if",cond,rest)
    
    # Visit a parse tree produced by GLSLParser#selection_rest_statement.
    def visitSelection_rest_statement(self, ctx:GLSLParser.Selection_rest_statementContext):
        first = ctx.statement(0).accept(self)
        second = ctx.statement(1).accept(self)
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

  