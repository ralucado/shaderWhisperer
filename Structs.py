class srcPoint():
    def __init__(self, l=-1, c=-1):
        self.line = l
        self.col = c 
        
    def __str__(self):
        return repr(self.line) + ":" + repr(self.col)
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if(isinstance(other, srcPoint)):
            return (self.line == other.line and self.col == other.col)
        return False

class srcInterval():   
    def __init__(self,x,y):
        self.start = x
        self.end = y
    
    def __str__(self):
        return str(self.start)+".."+str(self.end)
    
    def __eq__(self, other):
        if(isinstance(other, srcInterval)):
            return (self.x == other.x and self.y == other.y)
        return False
    #TODO: def len?