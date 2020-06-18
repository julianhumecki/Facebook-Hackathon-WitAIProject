from Stack import Stack

class MessagePair:
    def __init__(self, byWhom, message, dayAndTime):
        self.messagePair = (byWhom, message)
        self.dayTime = dayAndTime
#used for tasks
class Task:
    def __init__(self, taskName, description, dueDate):
        self.taskName = taskName
        self.description = description 
        self.dueDate = dueDate
    def updateFields(self, taskName=None, description=None, dueDate=None):
        if not taskName == None:
            self.taskName = taskName
        if not description == None:
            self.description = description
        if not dueDate == None:
            self.dueDate = dueDate 

        
numericMonthToName = {
    1:"Jan",
    2:"Feb",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"Aug",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dec",
}

# task = Task("a","b","c") 
# task.updateFields(taskName="First One")
# print(task.taskName)
# print(task.dueDate)

    
