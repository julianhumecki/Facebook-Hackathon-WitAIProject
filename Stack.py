class Stack:
    def __init__(self):
        self.stack = list()
    #add
    def push(self, pair):
        self.stack.append(pair) 
    #remove
    def pop(self):
        removedPair = self.stack[-1] 
        self.stack = self.stack[:-1]
        return removedPair
    
    def isEmpty(self):
        return len(self.stack) == 0
    #return latest addition
    def peek(self):
        if self.isEmpty(): return None
        return self.stack[-1]

class TaskList:
    def __init__(self):
        self.taskList = list() 
    def addToList(self, task):
        self.taskList.append(task)      
    def remove(self, task):
        self.taskList.remove(task)  
