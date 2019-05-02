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
            return (self.start == other.start and self.end == other.end)
        return False
    #TODO: def len?
    
class programState():
    def __init__(self, id):
        self._id = id
        self.vars = {} #dictionary of variables with (type, coordSpace) as values
        self._goes = [] #list of tuples (id,condition) of accessible states and their respective transition conditions
        self._from = [] #list of tuples (id,condition) of parent states that transition into the current state
    
    def getID(self):
        return self._id
    
    def addChild(self, child, cond): #called by the main program
        self._goes.append((child.getID(),cond))
        child.addParent(self, cond)
        
    def addParent(self, parent, cond): #called only by other nodes when they are appended this child
        self._from.append((parent.getID(),cond))
    
    def increment(self, id):
        s=programState(id)
        s.vars = self.vars.copy()
        self.addChild(s, "")
        return s
    
    def resetParents(self):
        self._from = []
        
    def resetChildren(self):
        self._goes = []

            