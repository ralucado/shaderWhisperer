from shaderWhisperer import shaderWhisperer

#TODO: add testing class
def testSentences(sw):
    print("\n --- sentences testing\n")
    for s in ["switch", "case", "while", "do", "for", "if", "break", "continue", "return"]:
        print(s, "\t:", sw.sentences(s))
        
def testExpressions(sw):
    print("\n --- expression testing\n")
    sw.expressions("")
    
def testVisitor(sw):
    print("\n --- visitor testing\n")
    print(" -> ", sw.tryVisitor(""))
            
def testCalls(sw):
    print("\n --- call testing\n")
    print("isYellowStrip:", sw.calls("isYellowStrip"))
    print("fract:        ", sw.calls("fract"))
    print("normalize:    ", sw.calls("normalize"))
    print("vec3:    ", sw.calls("vec3"))

def testDecls(sw):
    print("\n --- decl testing\n")
    print("frontColor:   ", sw.declarations("frontColor")) #should be one
    print("i:            ", sw.declarations("i") )#should be many
    print("f:            ", sw.declarations("f") )#should be many
    
def testAssig(sw):
    print("\n --- assig testing\n")
    print("frontColor:   ", sw.assignments("frontColor"))
    print("i:   ", sw.assignments("i"))
    
def testUses(sw):
    print("\n --- uses testing\n")
    print("frontColor:   ", sw.uses("frontColor"))
    print("speed:   ", sw.uses("speed"))
    print("vertex:   ", sw.uses("vertex"))
    print("i:   ", sw.uses("i"))
    print("normalMatrix:   ", sw.uses("normalMatrix"))
    
def testIns(sw):
    print("\n --- inVars testing\n")
    print("in \t:", sw.inVars())
    
def testOuts(sw):
    print("\n --- outVars testing\n")
    print("out \t:", sw.outVars())
    
def main():
    fs = shaderWhisperer(["Shaders/test.frag"])
    vs = shaderWhisperer(["Shaders/test.vert"])
    vsfs = shaderWhisperer(["Shaders/test.vert", "Shaders/test.frag"])

    testSentences(vsfs)
    testCalls(vsfs)
    testDecls(vsfs)
    testAssig(vsfs)
    testUses(vsfs)
    testIns(vsfs)
    testOuts(vsfs)
    #testExpressions(vsfs)
    #testVisitor(sw)
    
if __name__ == '__main__':
    main()