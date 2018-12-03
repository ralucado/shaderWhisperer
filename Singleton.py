class Result:
    
    class __Result:
        
        def __init__(self):
            self.val = []
            
        def __str__(self):
            return repr(self) + repr(self.val)
        
        
    instance = None
    
    def __init__(self):
        if not Result.instance:
            Result.instance = Result.__Result()
            
    def reset(self):
        if not Result.instance:
            Result.instance = Result.__Result()
        else:
            Result.instance.val = []
    
    def addValue(self, arg):
        if not Result.instance:
            Result.instance = Result.__Result()
        Result.instance.val.append(arg)
    
    def getValue(self):
        if not Result.instance:
            return []
        else:
            r = Result.instance.val
            Result.instance.val = []
            return r
        
            
    def __getattr__(self, name):
        return getattr(self.instance, name)