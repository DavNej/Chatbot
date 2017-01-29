"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import urllib.request
import json

@route('/', method='GET')
def index():
    return template("chatbot.html")

unknown_name = False

def name(message):
    print("Name")
    return True

def all_upper(message):
    num_of_letters = len([char for char in message if char.isalpha()])
    num_of_caps = len([char for char in message if char.isupper()])

    if num_of_caps == num_of_letters and num_of_letters != 0:
        return True

def heartbroke(message):
    negation = ["don't", "dont", "doesn't", "no", "not", "doesnt", "never"]
    love = ["like", "love"]
    hate = ["hate", "hates"]
    
    if any(x in negation for x in message):
        answer =  any(x in love for x in message) and "you" in message
    else:
        answer =  any(x in hate for x in message) and "you" in message
    return answer

def is_insults(message):
    for word in message:
        word.lower()

    swear_words = ["fuck", "fucking", "shit", "putain", "connard", "cunt", "bitch"]
    return any(x in swear_words for x in message)

def get_jokes():
    try:
        url = 'http://api.icndb.com/jokes/random'
        json_obj = urllib.request.urlopen(url)
        response_obj = json.loads(json_obj.read().decode('utf-8'))
        return response_obj['value']['joke']

    except Exception as e:
        print(str(e))



@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    words = user_message.split()

    if all_upper(user_message):
        return json.dumps(REPLY["allcaps"])
    elif "jokes" in words or "joke" in words:
        return json.dumps({"animation": "excited", "msg": get_jokes()})
    elif heartbroke(words):
        return json.dumps(REPLY["heartbroke"])
    elif user_message[-1] == '?':
        return json.dumps(REPLY["question"])
    elif unknown_name and name(user_message):
        return json.dumps({
            "animation": REPLY["greetings"]["animation"],
            "msg": REPLY["greetings"]["msg"] + user_message})
    elif is_insults(words):
        return json.dumps(REPLY["insults"])
    else:
        return json.dumps({
            "animation": REPLY["default"]["animation"],
            "msg": user_message})

REPLY = {
    "allcaps": {
        "animation": "no",
        "msg": "It seems like your caps-lock key is on. I prefer small case."},
    "question": {
        "animation": "giggling",
        "msg": "This is a nice question, but I'm sorry I didn't learn how to answer those yet..."},
    "greetings":{
        "animation": "ok",
        "msg": "It is nice to meet you "},
    "insults": {
        "animation": "afraid",
        "msg": "I'm sorry but I dont understand that kind of language. Please refrase..."},
    "heartbroke": {
        "animation": "heartbroke",
        "msg": "You just broke my heart :'("},
    "default": {
        "animation": "confused",
        "msg":""}
    }

##############################

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})

@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
