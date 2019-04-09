from Setup import Setup
from shaderWhisperer import R, shaderWhisperer


#TODO: add testing class
def testSentences(sw):
    print("\n --- sentences testing\n")
    for s in ["switch", "case", "while", "do", "for", "if", "break", "continue", "return"]:
        print(s, "\t:", sw.sentences(s))
        
def testExpressions(sw):
    print("\n --- expression testing\n")
    sw.expressions("")
    
def coordSpaces(sw):
    print("\n --- visitor testing\n")
    print(sw.coordSpaces("P"))
    print(sw.coordSpaces("ndcP"))


    #R("wrong coords", "wrong" in sw.coordSpaces("V"))
    #R("wrong coords", "wrong" in sw.coordSpaces("LW"))
    
def testVisitorNoPrint(sw):
    print("\n --- visitor noprint testing\n")
    sw.tryVisitor("")
    
            
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
    
def testNumUses(sw):
    print("\n --- uses testing\n")
    print("frontColor:   ", sw.numUses("frontColor"))
    print("speed:   ", sw.numUses("speed"))
    print("vertex:   ", sw.numUses("vertex"))
    print("i:   ", sw.numUses("i"))
    print("normalMatrix:   ", sw.numUses("normalMatrix"))
    
def testInTypes(sw):
    print("\n --- inType testing\n")
    print("in \t:", sw.inTypes())
    
def testOutTypes(sw):
    print("\n --- outType testing\n")
    print("out \t:", sw.outTypes())
    
def testInNames(sw):
    print("\n --- inName testing\n")
    print("in \t:", sw.inNames())
    
def testOutNames(sw):
    print("\n --- outName testing\n")
    print("out \t:", sw.outNames())
    
def testParam(sw):
    print("\n --- param testing\n")
    print("vec4 \t:", sw.param("vec4"))
    print("vec4, 2\t:", sw.param("vec4", 2))
    print("mix, 2\t:", sw.param("mix", 2))
    print("normalize \t:", sw.param("normalize"))



    

def testFieldSelectors(sw):
    print("\n --- swizzle names testing\n")
    print("x \t:", sw.fieldSelectors("x"))
    print("z \t:", sw.fieldSelectors("z"))
    print("xz \t:", sw.fieldSelectors("xz"))
    print("w \t:", sw.fieldSelectors("w"))

