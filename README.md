![bruh](https://wusa.ca/sites/ca.waterloo-undergraduate-student-association/files/uploads/images/logo-studentcare.png)
<h1><b>StudentCare</b></h1>
A bot for helping students manage their workload and relieve their stress.

<b><h2>Dependencies</h2></b>

1. Flask (pip install flask)
2. Wit (pip install wit)


<b><h2>Utterances</h2></b>

Each utterance is related to an <i>entity</i> that consists of a <i>role</i>. 
There is currently only one entity which is 'show_schedule' and it has only one role associated with it; 'day'. The 'day' role consists of the following values: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, today, tomorrow, and tonight

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

<b>Sample Utterances</b>

```
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
What's the plan for tomorrow?
What's going on tomorrow?
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
```
