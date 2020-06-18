from flask import Flask, render_template, request, session
from Stack import Stack
from MessageHistory import MessagePair, numericMonthToName
from datetime import datetime
from pytz import timezone
from Service.WitConnector import *

app = Flask(__name__)
app.debug = True

tz = timezone('Canada/Eastern')

#connect to wit service
wc = init_wit()

@app.route("/")
def index():
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

        phrase = 'I am not sure what\'s going on ' + answer[1]

        messageHistory.push(MessagePair(witName, phrase, dayTime))
        
    return render_template("chat.html", messageHistory=messageHistory, witName=witName, userName=userName)

    
@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/schoolsite")
def school_site():
    return render_template("schoolSite.html")

def extract(json):

    ent = json['entities']   
    role = ent['day:day'][0]['role']
    day =  ent['day:day'][0]['value']
    return [role, day]


    