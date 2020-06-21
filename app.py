
#More stuff
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from Stack import Stack, TaskList
from MessageHistory import MessagePair, numericMonthToName, Task
from datetime import datetime
from pytz import timezone

#wit 
from Service.WitConnector import *
#outlook
from Service.MSGraphService import *


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
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

@app.route('/mscal')
def calendar_show():
    return render_template("json.html")

#show calendar events
@app.route('/caldata')
def data():    
    
    account = get_account()
    schedule = account.schedule()    
    calendar = schedule.get_calendar(calendar_name='Calendar')
    q = calendar.new_query('start').greater_equal(dt.datetime(2019, 5, 20))
    q.chain('and').on_attribute('end').less_equal(dt.datetime(2023, 5, 24))
    events = calendar.get_events(query=q, include_recurring=True)  # include_recurring=True will include repeated events on the result set.    

    return render_template('events.html', events=events)

#authentication part1
@app.route('/stepone')
def auth_step_one():    
    return redirect(auth_init())

#authentication part2
@app.route('/steptwo')
def auth_step_two_callback():       

   if auth_end(request.url, request.args.get('state')):
    return redirect('/caldata')
   else:
    return render_template('message.html')


app.run(port=9090, ssl_context=('cert.pem', 'key.pem')) 

