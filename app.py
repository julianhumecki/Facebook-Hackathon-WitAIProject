from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("message.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")
    
@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/schoolsite")
def school_site():
    return render_template("schoolSite.html")
