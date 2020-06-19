from flask import Flask, render_template, request, session
from Stack import Stack, TaskList
from MessageHistory import MessagePair, numericMonthToName, Task
from datetime import datetime
from pytz import timezone
from Service.WitConnector import *


app = Flask(__name__)
app.debug = True

tz = timezone('Canada/Eastern')

#connect to wit service
wc = init_wit()

allTasks = TaskList()
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
    #deal with new task
        taskName = request.form.get("task-name") 
        dueDate = request.form.get("dueDate")
        description = request.form.get("quick-describe")
        timeDue = request.form.get("timeDue") 
        location = request.form.get("location")
        print(timeDue)
        dueDateList = str(dueDate).split("-")
        dueDate = (numericMonthToName[int(dueDateList[1])], int(dueDateList[2]))
        print(dueDate)
        input("Heyyy ")
        #add to our list of tasks
        allTasks.addToList(Task(taskName, description, timeDue, location, dueDate))
        #print(len(allTasks.taskList))
    return render_template("message.html")


#create a stack to store messages
messageHistory = Stack()


userName = "Name" 
witName = "WitAI"
@app.route("/chat", methods=["GET", "POST"])
def chat():
    currentDayAndTime = datetime.now(tz)
    
    time = str(currentDayAndTime.hour) + ":" + str(currentDayAndTime.minute)
    day = numericMonthToName[currentDayAndTime.month] + " " + str(currentDayAndTime.day)
    dayTime = (time, day)
    if request.method == "POST":
        #deal with messages
        #get user query(message)
        userQuery = request.form.get("user-message")
        messageHistory.push(MessagePair(userName, userQuery, dayTime))
        
        #get computer query
        witResponse = wc.message(userQuery)
        answer = ['', 'stupid']

        try: 
            answer = extract(witResponse)        
        except:
            pass

        #phrase = 'I am not sure what\'s going on ' + answer[1]

        #messageHistory.push(MessagePair(witName, phrase, dayTime))
        #witResponse = getWitResponse()
        messageHistory.push(MessagePair(witName, witResponse, dayTime))
        #------------------------------------------------------------------
        
        
    return render_template("chat.html", messageHistory=messageHistory, witName=witName, userName=userName)

    
@app.route("/calendar")
def calendar():

    return render_template("calendar.html", allTasks=allTasks)

@app.route("/schoolsite")
def school_site():
    return render_template("schoolSite.html")

def extract(json):

    ent = json['entities']   
    role = ent['day:day'][0]['role']
    day =  ent['day:day'][0]['value']
    return [role, day]


