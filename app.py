import os

from flask import Flask, render_template, request, session, redirect
from flask_session import Session

from Stack import Stack, TaskList
from MessageHistory import MessagePair, numericMonthToName, Task
from datetime import datetime
from pytz import timezone
from Service.WitConnector import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

    if session.get("username") == None:
        config_sessions()
    #if request.method == "POST":
    #deal with new task
        # taskName = request.form.get("task-name") 
        # dueDate = request.form.get("dueDate")
        # description = request.form.get("quick-describe")
        # timeDue = request.form.get("timeDue") 
        # location = request.form.get("location")
        # dueDateList = str(dueDate).split("-")
        # dueDate = (numericMonthToName[int(dueDateList[1])], int(dueDateList[2]))
        
        # # input("Heyyy ")
        # #add to our list of tasks
        # allTasks.addToList(Task(taskName, description, timeDue, location, dueDate))
        #print(len(allTasks.taskList))
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
        answer = ['', 'stupid']

        try: 
            answer = extract(witResponse)        
        except:
            pass

        currentDayAndTime = datetime.now(tz)

        time = str(currentDayAndTime.hour) + ":" + str(currentDayAndTime.minute)
        day = currentDayAndTime.day
        month = numericMonthToName[currentDayAndTime.month]
        year = currentDayAndTime.year
        sender = "User"


        #insert into the database
        userAdded = db.execute("INSERT INTO messagings (day, month, year, timesent, messagecontent, sender) VALUES (:day, :month, :year, :timesent, :messagecontent, :sender)",
                {"day":day, "month": month, "year":year, "timesent":time, "messagecontent":userQuery, "sender":sender})
        witAdded = db.execute("INSERT INTO messagings (day, month, year, timesent, messagecontent, sender) VALUES (:day, :month, :year, :timesent, :messagecontent, :sender)",
                {"day":day, "month": month, "year": year, "timesent":time, "messagecontent":str(witResponse), "sender":witName})
        db.commit()
    
        messagesLinkingToTable = db.execute("SELECT messagehistory FROM users WHERE email = :email", {"email":session["username"]}).fetchone()[0]
        length = 0
        if not messagesLinkingToTable is None:
            length = len(messagesLinkingToTable)

        #messages = db.execute("SELECT messagehistory FROM users WHERE email = :email", {"email":session["username"]}).fetchone();
        #update entries in message history
        message_one_id = db.execute("SELECT id FROM messagings WHERE day = :day AND month = :month AND year = :year AND messagecontent = :messagecontent", {"day":day, "month":month, "year":year, "messagecontent":userQuery}).fetchone()
        message_two_id = db.execute("SELECT id FROM messagings WHERE day = :day AND month = :month AND year = :year AND messagecontent = :messagecontent", {"day":day, "month":month, "year":year, "messagecontent":str(witResponse)}).fetchone()
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

    if session.get("username") == None:
        config_sessions()
    return render_template("calendar.html", allTasks=allTasks, signed_in=session["username"], navbar=session["welcome_message"])

@app.route("/schoolsite")
def school_site():
    #already logged in shouldnt have access to log in form
    if not isLoggedIn():
        return redirect("/login", code=302)

    if session.get("username") == None:
        config_sessions()
    return render_template("schoolSite.html", signed_in=session["username"], navbar=session["welcome_message"])

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
    role = ent['day:day'][0]['role']
    day =  ent['day:day'][0]['value']
    return [role, day]


def config_sessions():
    session["username"] = None
    session["firstname"] = None
    session["welcome_message"] = None
    session["messaginghistory"] = []

def isLoggedIn():
    if session.get("username") is None:
        return False
    return True
def fillMessageHistory():
#loop over all message ids
    messageList = list()
    allMessages = db.execute("SELECT messagehistory FROM users WHERE email = :email", {"email":session["username"]}).fetchone()[0]
    #print(allMessages)
    for message_id in allMessages:
        #get message contents from messages sent
        value = db.execute("SELECT day,month,year,timesent, messagecontent,sender FROM messagings WHERE id = :id", {"id":message_id}).fetchone()
        #print(value)
        messageList.append((value.day, value.month, value.year, value.timesent, value.messagecontent, value.sender))
    #phrase = 'I am not sure what\'s going on ' + answer[1]
    #messageHistory.push(MessagePair(witName, phrase, dayTime))
    #witResponse = getWitResponse()
    #messageHistory.push(MessagePair(witName, witResponse, dayTime))
    #------------------------------------------------------------------
    session["messaginghistory"] = messageList.copy()
    return