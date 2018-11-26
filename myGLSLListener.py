# Generated from GLSL.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .classes.GLSLListener import *
else:
    from classes.GLSLListener  import *

class callGLSLListener(GLSLListener):
    
    def __init__(self, name):
            self.name = name
            
    # Enter a parse tree produced by GLSLParser#function_call.
    def enterFunction_call(self, ctx:GLSLParser.Function_callContext):
        token = ctx.function_name().IDENTIFIER().getSymbol();
        if (self.name == token.text):
            print("Found",self.name,"at", token.line, token.column)
        pass