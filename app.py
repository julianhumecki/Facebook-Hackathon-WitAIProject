import os

from flask import Flask, render_template, request, session, redirect
from flask_session import Session

from Stack import Stack, TaskList
from MessageHistory import MessagePair, numericMonthToName, Task
from datetime import datetime
from pytz import timezone
from Service.WitConnector import *
from Scraping.scraping import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from calendar import weekday
import random

app = Flask(__name__)

engine = create_engine(os.getenv("POSTGRES_SERVER_CREDENTIALS"))
db = scoped_session(sessionmaker(bind=engine))

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



tz = timezone('Canada/Eastern')

#connect to wit service
wc = init_wit()

allTasks = TaskList()
@app.route("/", methods=["GET", "POST"])
def index():
    #already logged in shouldnt have access to log in form
    if not isLoggedIn():
        return redirect("/login", code=302)
    #check if empty
    if session.get("username") == None or session.get("tasklist") == None:
        config_sessions()

    if request.method == "POST":
    #deal with new task
        taskName = str(request.form.get("task-name")) 
        dueDate = str(request.form.get("dueDate"))
        description = str(request.form.get("quick-describe"))
        timeDue = str(request.form.get("timeDue")) 
        location = str(request.form.get("location"))
        #add task to database
        taskAdded = db.execute("INSERT INTO tasks (taskname, duedate, description, timedue, location) VALUES (:taskname, :duedate, :description, :timedue, :location)",
                {"taskname":taskName, "duedate": dueDate, "description":description, "timedue":timeDue, "location":location})
        #save the addition
        db.commit()
        #select task list from user
        tasksLinkingToTable = db.execute("SELECT tasklist FROM users WHERE email = :email", {"email":session["username"]}).fetchone()[0]
        length = 0
        if not tasksLinkingToTable is None:
            length = len(tasksLinkingToTable)

        task_list = db.execute("SELECT id FROM tasks WHERE taskname = :taskname AND duedate = :duedate AND description = :description AND timedue = :timedue AND location = :location ", {"taskname":taskName, "duedate": dueDate, "description":description, "timedue":timeDue, "location":location}).fetchone()
        #extract the id
        task_list_id = int(task_list[0])
        length += 1
        #add to list in users
        db.execute("UPDATE users SET tasklist[:index] = :task_list_id WHERE email = :email",{"index":length, "task_list_id":task_list_id, "email":session["username"]})
        #save the changes
        db.commit()
        fillTaskList()

        
        
    return render_template("message.html", signed_in=session["username"], navbar=session["welcome_message"])


#create a stack to store messages
messageHistory = Stack()


userName = "Name" 
witName = "WitAI"
@app.route("/chat", methods=["GET", "POST"])
def chat():
    #already logged in shouldnt have access to log in form
    if not isLoggedIn():
        return redirect("/login", code=302)

    if session.get("username") == None or session.get("messaginghistory") == None:
        config_sessions()

    messageList = list()
    if request.method == "POST":
        #deal with messages
        #get user query(message)
        userQuery = request.form.get("user-message")
        #messageHistory.push(MessagePair(userName, userQuery, dayTime))
        
        #get computer query
        witResponse = wc.message(userQuery)

        currentDayAndTime = datetime.now(tz)
        #Get info
        witAI_info = extract(witResponse)
        

        time = str(currentDayAndTime.hour) + ":" + str(currentDayAndTime.minute) + ":" + str(currentDayAndTime.second)
        day = currentDayAndTime.day
        month = numericMonthToName[currentDayAndTime.month]
        year = currentDayAndTime.year
        sender = "User"

        #gets top 5 links if uncertain
        if(witAI_info[2] < 0.70 or witAI_info[1] == ""):
            print("results")
            witResponse = getSearchResults(userQuery)
            linkInContent = True
        else:
            if(witAI_info[0] == "show_schedule"):
                return redirect("/calendar", code=302)
            if(witAI_info[1] == "state:very_negative" or witAI_info[1] == "state:negative" or witAI_info[1] == "state:neutral" or witAI_info[1] == "state:positive" or witAI_info[1] == "state:very_positive"):
                witResponse = extractRelevantInfo(witAI_info)
                linkInContent = False
            else:
                witResponse = getSearchResults(userQuery)
                linkInContent = True
        
        print(witResponse)
        input("wait...")
        #insert into the database
        userAdded = db.execute("INSERT INTO messagings (day, month, year, timesent, messagecontent, sender, haslinkincontent) VALUES (:day, :month, :year, :timesent, :messagecontent, :sender, :haslinkincontent)",
                {"day":day, "month": month, "year":year, "timesent":time, "messagecontent":[userQuery], "sender":sender, "haslinkincontent":False})
        witAdded = db.execute("INSERT INTO messagings (day, month, year, timesent, messagecontent, sender, haslinkincontent) VALUES (:day, :month, :year, :timesent, :messagecontent, :sender, :haslinkincontent)",
                {"day":day, "month": month, "year": year, "timesent":time, "messagecontent":witResponse, "sender":witName, "haslinkincontent":linkInContent})
        db.commit()
    
        messagesLinkingToTable = db.execute("SELECT messagehistory FROM users WHERE email = :email", {"email":session["username"]}).fetchone()[0]
        length = 0
        if not messagesLinkingToTable is None:
            length = len(messagesLinkingToTable)


        #messages = db.execute("SELECT messagehistory FROM users WHERE email = :email", {"email":session["username"]}).fetchone();
        #update entries in message history
        message_one_id = db.execute("SELECT id FROM messagings WHERE day = :day AND month = :month AND year = :year AND timesent = :timesent AND sender = :sender ", {"day":day, "month":month, "year":year, "timesent":time, "sender":sender}).fetchone()
        message_two_id = db.execute("SELECT id FROM messagings WHERE day = :day AND month = :month AND year = :year AND timesent = :timesent AND sender = :sender ", {"day":day, "month":month, "year":year, "timesent":time, "sender":witName}).fetchone()
        #grab first id
        message_one_id = int(message_one_id[0])
        message_two_id = int(message_two_id[0])
        length += 1
        db.execute("UPDATE users SET messagehistory[:lowerIndex] = :message_one WHERE email = :email",{"lowerIndex":length, "message_one":message_one_id, "email":session["username"]})
        length += 1
        db.execute("UPDATE users SET messagehistory[:upperIndex] = :message_two WHERE email = :email",{"upperIndex":length, "message_two":message_two_id, "email":session["username"]})
        db.commit()

       
        fillMessageHistory()
        
        
    return render_template("chat.html", messageHistory=session["messaginghistory"], witName=witName, userName=userName, signed_in=session["username"], navbar=session["welcome_message"])

    
