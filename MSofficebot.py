from nltk.chat.util import Chat, reflections
import re
import random
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta
from teacher_room_number import teacher_rooms
import json
import requests

# === This is the extension code for the NLTK library ===

class ContextChat(Chat):
    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response

                if callable(resp):
                    resp = resp(match.groups())
                
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num + 1)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.": user_input = user_input[:-1]    
                print(self.respond(user_input))

# === Your code should go here ===

school_bus_time = ["3:45", "4:30", "5:30"]

lunch_time = {
    "not wednesday": ["11:00", "11:40"], 
    "wednesday": ["13:35", "14:20"]
    }

def find_teacher_room(teacher):
    return teacher_rooms[teacher]

today_datetime = datetime.now()
today_date = today_datetime.strftime('%Y-%m-%d')
str_today_date = str(today_date)
date_1 = datetime.strptime('2018-01-28', '%Y-%m-%d')
date_2 = date_1 + timedelta(days=1)
date_2 = date_2.strftime('%Y-%m-%d')
date_3 = date_1 + timedelta(days=2)
date_3 = date_3.strftime('%Y-%m-%d')
date_4 = date_1 + timedelta(days=4)
date_4 = date_4.strftime('%Y-%m-%d')
date_1 = "Day B"
date_2 = "Day C"
date_3 = "Day D"
date_4 = "Day A"

def find_day(date):
    day = ""
    return day
    


pairs = [
    [
      	r'(when)(.*)(schoolbus|bus)(leave)?',
      	['Buses leave at {0}.'.format(school_bus_time)]
    ],
    [
        r'(when)(.*)(lunch)(.*)(monday|tuesday|thursday|friday?)', 
        ['Lunch is between {0}.'.format(lunch_time["not wednesday"])]
    ],
    [
        r'(when)(.*)(lunch)(.*)(wednesday?)', 
        ['Lunch is between {0} on Wednesdays.'.format(lunch_time["wednesday"])]
    ],
    [
      	r'(when)(.*)(lunch?)',
      	['Lunch is between {0} on most days.'.format(lunch_time["not wednesday"])]
    ],
    [
        r'(where is)(.*)(room?)',
        [lambda matches: "It is in " + str( find_teacher_room(matches[1].strip()) )] #credits: Michał
    ],
    [
        r'(what day is it?)',
        ['Today is {0}'.format(str_today_date)]
    ],
    [
      	r'(where is MS Lost and Found?)',
      	['MS Lost and Found is next to the MS Office.']
    ],
    [
      	r"(why can't I use my phone?)",
      	["You can't use your phone because it may distract you from learning."]
    ],
    [
        r'(how do I quit?)',
        ["To quit, you simply enter the word 'quit'."]
    ],
    [
        r'(how are you?)',
        ["Fine, thank you!"]
    ],
    [
        r'(hi)',
        ["Hi!"]
    ],
    [
        r'(hello)',
        ["Hello."]
    ],
    [
        r'(.*)(thanks|thank you|thx)(.*)',
        ["You're welcome."]
    ],
    [
        r'(quit)',
        ["Bye!"]
    ],
  	[
        r'(.*)',
        ["Maybe you should try to rephrase your question."],
    ]
]

if __name__ == "__main__":
    name = "MSofficeBot"
    print("Hi, I am {0}.".format(name))
    username = input("What's your name? ")
    print("Okay, so your name is {0}.".format(username))
    
    user_feeling = input("How are you today? ")
    if user_feeling == "good" or user_feeling == "fine":
        print("I'm glad.")
    elif user_feeling == "great":
        print("Cool!")
    elif user_feeling == "bad" or user_feeling == "not good":
        event = input("That's not good! What happened? ")
        print("That's very unfortunate, I hope it gets better!")
    else:
        print("Cool!")

    print("So {0}, what questions do you have?".format(username))
    print(date_4)

    chat = ContextChat(pairs, reflections)
    chat.converse()
