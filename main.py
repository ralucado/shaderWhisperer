from shaderWhisperer import shaderWhisperer

#TODO: add testing class
def testSentences(sw):
    for s in ["switch", "case", "while", "do", "for", "if", "break", "continue", "return"]:
        print(s, ":", sw.sentences(s, "VS"))
            
def testCalls(sw):
    print("FS -- isYellowStrip:", sw.calls("isYellowStrip", "FS"))
    print("FS -- fract:", sw.calls("fract", "FS"))
    print("VS -- normalize:", sw.calls("normalize", "VS"))
    
    
def main():
    sw = shaderWhisperer()
    sw.addSource("FS", "Shaders/test.frag")
    sw.addSource("VS", "Shaders/test.vert")
    testSentences(sw)
    
if __name__ == '__main__':
    main()