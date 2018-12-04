from shaderWhisperer import shaderWhisperer

#TODO: add testing class
def testSentences(sw):
    print("\n --- sentences testing\n")
    for s in ["switch", "case", "while", "do", "for", "if", "break", "cont.", "return"]:
        print(s, "\t:", sw.sentences(s, "VS"))
            
def testCalls(sw):
    print("\n --- call testing\n")
    print("FS -- isYellowStrip:", sw.calls("isYellowStrip", "FS"))
    print("FS -- fract:        ", sw.calls("fract", "FS"))
    print("VS -- normalize:    ", sw.calls("normalize", "VS"))

def testDecls(sw):
    print("\n --- decl testing\n")
    print("VS -- frontColor:   ", sw.declarations("frontColor", "VS")) #should be one
    print("VS -- i:            ", sw.declarations("i", "VS") )#should be many
    
def testAssig(sw):
    print("\n --- assig testing\n")
    print("VS -- frontColor:   ", sw.assignments("frontColor", "VS"))
    
def testUses(sw):
    print("\n --- uses testing\n")
    print("VS -- frontColor:   ", sw.uses("frontColor", "VS"))
    print("VS -- speed:   ", sw.uses("speed", "VS"))
    print("VS -- vertex:   ", sw.uses("vertex", "VS"))
    
def testIns(sw):
    print("\n --- inVars testing\n")
    print("VS --- in \t:", sw.inVars("VS"))
    
def testOuts(sw):
    print("\n --- outVars testing\n")
    print("VS --- out \t:", sw.outVars("VS"))
    
def main():
    sw = shaderWhisperer()
    sw.addSource("FS", "Shaders/test.frag")
    #sw.addSource("VS", "Shaders/noexiste")
    sw.addSource("VS", "Shaders/test.vert")
    testSentences(sw)
    testCalls(sw)
    testDecls(sw)
    testAssig(sw)
    testUses(sw)
    testIns(sw)
    testOuts(sw)
    
if __name__ == '__main__':
    main()