@app.route("/calendar")
def calendar():
    #already logged in shouldnt have access to log in form
    if not isLoggedIn():
        return redirect("/login", code=302)

    if session.get("username") == None or session.get("tasklist") == None:
        config_sessions()
    return render_template("calendar.html", allTasks=allTasks, signed_in=session["username"], navbar=session["welcome_message"], taskList=session["tasklist"])


@app.route("/login", methods=["GET", "POST"])
def login():
    #already logged in shouldnt have access to log in form
    if isLoggedIn():
        return redirect("/", code=302)
    #check if anyone logged in
    if session.get("username") == None:
        config_sessions()
    if request.method == "POST":
        username =  str(request.form.get("username"))
        password = str(request.form.get("password"))
        result = db.execute("SELECT firstname, email, password FROM users WHERE email = :username", {"username":username}).fetchone()
        if result is None:
            return render_template("login.html", error="username dne")
        elif not result.password == password:
            return render_template("login.html", error="invalid password")
        else:
            session["username"] = result.email
            session["firstname"] = result.firstname
            session["welcome_message"] = "Signed in as: " + session["firstname"] 
            fillMessageHistory()
            fillTaskList()
            return redirect("/", code=302)

    return render_template("login.html", signed_in=session["username"], navbar=session["welcome_message"])

@app.route("/register", methods=["GET","POST"])
def register():
    #already logged in shouldnt have access to log in form
    if isLoggedIn():
        return redirect("/", code=302)

    if session.get("username") == None:
        config_sessions()

    #--------------------------------------------------------

    register = ""
    if request.method == "POST":
        firstName = str(request.form.get("firstName"))
        lastName = str(request.form.get("lastName"))
        email = str(request.form.get("email"))
        password = str(request.form.get("password"))  
        messageHistory = []
        #check for preexisiting that's been registered
        existingInfo = db.execute("SELECT email FROM users WHERE email = :email", {"email":email}).fetchone()
        if existingInfo == None:
            db.execute("INSERT INTO users (messagehistory, firstname, lastname, email, password) VALUES (:messagehistory, :firstname, :lastname, :email, :password)",
                {"messagehistory":messageHistory,"firstname": firstName, "lastname":lastName, "email":email, "password":password})

            db.commit()
            register = "Success"
        else:
            register = "Email is already registered"
            return render_template("register.html", register=register, signed_in=session["username"], navbar=session["welcome_message"])
        

    return render_template("register.html", register=register, signed_in=session["username"], navbar=session["welcome_message"])

@app.route("/logout")
def logout():
    config_sessions()
    return redirect("/login", code=302)

#extra functions

