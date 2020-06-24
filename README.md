![bruh](https://wusa.ca/sites/ca.waterloo-undergraduate-student-association/files/uploads/images/logo-studentcare.png)
<h1><b>StudentCare</b></h1>
A bot for helping students manage their workload and relieve their stress.

<b><h2>Dependencies</h2></b>

1. Flask (pip install flask)
2. Wit (pip install wit)

<b><h2> Login/Registering </h2></b>
To make use of our services, you need to have registered/signed up for an account.

<b><h2> Student Care </h2></b>
Here you will have access to a form that adds events to your calendar (/calendar)
Once you submit it, it will add this event to your calendar. These added events are sorted based on date.

<b><h2> Chat </h2></b>
This is the main part of our app. Here you can type in any query, and you will receive a response. 
This will either be in the form of<span><b>5</b> </span>links or in the form of a text response. If you ask to see your schedule on a given day, our chat will interpret this and move you to the appropriate section (/calendar).
Our chat will also detect when you are feeling a certain way, and will respond appropriately

<b><h2>Utterances</h2></b>

Each utterance is related to an <i>intent</i>. An intent is realated to an <i>entity</i> that consists of a <i>role</i>. 
There are currently two intents; 'feeling' and 'show_schedule'.  

show_shcedule has the 'day' intent

'day' has only one role associated with it; 'day'. The 'day' role consists of the following values: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, today, tomorrow, and tonight.

feeling has the 'state' intent

'state' consists of multiple roles including 'negative', 'very_negative', 'positive', 'very_positive' and 'neutral'. Additionally, each of these roles can have a value assocaited to it; for ex stressed_out, happy, excited, anxious, etc.


The wit client's message() function returns a JSON object as follows. 

<b>Example 1</b>
```
{
   "text":"What's going on next Wednesday?", //message sent by the user
   "intents":[
      {
         "id":"902814443555620",
         "name":"show_schedule", //intent as described above
         "confidence":1
      }
   ],
   "entities":{
      "day:day":[
         {
            "id":"3240062442727830",
            "name":"day",
            "role":"day", //role as described above
            "start":21,
            "end":30,
            "body":"Wednesday", //role value
            "confidence":0.9737,
            "entities":[

            ],
            "value":"Wednesday", //role value
            "type":"value"
         }
      ]
   },
   "traits":{}
}

```

<b>Example 2</b>
```
{
   "text":"What's cooking tomorrow?", //message sent by the user
   "intents":[
      {
         "id":"902814443555620",
         "name":"show_schedule", //intent
         "confidence":1
      }
   ],
   "entities":{
      "day:day":[ //role
         {
            "id":"3240062442727830",
            "name":"day",
            "role":"day",
            "start":15,
            "end":23,
            "body":"tomorrow", //role value
            "confidence":0.9885,
            "entities":[

            ],
            "value":"tomorrow",
            "type":"value"
         }
      ]
   },
   "traits":{

   }
}

```
```
# Example 3. Sentiments and feelings

{
   "text":"I am feeling stressed out",
   "intents":[
      {
         "id":"4331082736909559",
         "name":"feeling",
         "confidence":0.9991
      }
   ],
   "entities":{
      "state:negative":[
         {
            "id":"2653812744877976",
            "name":"state",
            "role":"negative",
            "start":13,
            "end":25,
            "body":"stressed out",
            "confidence":0.9454,
            "entities":[

            ],
            "value":"stressed out",
            "type":"value"
         }
      ]
   },
   "traits":{
      "wit$sentiment":[
         {
            "id":"5ac2b50a-44e4-466e-9d49-bad6bd40092c",
            "value":"negative",
            "confidence":0.6804
         }
      ]
   }
}


```
```
# Ex. 4

{
   "text":"I am feeling down",
   "intents":[
      {
         "id":"4331082736909559",
         "name":"feeling",
         "confidence":0.9978
      }
   ],
   "entities":{
      "state:negative":[
         {
            "id":"2653812744877976",
            "name":"state",
            "role":"negative",
            "start":13,
            "end":17,
            "body":"down",
            "confidence":0.9321,
            "entities":[

            ],
            "value":"down",
            "type":"value"
         }
      ]
   },
   "traits":{

   }
}

```

```
Ex 5. 

{
   "text":"I am feeling excited",
   "intents":[
      {
         "id":"4331082736909559",
         "name":"feeling",
         "confidence":0.9995
      }
   ],
   "entities":{
      "state:very_positive":[
         {
            "id":"209556380088589",
            "name":"state",
            "role":"very_positive",
            "start":13,
            "end":20,
            "body":"excited",
            "confidence":0.8613,
            "entities":[

            ],
            "value":"excited",
            "type":"value"
         }
      ]
   },
   "traits":{ 
      "wit$sentiment":[
         {
            "id":"5ac2b50a-44e4-466e-9d49-bad6bd40092c",
            "value":"positive",
            "confidence":0.9673
         }
      ]
   }
}

```

<b>Sample Utterances</b>

```
# Scheduled inquiries
How goes Tuesday?
What's on for Tuesday?
What's the schedule fot Friday?
How goes tomorrow?
What's the schedule for Tuesday?
What's on the day after tomorrow?
What am I doing on Monday?
What is my schedule for tomorrow?
What's the schedule for Thursday?
What's cooking on Tueday?
What does tomorrow look like?
How does thursday look like?
What's on Wednesday?
What is on for tomorrow?
What's on for tomorrow?
Today is the worst day of my life
What's the plan for tomorrow?
How does Thursday look like?
What's the schedule for Monday?
How does tomorrow look like?
What's my day like?
What does the day after tomorrow look like
What's cooking tomorrow?
What is my schedule for today?
What's on tonight?
What's up for tomorrow?
What's up today?
How goes Monday

# Emotional state
I am on top of the world
I am very happy today
What's going on tomorrow?
i am feeling stressed out
I feel like garbage
I am feeling down
I am super excited today
I am so anxious
I am feeling happy
I feel fine
I am kinda bored
```
