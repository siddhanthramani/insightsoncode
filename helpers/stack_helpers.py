class InsightPointAutoStack(object):
    def __init__(self) -> None:
        self.unique_start = 0
        self.stacklist = []
    
    def push(self):
        self.unique_start += 1
        self.stacklist.append(str(self.unique_start))
        return str(self.unique_start)
        
    def pop(self):
        return self.stacklist.pop()