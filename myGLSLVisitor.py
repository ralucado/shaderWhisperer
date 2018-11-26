# Generated from GLSL.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .build.classes.GLSLVisitor import *
else:
    from build.classes.GLSLVisitor import *

# This class defines a complete generic visitor for a parse tree produced by GLSLParser.

class GLSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GLSLParser#prog.
    def visitProg(self, ctx:GLSLParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#preprocessor.
    def visitPreprocessor(self, ctx:GLSLParser.PreprocessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#version_pre.
    def visitVersion_pre(self, ctx:GLSLParser.Version_preContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#type_qualifier.
    def visitType_qualifier(self, ctx:GLSLParser.Type_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#layout_qualifier.
    def visitLayout_qualifier(self, ctx:GLSLParser.Layout_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#layout_qualifier_id.
    def visitLayout_qualifier_id(self, ctx:GLSLParser.Layout_qualifier_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#storage_qualifier.
    def visitStorage_qualifier(self, ctx:GLSLParser.Storage_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#precision_qualifier.
    def visitPrecision_qualifier(self, ctx:GLSLParser.Precision_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#interpolation_qualifier.
    def visitInterpolation_qualifier(self, ctx:GLSLParser.Interpolation_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#invariant_qualifier.
    def visitInvariant_qualifier(self, ctx:GLSLParser.Invariant_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#precise_qualifier.
    def visitPrecise_qualifier(self, ctx:GLSLParser.Precise_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#integer.
    def visitInteger(self, ctx:GLSLParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#float_num.
    def visitFloat_num(self, ctx:GLSLParser.Float_numContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#bool_num.
    def visitBool_num(self, ctx:GLSLParser.Bool_numContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#type_specifier.
    def visitType_specifier(self, ctx:GLSLParser.Type_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#type_specifier_nonarray.
    def visitType_specifier_nonarray(self, ctx:GLSLParser.Type_specifier_nonarrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#array_specifier.
    def visitArray_specifier(self, ctx:GLSLParser.Array_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#struct_specifier.
    def visitStruct_specifier(self, ctx:GLSLParser.Struct_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#basic_type.
    def visitBasic_type(self, ctx:GLSLParser.Basic_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#void_type.
    def visitVoid_type(self, ctx:GLSLParser.Void_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#scala_type.
    def visitScala_type(self, ctx:GLSLParser.Scala_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#vector_type.
    def visitVector_type(self, ctx:GLSLParser.Vector_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#matrix_type.
    def visitMatrix_type(self, ctx:GLSLParser.Matrix_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#opaque_type.
    def visitOpaque_type(self, ctx:GLSLParser.Opaque_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#float_opaque_type.
    def visitFloat_opaque_type(self, ctx:GLSLParser.Float_opaque_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#int_opaque_type.
    def visitInt_opaque_type(self, ctx:GLSLParser.Int_opaque_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#u_int_opaque_type.
    def visitU_int_opaque_type(self, ctx:GLSLParser.U_int_opaque_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#expression.
    def visitExpression(self, ctx:GLSLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#primary_expression.
    def visitPrimary_expression(self, ctx:GLSLParser.Primary_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#constant_expression.
    def visitConstant_expression(self, ctx:GLSLParser.Constant_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#left_value.
    def visitLeft_value(self, ctx:GLSLParser.Left_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#array_struct_selection.
    def visitArray_struct_selection(self, ctx:GLSLParser.Array_struct_selectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#assignment_expression.
    def visitAssignment_expression(self, ctx:GLSLParser.Assignment_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#arithmetic_assignment_expression.
    def visitArithmetic_assignment_expression(self, ctx:GLSLParser.Arithmetic_assignment_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#function_definition.
    def visitFunction_definition(self, ctx:GLSLParser.Function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#function_declaration.
    def visitFunction_declaration(self, ctx:GLSLParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#function_call.
    def visitFunction_call(self, ctx:GLSLParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#return_Type.
    def visitReturn_Type(self, ctx:GLSLParser.Return_TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#function_name.
    def visitFunction_name(self, ctx:GLSLParser.Function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#func_decl_member.
    def visitFunc_decl_member(self, ctx:GLSLParser.Func_decl_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#statement_list.
    def visitStatement_list(self, ctx:GLSLParser.Statement_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#statement.
    def visitStatement(self, ctx:GLSLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#simple_statement.
    def visitSimple_statement(self, ctx:GLSLParser.Simple_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#compoud_statement.
    def visitCompoud_statement(self, ctx:GLSLParser.Compoud_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#basic_statement.
    def visitBasic_statement(self, ctx:GLSLParser.Basic_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#declaration_statement.
    def visitDeclaration_statement(self, ctx:GLSLParser.Declaration_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#simple_declaration.
    def visitSimple_declaration(self, ctx:GLSLParser.Simple_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#simple_declarator.
    def visitSimple_declarator(self, ctx:GLSLParser.Simple_declaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#struct_declaration.
    def visitStruct_declaration(self, ctx:GLSLParser.Struct_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#function_definition_statement.
    def visitFunction_definition_statement(self, ctx:GLSLParser.Function_definition_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#assignment_statement.
    def visitAssignment_statement(self, ctx:GLSLParser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#expression_statement.
    def visitExpression_statement(self, ctx:GLSLParser.Expression_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#selection_statement.
    def visitSelection_statement(self, ctx:GLSLParser.Selection_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#selection_rest_statement.
    def visitSelection_rest_statement(self, ctx:GLSLParser.Selection_rest_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#switch_statement.
    def visitSwitch_statement(self, ctx:GLSLParser.Switch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#case_label.
    def visitCase_label(self, ctx:GLSLParser.Case_labelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#iteration_statement.
    def visitIteration_statement(self, ctx:GLSLParser.Iteration_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#for_init_statement.
    def visitFor_init_statement(self, ctx:GLSLParser.For_init_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#for_cond_statement.
    def visitFor_cond_statement(self, ctx:GLSLParser.For_cond_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#for_rest_statement.
    def visitFor_rest_statement(self, ctx:GLSLParser.For_rest_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GLSLParser#jump_statement.
    def visitJump_statement(self, ctx:GLSLParser.Jump_statementContext):
        return self.visitChildren(ctx)



del GLSLParser