def main():
    fs = shaderWhisperer(["Shaders/test.frag"])
    vs = shaderWhisperer(["Shaders/test.vert"])
    mag = shaderWhisperer(["Shaders/magnet.vert"])
    vsfs = shaderWhisperer(["Shaders/test2.vert", "Shaders/test.frag"])
    all = shaderWhisperer(["Shaders/allShaders/001.fs",  "Shaders/allShaders/006.fs",  "Shaders/allShaders/011.fs",  "Shaders/allShaders/016.fs",  "Shaders/allShaders/021.fs",  "Shaders/allShaders/026.fs",  "Shaders/allShaders/031.fs",  "Shaders/allShaders/036.fs",  "Shaders/allShaders/041.fs",  "Shaders/allShaders/046.fs",  "Shaders/allShaders/051.fs",  "Shaders/allShaders/057.vs", "Shaders/allShaders/001.vs",  "Shaders/allShaders/006.vs",  "Shaders/allShaders/011.vs",  "Shaders/allShaders/016.vs",  "Shaders/allShaders/021.vs",  "Shaders/allShaders/026.vs",  "Shaders/allShaders/031.vs",  "Shaders/allShaders/036.vs",  "Shaders/allShaders/041.vs",  "Shaders/allShaders/046.vs",  "Shaders/allShaders/054.vs",  "Shaders/allShaders/058.fs", "Shaders/allShaders/002.fs",  "Shaders/allShaders/007.fs",  "Shaders/allShaders/012.fs",  "Shaders/allShaders/017.fs",  "Shaders/allShaders/022.fs",  "Shaders/allShaders/027.fs",  "Shaders/allShaders/032.fs",  "Shaders/allShaders/037.fs",  "Shaders/allShaders/042.fs",  "Shaders/allShaders/047.fs",  "Shaders/allShaders/051.vs",  "Shaders/allShaders/055.fs", "Shaders/allShaders/002.vs",  "Shaders/allShaders/007.vs",  "Shaders/allShaders/012.vs",  "Shaders/allShaders/017.vs",  "Shaders/allShaders/022.vs",  "Shaders/allShaders/027.vs",  "Shaders/allShaders/032.vs",  "Shaders/allShaders/037.vs",  "Shaders/allShaders/042.vs",  "Shaders/allShaders/047.vs",  "Shaders/allShaders/052.fs",  "Shaders/allShaders/058.vs", "Shaders/allShaders/003.fs",  "Shaders/allShaders/008.fs",  "Shaders/allShaders/013.fs",  "Shaders/allShaders/018.fs",  "Shaders/allShaders/023.fs",  "Shaders/allShaders/028.fs",  "Shaders/allShaders/033.fs",  "Shaders/allShaders/038.fs",  "Shaders/allShaders/043.fs",  "Shaders/allShaders/048.fs",  "Shaders/allShaders/055.vs",  "Shaders/allShaders/059.fs", "Shaders/allShaders/003.vs",  "Shaders/allShaders/008.vs",  "Shaders/allShaders/013.vs",  "Shaders/allShaders/018.vs",  "Shaders/allShaders/023.vs",  "Shaders/allShaders/028.vs",  "Shaders/allShaders/033.vs",  "Shaders/allShaders/038.vs",  "Shaders/allShaders/043.vs",  "Shaders/allShaders/048.vs",  "Shaders/allShaders/052.vs",  "Shaders/allShaders/056.fs", "Shaders/allShaders/004.fs",  "Shaders/allShaders/009.fs",  "Shaders/allShaders/014.fs",  "Shaders/allShaders/019.fs",  "Shaders/allShaders/024.fs",  "Shaders/allShaders/029.fs",  "Shaders/allShaders/034.fs",  "Shaders/allShaders/039.fs",  "Shaders/allShaders/044.fs",  "Shaders/allShaders/049.fs",  "Shaders/allShaders/053.fs", "Shaders/allShaders/059.vs", "Shaders/allShaders/004.vs",  "Shaders/allShaders/009.vs",  "Shaders/allShaders/014.vs",  "Shaders/allShaders/019.vs",  "Shaders/allShaders/024.vs",  "Shaders/allShaders/029.vs",  "Shaders/allShaders/034.vs",  "Shaders/allShaders/039.vs",  "Shaders/allShaders/044.vs",  "Shaders/allShaders/049.vs", "Shaders/allShaders/056.vs",  "Shaders/allShaders/060.fs", "Shaders/allShaders/005.fs",  "Shaders/allShaders/010.fs",  "Shaders/allShaders/015.fs",  "Shaders/allShaders/020.fs",  "Shaders/allShaders/025.fs",  "Shaders/allShaders/030.fs",  "Shaders/allShaders/035.fs",  "Shaders/allShaders/040.fs",  "Shaders/allShaders/045.fs",  "Shaders/allShaders/050.fs",  "Shaders/allShaders/053.vs",  "Shaders/allShaders/057.fs", "Shaders/allShaders/005.vs",  "Shaders/allShaders/010.vs",  "Shaders/allShaders/015.vs",  "Shaders/allShaders/020.vs",  "Shaders/allShaders/025.vs",  "Shaders/allShaders/030.vs",  "Shaders/allShaders/035.vs",  "Shaders/allShaders/040.vs",  "Shaders/allShaders/045.vs",  "Shaders/allShaders/050.vs",  "Shaders/allShaders/054.fs", "Shaders/allShaders/060.vs"])
    errors = shaderWhisperer(["Shaders/allShaders/051.gs", "Shaders/allShaders/052.gs", "Shaders/allShaders/053.gs", "Shaders/allShaders/054.gs", "Shaders/allShaders/055.gs", "Shaders/allShaders/056.gs", "Shaders/allShaders/057.gs", "Shaders/allShaders/058.gs", "Shaders/allShaders/059.gs"])
    test =  shaderWhisperer(["Shaders/allShaders/032.vs"])
    par = shaderWhisperer(["Shaders/testParam.vs"])
    #testSentences(all)
    #testCalls(all)
    #testDecls(all)
    #testAssig(all)
    #testUses(all)
    #testNumUses(all)
    testParam(all)
    #testUses(all)
    #testNumUses(all)
    #testInTypes(all)
    #testInNames(all)
    #testOutTypes(all)
    #testOutNames(all)
    #test.setConstantCoordSpace("eye")
    #coordSpaces(all)
    #testVisitorNoPrint(all)
    testFieldSelectors(vs)
    
if __name__ == '__main__':
    main()
