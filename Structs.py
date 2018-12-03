class srcPoint():
    def __init__(self, l, c):
        self.line = l
        self.col = c 
        
    def __str__(self):
        return repr(self.line) + ":" + repr(self.col)
    
    def __repr__(self):
        return str(self)

class srcInterval():   
    def __init__(self,x,y):
        self.start = x
        self.end = y
    
    def __str__(self):
        return str(self.start)+".."+str(self.end)
    #TODO: def len?