def extract(json):

    ent = json['entities']   
    role = str()
    important = str()
    confidence = 0
    if (len(json['intents']) > 0):
        role = json['intents'][0]['name']
        important = str()
        confidence = json['intents'][0]['confidence']
        
        length = 0
        for feeling in ent:
            length +=1
        if(length > 0):
            if role == "show_schedule":
                important =  ent['day:day'][0]['value']
            elif role == "feeling":
                for feeling in ent:
                    important = feeling
                    break

    
    return [role, important, confidence]


def config_sessions():
    session["username"] = None
    session["firstname"] = None
    session["welcome_message"] = None
    session["messaginghistory"] = []
    session["tasklist"] = []

def isLoggedIn():
    if session.get("username") is None:
        return False
    return True

def fillMessageHistory():
#loop over all message ids
    messageList = list()
    allMessages = db.execute("SELECT messagehistory FROM users WHERE email = :email", {"email":session["username"]}).fetchone()[0]
    if not allMessages is None:
        for message_id in allMessages:
            #get message contents from messages sent
            value = db.execute("SELECT day,month,year,timesent, messagecontent,sender,haslinkincontent FROM messagings WHERE id = :id", {"id":message_id}).fetchone()
            
            messageList.append((value.day, value.month, value.year, value.timesent, value.messagecontent, value.sender, value.haslinkincontent))
    #phrase = 'I am not sure what\'s going on ' + answer[1]
    #messageHistory.push(MessagePair(witName, phrase, dayTime))
    #witResponse = getWitResponse()
    #messageHistory.push(MessagePair(witName, witResponse, dayTime))
    #------------------------------------------------------------------
    session["messaginghistory"] = messageList.copy()
    return

def fillTaskList():
    tasks = list()
    allTasks = db.execute("SELECT tasklist FROM users WHERE email = :email", {"email":session["username"]}).fetchone()[0]
    if not allTasks is None:
        for task_id in allTasks:
            value = db.execute("SELECT taskname, duedate, description, timedue, location FROM tasks WHERE id = :id", {"id":task_id}).fetchone()
            insertion = (value.taskname, value.duedate, value.description, value.timedue, value.location)
            insertToTasks(tasks, insertion)
    
    session["tasklist"] = tasks.copy()
    return

#insert in a chronological way
def insertToTasks(tasks, insertion):
    #sorting by the 2nd index of description
    if len(tasks) == 0:
        tasks.append(insertion)
        return
    count = 0
    taskCopy = tasks.copy()
    for task in taskCopy:
        if (insertion[1] < task[1]):
            tasks.insert(count, insertion)
            return
        #if same day, check which time is earlier
        elif (insertion[1] == task[1]):
            if(insertion[3] < task[3]):
                tasks.insert(count, insertion)
                return
            else:
                while(insertion[3] >= task[3] and insertion[1]== task[1]):
                    count += 1    
                    if(count < len(tasks)):
                        task = tasks[count]
                    else:
                        
                        tasks.append(insertion)
                        return
                tasks.insert(count, insertion)

            return
        #last element check
        elif (count == (len(tasks) - 1) and insertion[1] > task[1]):
            tasks.append(insertion)
            return
        #last elem, same day
        elif (count == (len(tasks) - 1) and insertion[1] == task[1]):
            if(insertion[3] < task[3]):
                tasks.insert(count, insertion)
                return
            else:
                tasks.append(insertion)

        count +=1
    return 

def extractRelevantInfo(witAI_info):
    if witAI_info == "show_schedule":
        return []
    else:
        return [getAppropriateResponse(witAI_info[1].split(":")[1])]

def getAppropriateResponse(feeling):
    if feeling == "positive" or feeling == "very_positive":
        return postiveResponse()
    elif feeling == "negative" or feeling == "very_negative":
        return inspiration()
    else:
        return neutral()

def postiveResponse():
    positive = ["Wowwwww", "That's dope", "Legend", "Killing the game", "Atta legend", "Keep at it", "You're golden", "That's how it be when you're awesome"]
    return random.choice(positive)
def inspiration():
    inspiration = ["You can do it", "Dont give up, you're very strong", "Keep pushing!", "You will get through this!", "You will succeed!", "Trust yourself!", "You're amazing! Remember this!", "Keep trying!"]
    return random.choice(inspiration)
def neutral():
    neutral = ["Life is good, take a moment to appreciate it", "Dont dwell on the negative!", "Youre a Legend BE HAPPY!", "Take time to relax and enjoy yourself", "You're beautiful", "Life's too short to be neutral :)", ":) SMILE :)"]
    return random.choice(neutral)

#if this app is run
if __name__ == "__main__":
    app.run()
