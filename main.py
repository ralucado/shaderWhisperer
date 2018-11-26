import sys
from antlr4 import *
from build.classes.GLSLLexer import GLSLLexer
from build.classes.GLSLParser import GLSLParser
from myGLSLListener import *


def calls(name, input):
    lexer = GLSLLexer(input)
    stream = CommonTokenStream(lexer)
    parser = GLSLParser(stream)
    tree = parser.prog()
    printer = callGLSLListener(name)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)    

def main():
    FS = FileStream("Shaders/test.frag")
    #VS = FileStream("Shaders/test.vert")
    calls("fract", FS)
    FS = FileStream("Shaders/test.frag")
    calls("isYellowStrip", FS)
 
if __name__ == '__main__':
    main()