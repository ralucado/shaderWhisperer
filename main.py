from shaderWhisperer import shaderWhisperer

def main():
    sw = shaderWhisperer()
    sw.addSource("FS", "Shaders/test.frag")
    sw.addSource("VS", "Shaders/test.vert")
    
    if (len(sw.calls("normalize", "VS")) > 0):
        print("Aqui no cal normalitzar")
        
    if (len(sw.calls("mix", "VS")) < 2):
        print("No fa servir mix()")
    
    if(len(sw.sentences("for", "FS")) > 0):
        print("Usa bucle for")    
 
if __name__ == '__main__':
    main()